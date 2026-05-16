from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    text: str
    history: list

@app.post("/senddata")
def senddata(message: Message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=message.history + [{ "role": "user", "content": message.text }]
    )
    reply = response.choices[0].message.content
    return { "reply": reply }