# Pregunta - Ask AI 🤖

A conversational AI chat app that lets you have a full conversation with an AI powered by Groq. The app remembers the full chat history so the AI understands context from previous messages.

---

## Screenshots

> Chat interface with AI responses powered by Groq

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Axios, Vite |
| Backend | FastAPI, Python |
| AI Model | Groq — llama-3.3-70b-versatile |
| Styling | CSS, Bootstrap Icons |

---

## Prerequisites

Make sure you have these installed before starting:

- [Node.js](https://nodejs.org/) — v18 or higher
- [Python](https://www.python.org/) — v3.10 or higher
- [Git](https://git-scm.com/)
- A Groq API key — get one free at [https://console.groq.com](https://console.groq.com)

---

## Step 1 — Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/danny23-hossam/Pregunta-askai.git
```

Navigate into the project folder:

```bash
cd Pregunta-askai
```

---

## Step 2 — Setup the Backend

Navigate into the backend folder:

```bash
cd backend
```

Install all required Python packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:

```bash
# Windows
New-Item .env

# Mac/Linux
touch .env
```

Open the `.env` file and add your Groq API key:

```
API_Key=your_groq_api_key_here
```

> You can get a free API key at https://console.groq.com

Start the backend server:

```bash
uvicorn backend:app --reload --port 8000
```

You should see this in your terminal:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using StatReload
```

> Keep this terminal open and running.

---

## Step 3 — Setup the Frontend

Open a **new terminal** and navigate to the frontend folder:

```bash
cd Pregunta-askai/frontend
```

Install all required Node packages:

```bash
npm install
```

Start the frontend development server:

```bash
npm run dev
```

You should see this in your terminal:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## Step 4 — Open in Browser

Open your browser and go to:

```
http://localhost:5173
```

You should see the Pregunta chat app running and ready to use.

---

## How it Works

```
You type a message in the chat input
            ↓
React sends the message + full chat history to FastAPI on port 8000
            ↓
FastAPI passes everything to Groq AI
            ↓
Groq reads the full history and generates a context-aware reply
            ↓
Reply is sent back to React and displayed in the chat
```

The app keeps two lists:
- **messages** — what you see in the chat UI
- **history** — what gets sent to Groq so it remembers the conversation

---

## Project Structure

```
Pregunta-askai/
├── backend/
│   ├── backend.py           # FastAPI server + Groq integration
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Your API key (never upload this)
│
├── frontend/
│   ├── src/
│   │   ├── Components/
│   │   │   ├── Chat.jsx     # Main chat UI component
│   │   │   ├── Chat.css     # Chat styles
│   │   │   ├── Header.jsx   # Top navigation bar
│   │   │   ├── Header.css   # Header styles
│   │   │   ├── Footer.jsx   # Bottom footer
│   │   │   └── Footer.css   # Footer styles
│   │   ├── App.jsx          # Root component
│   │   └── App.css          # Global styles
│   ├── index.html
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## Environment Variables

The backend requires a `.env` file with the following:

```
API_Key=your_groq_api_key_here
```

> Never share or upload your `.env` file. It is already listed in `.gitignore`.

---

## Common Issues

**Backend not starting?**
```
Make sure Python is installed:
python --version

Make sure all packages are installed:
pip install -r requirements.txt
```

**Frontend not connecting to backend?**
```
Make sure the backend is running on port 8000.
You should see http://127.0.0.1:8000 in the backend terminal.
Both terminals must be open at the same time.
```

**AI not responding / Something went wrong?**
```
Check your .env file has the correct API key.
Make sure the key is named exactly: API_Key
Generate a new key at https://console.groq.com if needed.
```

**Port already in use?**
```bash
# Run backend on a different port
uvicorn backend:app --reload --port 8001

# Then update the URL in Chat.jsx
axios.post("http://localhost:8001/senddata", ...)
```

---

## License

MIT License — feel free to use and modify this project.

---

## Author

Made by [danny23-hossam](https://github.com/danny23-hossam)
