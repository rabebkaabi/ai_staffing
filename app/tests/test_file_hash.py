from pathlib import Path

from app.utils.file_hash import compute_file_hash


def test_compute_file_hash_same_content_same_hash(tmp_path: Path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("hello world", encoding="utf-8")
    file2.write_text("hello world", encoding="utf-8")

    hash1 = compute_file_hash(str(file1))
    hash2 = compute_file_hash(str(file2))

    assert hash1 == hash2


def test_compute_file_hash_different_content_different_hash(tmp_path: Path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("hello world", encoding="utf-8")
    file2.write_text("hello world!!!", encoding="utf-8")

    hash1 = compute_file_hash(str(file1))
    hash2 = compute_file_hash(str(file2))

    assert hash1 != hash2