# ReflectionsApp

Monorepo for a local-first reflection app.

## Stack

- Frontend: React + TypeScript (Vite)
- Backend: FastAPI (Python)
- Local LLM: Ollama (`qwen2.5:7b` or any locally available model)
- Later: SQLite and Chroma

## Repository Layout

- `apps/web` — React frontend
- `apps/api` — FastAPI backend
- `data/nodes/human/` — Diary entries as Markdown files (gitignored)
- `data/chats/` — Saved chat conversations as JSON files (gitignored)
- `.github/workflows` — CI definitions

## Quick Start

### Backend
```bash
cd apps/api
python -m venv .venv
.venv/Scripts/activate        # Windows
source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend
```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:5173. The Vite proxy forwards `/api/*` to FastAPI on port 8000.

### Ollama
Install from https://ollama.com, then:
```bash
ollama pull qwen2.5:7b
```
Ollama must be running for the chat feature to work.
