# 🚀 Pregunta AskAI - Fullstack Dockerized Application

A fullstack web application built with a **React (Vite) frontend** and a **Python backend**, fully containerized using **Docker & Docker Compose** for easy development and deployment.

---

## 📌 Overview

This project is a simple fullstack chat-style application structure that demonstrates:

- Frontend built with React + Vite
- Backend API built with Python
- Containerized development using Docker
- Multi-service orchestration with Docker Compose

---

## 🧱 Tech Stack

### Frontend
- React (Vite)
- JavaScript (ES6+)
- CSS (Component-based styling)

### Backend
- Python
- REST API (FastAPI / Flask-style structure)

### DevOps
- Docker
- Docker Compose

---

## 📁 Project Structure


Pregunta-askai/
│
├── backend/
│ ├── backend.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── frontend/
│ ├── my-app/
│ │ ├── public/
│ │ ├── src/
│ │ ├── index.html
│ │ └── vite.config.js
│ │
│ ├── Dockerfile
│ ├── package.json
│ └── package-lock.json
│
├── docker-compose.yml
└── README.md


---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/danny23-hossam/Pregunta-askai.git
cd Pregunta-askai
2. Run with Docker

Make sure Docker Desktop is running:

docker compose up --build
3. Stop containers
docker compose down
🌐 Access the App
Frontend: http://localhost:5173
Backend: http://localhost:8000
🧪 Features
Fullstack Dockerized setup
React frontend (Vite)
Python backend API
Hot reload during development
Clean modular structure
Easy local setup with one command
🐳 Docker Architecture

Docker Compose runs two services:

frontend → React (Vite) app
backend → Python API server

Both services communicate over a shared Docker network.
