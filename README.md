# ReflectionsApp

Monorepo for a local-first reflection app.

## Stack

- Frontend: React
- Backend: FastAPI
- Local LLM: Ollama
- Later: SQLite and Chroma

## Repository Layout

- `apps/web` React frontend
- `apps/api` FastAPI backend
- `packages/shared` Shared contracts/constants
- `data` Local content and runtime folders
- `docs` Architecture, API, and decisions
- `.github/workflows` CI definitions

## Quick Start

1. Frontend and backend setup docs are in each app folder.
2. Keep Python dependencies inside `apps/api/.venv`.
3. Copy `.env.example` to `.env` when you wire runtime configuration.
