from fastapi import APIRouter

from app.schemas.entry import EntryCreate
from app.services.entry_service import write_entry_markdown

router = APIRouter(prefix="/entries", tags=["entries"])


@router.post("", status_code=201)
def create_entry(entry: EntryCreate) -> dict[str, str]:
    """
    Accept an entry from the frontend, write it to a Markdown file,
    and return the node_id so the frontend can confirm which entry was saved.
    """
    file_path = write_entry_markdown(entry)
    return {"node_id": entry.node_id, "file": file_path.name}
