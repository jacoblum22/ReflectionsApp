from pathlib import Path

from app.schemas.entry import EntryCreate

# Resolve the data directory relative to the project root.
# __file__ is apps/api/app/services/entry_service.py
# So we go up 4 levels to reach the repo root, then into data/nodes/human/.
_HUMAN_NODES_DIR = Path(__file__).resolve().parents[4] / "data" / "nodes" / "human"


def write_entry_markdown(entry: EntryCreate) -> Path:
    """
    Write an entry to a Markdown file with YAML frontmatter.
    Returns the path of the written file.
    """
    _HUMAN_NODES_DIR.mkdir(parents=True, exist_ok=True)

    content = f"""---
node_id: {entry.node_id}
title_or_name: {entry.title_or_name}
created_at: {entry.created_at}
---

{entry.body_text}
"""

    file_path = _HUMAN_NODES_DIR / f"{entry.node_id}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path
