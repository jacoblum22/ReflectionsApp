from datetime import datetime
from pathlib import Path

import frontmatter

from app.schemas.entry import EntryCreate, EntryDetail, EntrySummary

# Resolve the data directory relative to the project root.
# __file__ is apps/api/app/services/entry_service.py
# So we go up 4 levels to reach the repo root, then into data/nodes/human/.
_HUMAN_NODES_DIR = Path(__file__).resolve().parents[4] / "data" / "nodes" / "human"


def list_entries() -> list[EntrySummary]:
    """
    Read all .md files and return a list of EntrySummary sorted newest-first.
    Only parses frontmatter — body content is not loaded.
    """
    summaries: list[EntrySummary] = []
    for path in _HUMAN_NODES_DIR.glob("*.md"):
        post = frontmatter.load(str(path))
        summaries.append(
            EntrySummary(
                node_id=str(post.get("node_id", path.stem)),
                title_or_name=str(post.get("title_or_name", "Untitled")),
                created_at=str(post.get("created_at", "")),
            )
        )
    return sorted(summaries, key=lambda e: e.created_at, reverse=True)


def get_entry(node_id: str) -> EntryDetail | None:
    """
    Load a single entry by node_id. Returns None if the file does not exist.
    """
    path = _HUMAN_NODES_DIR / f"{node_id}.md"
    if not path.exists():
        return None
    post = frontmatter.load(str(path))
    return EntryDetail(
        node_id=str(post.get("node_id", node_id)),
        title_or_name=str(post.get("title_or_name", "Untitled")),
        created_at=str(post.get("created_at", "")),
        body_text=post.content,
    )


def write_entry_markdown(entry: EntryCreate) -> Path:
    """
    Write an entry to a Markdown file with YAML frontmatter.
    created_at is stored as a full ISO 8601 datetime: the user's chosen date
    combined with the current clock time, so same-day entries sort by write order.
    Returns the path of the written file.
    """
    _HUMAN_NODES_DIR.mkdir(parents=True, exist_ok=True)

    # Combine the user's chosen date (YYYY-MM-DD) with the current time.
    now = datetime.now()
    created_at = datetime(
        year=int(entry.created_at[:4]),
        month=int(entry.created_at[5:7]),
        day=int(entry.created_at[8:10]),
        hour=now.hour,
        minute=now.minute,
        second=now.second,
    ).isoformat()

    content = f"""---
node_id: {entry.node_id}
title_or_name: {entry.title_or_name}
created_at: {created_at}
---

{entry.body_text}
"""

    file_path = _HUMAN_NODES_DIR / f"{entry.node_id}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path
