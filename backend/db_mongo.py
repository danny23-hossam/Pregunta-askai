"""NoSQL database layer (MongoDB via PyMongo).

Stores chat history. Each conversation document references the MySQL user id via
the ``user_id`` field, dynamically linking a NoSQL document to a relational row.

Conversation document shape::

    {
        "_id": ObjectId,
        "user_id": 1,                     # -> MySQL users.id
        "title": "New chat",
        "created_at": datetime,
        "updated_at": datetime,
        "messages": [
            {"role": "user", "content": "...", "ts": datetime},
            {"role": "assistant", "content": "...", "ts": datetime},
        ],
    }
"""
import os
from datetime import datetime, timezone

from bson import ObjectId
from pymongo import DESCENDING, MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "pregunta")

_client = MongoClient(MONGO_URL)
_db = _client[MONGO_DB]
conversations = _db["conversations"]
conversations.create_index([("user_id", DESCENDING), ("updated_at", DESCENDING)])


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _serialize(doc: dict) -> dict:
    """Convert a Mongo document into a JSON-serializable dict."""
    return {
        "id": str(doc["_id"]),
        "user_id": doc["user_id"],
        "title": doc.get("title", "New chat"),
        "created_at": doc["created_at"].isoformat(),
        "updated_at": doc["updated_at"].isoformat(),
        "messages": [
            {
                "role": m["role"],
                "content": m["content"],
                "ts": m["ts"].isoformat() if isinstance(m.get("ts"), datetime) else m.get("ts"),
            }
            for m in doc.get("messages", [])
        ],
    }


def create_conversation(user_id: int, title: str = "New chat") -> dict:
    now = _now()
    doc = {
        "user_id": user_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": [],
    }
    result = conversations.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize(doc)


def list_conversations(user_id: int) -> list[dict]:
    cursor = conversations.find({"user_id": user_id}).sort("updated_at", DESCENDING)
    return [_serialize(doc) for doc in cursor]


def get_conversation(user_id: int, conversation_id: str) -> dict | None:
    try:
        oid = ObjectId(conversation_id)
    except Exception:
        return None
    doc = conversations.find_one({"_id": oid, "user_id": user_id})
    return _serialize(doc) if doc else None


def append_messages(user_id: int, conversation_id: str, messages: list[dict]) -> dict | None:
    """Append messages to a conversation owned by ``user_id``."""
    try:
        oid = ObjectId(conversation_id)
    except Exception:
        return None

    now = _now()
    stamped = [{"role": m["role"], "content": m["content"], "ts": now} for m in messages]

    update: dict = {"$push": {"messages": {"$each": stamped}}, "$set": {"updated_at": now}}

    # Title the conversation from the first user message if still default.
    existing = conversations.find_one({"_id": oid, "user_id": user_id})
    if not existing:
        return None
    if existing.get("title", "New chat") == "New chat":
        first_user = next((m["content"] for m in stamped if m["role"] == "user"), None)
        if first_user:
            update["$set"]["title"] = first_user[:40]

    conversations.update_one({"_id": oid, "user_id": user_id}, update)
    doc = conversations.find_one({"_id": oid, "user_id": user_id})
    return _serialize(doc) if doc else None


def delete_conversation(user_id: int, conversation_id: str) -> bool:
    try:
        oid = ObjectId(conversation_id)
    except Exception:
        return False
    result = conversations.delete_one({"_id": oid, "user_id": user_id})
    return result.deleted_count > 0
