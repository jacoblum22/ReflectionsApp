from fastapi import APIRouter, HTTPException

from app.schemas.entry import EntryCreate, EntryDetail, EntrySummary
from app.services.entry_service import get_entry, list_entries, write_entry_markdown

router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("", response_model=list[EntrySummary])
def read_entries() -> list[EntrySummary]:
    """Return all entries sorted newest-first, without body text."""
    return list_entries()


@router.get("/{node_id}", response_model=EntryDetail)
def read_entry(node_id: str) -> EntryDetail:
    """Return a single entry including body text."""
    entry = get_entry(node_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.post("", status_code=201)
def create_entry(entry: EntryCreate) -> dict[str, str]:
    """
    Accept an entry from the frontend, write it to a Markdown file,
    and return the node_id so the frontend can confirm which entry was saved.
    """
    file_path = write_entry_markdown(entry)
    return {"node_id": entry.node_id, "file": file_path.name}
