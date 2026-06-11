"""Pregunta AskAI backend.

Hybrid persistence:
  * MySQL (relational)  -> user accounts / authentication
  * MongoDB (NoSQL)     -> chat history, linked to a user via MySQL user id
"""
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import db_mongo
from auth import create_access_token, decode_access_token, hash_password, verify_password
from db_mysql import User, get_session, init_db

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

app = FastAPI(title="Pregunta AskAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# --------------------------------------------------------------------------- #
# Schemas
# --------------------------------------------------------------------------- #
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    user: dict


class SendDataRequest(BaseModel):
    text: str
    conversation_id: str | None = None


class CreateConversationRequest(BaseModel):
    title: str | None = None


# --------------------------------------------------------------------------- #
# Auth dependency
# --------------------------------------------------------------------------- #
def current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_session),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def _user_dict(user: User) -> dict:
    return {"id": user.id, "username": user.username, "email": user.email}


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "groq_configured": groq_client is not None}


@app.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_session)) -> AuthResponse:
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    db.refresh(user)
    token = create_access_token(user.id, user.username)
    return AuthResponse(token=token, user=_user_dict(user))


@app.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_session)) -> AuthResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id, user.username)
    return AuthResponse(token=token, user=_user_dict(user))


@app.get("/me")
def me(user: User = Depends(current_user)) -> dict:
    return _user_dict(user)


@app.get("/conversations")
def list_conversations(user: User = Depends(current_user)) -> list[dict]:
    return db_mongo.list_conversations(user.id)


@app.post("/conversations")
def create_conversation(
    payload: CreateConversationRequest, user: User = Depends(current_user)
) -> dict:
    return db_mongo.create_conversation(user.id, payload.title or "New chat")


@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str, user: User = Depends(current_user)) -> dict:
    conversation = db_mongo.get_conversation(user.id, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, user: User = Depends(current_user)) -> dict:
    if not db_mongo.delete_conversation(user.id, conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"deleted": True}


@app.post("/senddata")
def senddata(payload: SendDataRequest, user: User = Depends(current_user)) -> dict:
    if groq_client is None:
        raise HTTPException(status_code=503, detail="GROQ_API_KEY is not configured")

    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message text is required")

    # Load existing history (dynamic, from Mongo) for an existing conversation.
    conversation_id = payload.conversation_id
    history: list[dict] = []
    if conversation_id:
        conversation = db_mongo.get_conversation(user.id, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        history = [
            {"role": m["role"], "content": m["content"]} for m in conversation["messages"]
        ]

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=history + [{"role": "user", "content": text}],
        )
    except Exception as err:  # surface Groq/API issues without a raw 500
        raise HTTPException(status_code=502, detail=f"AI provider error: {err}")
    reply = response.choices[0].message.content

    # Only create a conversation once we have a successful reply to store.
    if not conversation_id:
        conversation_id = db_mongo.create_conversation(user.id)["id"]

    # Persist both turns to MongoDB.
    db_mongo.append_messages(
        user.id,
        conversation_id,
        [
            {"role": "user", "content": text},
            {"role": "assistant", "content": reply},
        ],
    )

    return {"reply": reply, "conversation_id": conversation_id}
