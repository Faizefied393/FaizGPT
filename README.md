# FaizGPT – Full-Stack AI Assistant

FaizGPT is a full-stack AI-powered assistant built using modern LLM APIs, FastAPI, and a custom retrieval system. This project simulates a production-style AI application with chat memory, document-based question answering (RAG), and a clean frontend interface.

---

## Overview

FaizGPT allows users to:

- Chat with an AI assistant in real-time
- Maintain session-based memory across conversations
- Upload documents and ask context-aware questions
- Interact through a browser-based UI

This project demonstrates practical AI system design, backend engineering, and real-world integration of LLMs.

---

## Features

### Conversational AI Chat
- Built using OpenAI API
- Structured prompt system
- Real-time responses

### Session Memory
- Stores chat history per session
- JSON-based persistence
- Context-aware responses

### Document Upload + Q&A (RAG)
- Upload `.txt` or `.md` files
- Automatic chunking and indexing
- Query-based retrieval system

### Frontend Interface
- Simple chat UI using HTML, CSS, JavaScript
- Real-time interaction with backend API

### Backend API
- Built with FastAPI
- RESTful endpoints
- Auto-generated Swagger docs

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python, FastAPI, OpenAI SDK, dotenv |
| **Frontend** | HTML, CSS, JavaScript |
| **Data Handling** | JSON (chat memory), Custom RAG system |
| **Tools** | Git & GitHub, VS Code, Uvicorn |

---

## Project Structure

```
faizgpt/
│
├── app/
│   ├── main.py          # FastAPI app
│   ├── llm.py           # LLM logic
│   ├── memory.py        # Chat memory system
│   ├── rag.py           # Document retrieval (RAG)
│   └── schemas.py       # API schemas
│
├── data/
│   ├── chats/           # Stored conversations
│   ├── uploads/         # Uploaded files
│   └── vectors/         # Indexed document chunks
│
├── frontend/
│   ├── index.html       # UI
│   ├── style.css
│   └── script.js
│
├── .env
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/faizgpt.git
cd faizgpt
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create `.env` in root:

```env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4.1-mini
```

### 5. Run backend

```bash
uvicorn app.main:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

### 6. Run frontend

Open `frontend/index.html` directly, or use Live Server in VS Code.

---

## Testing the Application

### Backend Health

Visit:

```
http://127.0.0.1:8000/
```

### Chat

Use the UI or send a request to the `/chat` endpoint:

```json
{
  "session_id": "test123",
  "message": "Explain what FaizGPT does"
}
```

### Memory

Send this message:

```
My name is Faiz
```

Then follow up with:

```
What is my name?
```

### File Upload (RAG)

Upload a file like `sample.txt` with contents such as:

```
FaizGPT is built using FastAPI and OpenAI.
```

Then ask:

```
What technologies does FaizGPT use?
```

---

## Challenges & Debugging

During development, several real-world issues were encountered and resolved:

| Issue | Fix |
|-------|-----|
| Windows file system conflicts (`data/chats`, `uploads`, `vectors`) | Absolute path resolution (`Path(__file__)`) |
| Relative vs absolute path handling | Proper path construction from `__file__` |
| Environment variable loading issues | Correct `.env` loading with `python-dotenv` |
| FastAPI import errors | Dependency validation and module restructuring |
| API key configuration problems | File system validation checks |

---

## Future Improvements

- 🔹 PDF support
- 🔹 Embeddings + FAISS vector search
- 🔹 User authentication system
- 🔹 Database (SQLite/PostgreSQL)
- 🔹 Streaming responses (ChatGPT-style)
- 🔹 React frontend
- 🔹 Docker deployment
- 🔹 Local LLM support (Ollama)

---

## Resume / Portfolio Value

This project demonstrates:

-  Full-stack development
-  API integration with LLMs
-  Backend system design
-  State management (memory)
-  Retrieval-based AI workflows (RAG)
-  Debugging and real-world problem solving

---

## Author

**Faiz Tariq**  
Cybersecurity Student | AI + Security Enthusiast

[![GitHub](https://img.shields.io/badge/GitHub-FaizMasood-181717?style=flat&logo=github)](https://github.com/Faizefied393)