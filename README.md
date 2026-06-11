# 🚀 Pregunta AskAI - Fullstack Dockerized Application

A fullstack AI chat application built with a **React (Vite) frontend** and a **Python (FastAPI) backend**, using a **hybrid database** setup — **MySQL** for user accounts and **MongoDB** for chat history — fully containerized with **Docker & Docker Compose**.

---

## 📌 Overview

- User registration & login (JWT auth) stored in **MySQL** (relational).
- Chat history stored in **MongoDB** (NoSQL), with each conversation linked to its
  owner via the MySQL `user_id`.
- Conversation history is loaded **dynamically** per user from MongoDB.
- AI replies powered by Groq (`llama-3.3-70b-versatile` by default).

---

## 🧱 Tech Stack

### Frontend
- React (Vite), JavaScript (ES6+), component-based CSS

### Backend
- Python, FastAPI
- SQLAlchemy + PyMySQL (MySQL)
- PyMongo (MongoDB)
- JWT auth (PyJWT) + bcrypt password hashing (passlib)

### Databases
- **MySQL 8** → relational store for users
- **MongoDB 7** → document store for chat history

### DevOps
- Docker, Docker Compose

---

## 🗄️ Hybrid Database Design

```
MySQL (relational)                MongoDB (NoSQL)
┌─────────────────────────┐       ┌──────────────────────────────────────────┐
│ users                   │       │ conversations                            │
│  id (PK) ───────────────┼──────►│  user_id  ── references MySQL users.id   │
│  username (unique)      │       │  title                                   │
│  email (unique)         │       │  created_at / updated_at                 │
│  password_hash          │       │  messages: [{ role, content, ts }]       │
│  created_at             │       └──────────────────────────────────────────┘
└─────────────────────────┘
```

The two databases relate to each other through the integer `user_id`: a MongoDB
conversation document always carries the id of the MySQL user that owns it.

---

## 🔌 API Endpoints

| Method | Path                          | Auth | Description                              |
|--------|-------------------------------|------|------------------------------------------|
| GET    | `/health`                     | no   | Service + Groq status                    |
| POST   | `/register`                   | no   | Create user (MySQL), return JWT          |
| POST   | `/login`                      | no   | Authenticate, return JWT                 |
| GET    | `/me`                         | yes  | Current user                             |
| GET    | `/conversations`              | yes  | List the user's conversations (MongoDB)  |
| POST   | `/conversations`              | yes  | Create a conversation                    |
| GET    | `/conversations/{id}`         | yes  | Get one conversation with messages       |
| DELETE | `/conversations/{id}`         | yes  | Delete a conversation                    |
| POST   | `/senddata`                   | yes  | Send a message, get AI reply, persist    |

---

## 📁 Project Structure

```
Pregunta-askai/
├── backend/
│   ├── backend.py        # FastAPI app & routes
│   ├── db_mysql.py       # SQLAlchemy engine + User model (MySQL)
│   ├── db_mongo.py       # PyMongo chat-history helpers (MongoDB)
│   ├── auth.py           # bcrypt hashing + JWT
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── my-app/           # React (Vite) source
│   └── Dockerfile
├── docker-compose.yml    # mysql + mongo + backend + frontend
├── .env.example
└── README.md
```

---

## ⚙️ Getting Started

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your **Groq API key** (free at https://console.groq.com/keys):

```
GROQ_API_KEY=your_real_key_here
```

The MySQL/Mongo credentials already have working defaults.

### 2. Run with Docker

```bash
docker compose up --build
```

This starts four services: `mysql`, `mongo`, `backend`, `frontend`.

### 3. Stop containers

```bash
docker compose down
```

To wipe stored data too: `docker compose down -v`.

---

## 🌐 Access the App

- Frontend: http://localhost:5173
- Backend (API docs): http://localhost:8000/docs

Register an account, start chatting, and your conversations will appear in the
sidebar — reloaded dynamically from MongoDB on every login.
