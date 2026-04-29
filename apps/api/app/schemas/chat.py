from pydantic import BaseModel


class ChatMessage(BaseModel):
    """A single message in the conversation history."""

    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """
    Request body for POST /chat.
    - entry_id: the node_id of the diary entry to chat about
    - model: the Ollama model name to use (e.g. "qwen2.5:7b")
    - messages: the full conversation history so far (oldest first)
    """

    entry_id: str
    model: str
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    """The assistant's reply to the latest message."""

    role: str
    content: str
