# Run Pregunta AskAI WITHOUT Docker (XAMPP MySQL + local MongoDB)

This guide runs everything directly on your machine — no Docker.

- **MySQL** → provided by **XAMPP** (stores users)
- **MongoDB** → local **MongoDB Community Server** (stores chat history)
- **Backend** → Python / FastAPI (uvicorn)
- **Frontend** → Node / React (Vite)

---

## 0. Install prerequisites (one time)

| Tool | Why | Download |
|------|-----|----------|
| XAMPP | MySQL database | https://www.apachefriends.org/ |
| MongoDB Community Server | NoSQL database | https://www.mongodb.com/try/download/community |
| Python 3.11+ | Backend | https://www.python.org/downloads/ (check "Add Python to PATH") |
| Node.js 18+ | Frontend | https://nodejs.org/ |

---

## 1. Start MySQL (XAMPP)

1. Open the **XAMPP Control Panel** → click **Start** on **MySQL** (and **Apache** so you can use phpMyAdmin).
2. Open http://localhost/phpmyadmin
3. Click **New** (left side) → create a database named **`pregunta`** → **Create**.
   - You do **not** need to create any tables — the backend creates the `users` table automatically on first start.
   - XAMPP's default MySQL login is user **`root`** with an **empty password** (this is already set in `.env`).

## 2. Start MongoDB

- **Windows:** MongoDB usually installs as a service and is already running. To confirm, open "Services" and check **MongoDB Server** is *Running*. (Or run `mongod` manually.)
- **Mac (Homebrew):** `brew services start mongodb-community`
- **Linux:** `sudo systemctl start mongod`

MongoDB must be listening on the default `mongodb://localhost:27017`.

## 3. Configure your environment

In the project folder, copy the local env preset to `.env`:

- **Windows:** `copy .env.local.example .env`
- **Mac/Linux:** `cp .env.local.example .env`

Then open `.env` and paste your **Groq API key** (free at https://console.groq.com/keys):

```
GROQ_API_KEY=your_real_key_here
```

The MySQL/MongoDB values are already set for XAMPP + local MongoDB — leave them as-is.

## 4. Start the backend

- **Windows:** double-click **`start-backend.bat`**
- **Mac/Linux:** `bash start-backend.sh`

This creates a Python virtual environment, installs dependencies, and starts the API on **http://localhost:8000**.
Wait until you see `Application startup complete`. (API docs: http://localhost:8000/docs)

## 5. Start the frontend

Open a **second** terminal:

- **Windows:** double-click **`start-frontend.bat`**
- **Mac/Linux:** `bash start-frontend.sh`

This installs dependencies and starts the app on **http://localhost:5173**.

## 6. Use the app

1. Open http://localhost:5173
2. Click **Sign up** → create an account.
3. Chat. Each conversation appears in the left sidebar.
4. Log out and back in — your conversations reload from MongoDB.

---

## Verify both databases hold data

- **MySQL (users):** in phpMyAdmin open the `pregunta` database → `users` table → you'll see your account.
- **MongoDB (chat history):** run `mongosh` then:
  ```
  use pregunta
  db.conversations.find({}, { user_id: 1, title: 1 })
  ```
  Each conversation has a `user_id` equal to the `id` of your user row in MySQL — that's the link between the two databases.

---

## Troubleshooting

- **Backend can't connect to MySQL:** make sure XAMPP MySQL is started and the `pregunta` database exists. If your XAMPP `root` has a password, set `MYSQL_PASSWORD=` in `.env` accordingly.
- **Backend can't connect to MongoDB:** make sure the MongoDB service is running on port 27017.
- **AI replies fail (502):** your `GROQ_API_KEY` in `.env` is missing or invalid.
- **`python` not found (Windows):** reinstall Python with "Add Python to PATH" checked, or use `py -m venv venv`.
