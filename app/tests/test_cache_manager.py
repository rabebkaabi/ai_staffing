import os
from pathlib import Path

from app.utils.cache_manager import CacheManager


def test_cache_manager_set_get_processed(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    cache = CacheManager()
    payload = {"text": "document nettoyé"}

    cache.set_processed("abc123", payload)
    result = cache.get_processed("abc123")

    assert result == payload


def test_cache_manager_set_get_extracted(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    cache = CacheManager()
    payload = {
        "text": "cv text",
        "skills": [{"name": "Python", "type": "technical", "family": "MOE"}],
        "tasks": {"tasks": ["Développer une API"]},
    }

    cache.set_extracted("hash001", payload)
    result = cache.get_extracted("hash001")

    assert result == payload


def test_cache_manager_missing_key_returns_none(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    cache = CacheManager()
    result = cache.get_processed("unknown")

    assert result is None


def test_cache_manager_creates_directories(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    CacheManager()

    assert os.path.isdir("app/cache/parsed")
    assert os.path.isdir("app/cache/processed")
    assert os.path.isdir("app/cache/extracted")
    assert os.path.isdir("app/cache/query")
