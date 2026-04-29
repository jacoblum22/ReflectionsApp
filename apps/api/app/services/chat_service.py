import json
from pathlib import Path

# Parallel to data/nodes/human/ — chats live in data/chats/.
# __file__ is apps/api/app/services/chat_service.py → 4 parents up = repo root.
_CHATS_DIR = Path(__file__).resolve().parents[4] / "data" / "chats"


def load_chat(entry_id: str) -> list[dict[str, str]]:
    """
    Return the saved conversation for the given entry_id,
    or an empty list if no conversation has been saved yet.
    """
    path = _CHATS_DIR / f"{entry_id}.chat.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_chat(entry_id: str, messages: list[dict[str, str]]) -> None:
    """Overwrite the saved conversation for the given entry_id."""
    _CHATS_DIR.mkdir(parents=True, exist_ok=True)
    path = _CHATS_DIR / f"{entry_id}.chat.json"
    path.write_text(json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8")
