"""
Tests for the /entries endpoints.

Each test uses a temporary directory (tmp_path, provided by pytest) instead of
the real data/nodes/human/ folder. The service's _HUMAN_NODES_DIR constant is
monkey-patched so tests are fully isolated and leave no files behind.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
import app.services.entry_service as entry_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Redirect _HUMAN_NODES_DIR to a fresh temp directory for every test.
    Because autouse=True, this runs automatically for every test in this file
    without needing to explicitly request it.
    """
    monkeypatch.setattr(entry_service, "_HUMAN_NODES_DIR", tmp_path)


def test_create_entry() -> None:
    payload = {
        "node_id": "abc-123",
        "title_or_name": "My Test Entry",
        "created_at": "2026-04-27",
        "body_text": "Hello from the test.",
    }
    response = client.post(
        "/entries",
        content=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201
    assert response.json()["node_id"] == "abc-123"
    # The file should exist in the temp data dir.
    assert (entry_service._HUMAN_NODES_DIR / "abc-123.md").exists()


def test_list_entries_sorted_newest_first(tmp_path: Path) -> None:
    # Write two entries manually so we control their dates.
    (tmp_path / "a.md").write_text(
        "---\nnode_id: a\ntitle_or_name: Older\ncreated_at: 2026-01-01\n---\n\nOld entry.",
        encoding="utf-8",
    )
    (tmp_path / "b.md").write_text(
        "---\nnode_id: b\ntitle_or_name: Newer\ncreated_at: 2026-06-01\n---\n\nNew entry.",
        encoding="utf-8",
    )

    response = client.get("/entries")

    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 2
    # Newest first
    assert entries[0]["node_id"] == "b"
    assert entries[1]["node_id"] == "a"


def test_get_entry_returns_body(tmp_path: Path) -> None:
    (tmp_path / "xyz.md").write_text(
        "---\nnode_id: xyz\ntitle_or_name: Detail Test\ncreated_at: 2026-04-27\n---\n\nThe body.",
        encoding="utf-8",
    )

    response = client.get("/entries/xyz")

    assert response.status_code == 200
    data = response.json()
    assert data["node_id"] == "xyz"
    assert data["body_text"] == "The body."


def test_get_entry_not_found() -> None:
    response = client.get("/entries/does-not-exist")
    assert response.status_code == 404
