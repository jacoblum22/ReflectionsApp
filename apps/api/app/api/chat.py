import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
from app.services.chat_service import load_chat, save_chat
from app.services.entry_service import get_entry

OLLAMA_BASE = "http://localhost:11434"

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/models")
def list_models() -> list[str]:
    """
    Return the names of all locally available Ollama models.
    Useful for verifying the Ollama connection and letting the frontend
    offer a model picker in the future.
    """
    try:
        response = httpx.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        response.raise_for_status()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Cannot reach Ollama. Is it running?",
        ) from exc

    data = response.json()
    return [m["name"] for m in data.get("models", [])]


@router.get("/{entry_id}/history", response_model=list[ChatMessage])
def get_history(entry_id: str) -> list[dict[str, str]]:
    """Load the saved conversation for an entry, or return [] if none yet."""
    return load_chat(entry_id)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a conversation about a diary entry to Ollama and return the reply.

    The diary entry is loaded from disk and injected as a system prompt so the
    model has full context. The complete message history is re-sent each turn —
    this is stateless HTTP, same as the rest of the app.
    After each reply the full conversation is saved to disk automatically.
    """
    entry = get_entry(request.entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")

    system_prompt = (
        "You are a thoughtful, reflective assistant. "
        "The user has written the following diary entry and wants to reflect on it with you.\n\n"
        f"Title: {entry.title_or_name}\n"
        f"Date: {entry.created_at}\n\n"
        f"{entry.body_text}\n\n"
        "Engage with what they've written. Ask questions, offer perspective, and help them reflect."
    )

    # Build the message list for Ollama: system prompt first, then conversation history.
    ollama_messages = [{"role": "system", "content": system_prompt}]
    ollama_messages += [
        {"role": m.role, "content": m.content} for m in request.messages
    ]

    try:
        response = httpx.post(
            f"{OLLAMA_BASE}/api/chat",
            json={"model": request.model, "messages": ollama_messages, "stream": False},
            timeout=120,  # local LLMs can be slow; 2 min is generous but safe
        )
        response.raise_for_status()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Cannot reach Ollama. Is it running?",
        ) from exc
    except httpx.HTTPStatusError as exc:
        # Ollama returned an error (e.g. model not loaded, out of memory).
        raise HTTPException(
            status_code=502,
            detail=f"Ollama error: {exc.response.text}",
        ) from exc

    data = response.json()
    assistant_message = data["message"]
    reply = ChatResponse(
        role=assistant_message["role"], content=assistant_message["content"]
    )

    # Persist the full conversation (user messages + this reply) to disk.
    all_messages = [{"role": m.role, "content": m.content} for m in request.messages]
    all_messages.append({"role": reply.role, "content": reply.content})
    save_chat(request.entry_id, all_messages)

    return reply
