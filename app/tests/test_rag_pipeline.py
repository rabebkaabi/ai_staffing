from pathlib import Path

import pytest


@pytest.mark.asyncio
async def test_index_document_indexes_once_and_then_skips(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    from app.rag.rag_pipeline import index_document

    source_file = tmp_path / "cv.txt"
    source_file.write_text("Python FastAPI Docker Kubernetes", encoding="utf-8")

    first = await index_document(
        document_type="cv",
        source_path=str(source_file),
        text="Python FastAPI Docker Kubernetes",
    )

    second = await index_document(
        document_type="cv",
        source_path=str(source_file),
        text="Python FastAPI Docker Kubernetes",
    )

    assert first["status"] == "indexed"
    assert second["status"] == "already_indexed"
    assert first["file_hash"] == second["file_hash"]


@pytest.mark.asyncio
async def test_rag_search_returns_results(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    from app.rag.rag_pipeline import index_document, rag_search

    source_file = tmp_path / "ao.txt"
    source_file.write_text(
        "Nous recherchons un développeur Python avec expérience FastAPI",
        encoding="utf-8",
    )

    await index_document(
        document_type="ao",
        source_path=str(source_file),
        text="Nous recherchons un développeur Python avec expérience FastAPI",
    )

    results = await rag_search(
        query="développeur python fastapi",
        top_k=3,
        filters={"document_type": "ao"},
    )

    assert len(results) >= 1
    assert results[0]["metadata"]["document_type"] == "ao"
