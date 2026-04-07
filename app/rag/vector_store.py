import json
import os
from typing import Any

import numpy as np

VECTOR_FILE = "app/storage/embeddings/vectors.json"


def _ensure_store():
    os.makedirs("app/storage/embeddings", exist_ok=True)

    if not os.path.exists(VECTOR_FILE):
        with open(VECTOR_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def _load_store():
    _ensure_store()

    with open(VECTOR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_store(data):
    with open(VECTOR_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def store_vector(vector: np.ndarray, metadata: dict[str, Any]):
    data = _load_store()

    data.append(
        {
            "vector": vector.tolist(),
            "metadata": metadata,
        }
    )

    _save_store(data)


def search_vectors(
    query_vector: np.ndarray, top_k: int = 5, filters: dict[str, Any] | None = None
):
    data = _load_store()

    if not data:
        return []

    scored = []
    query_norm = np.linalg.norm(query_vector)

    for item in data:
        metadata = item.get("metadata", {})

        if filters:
            skip = False
            for key, value in filters.items():
                if value is not None and metadata.get(key) != value:
                    skip = True
                    break
            if skip:
                continue

        stored_vector = np.array(item["vector"], dtype=np.float32)

        denom = query_norm * np.linalg.norm(stored_vector)
        similarity = (
            0.0 if denom == 0 else float(np.dot(query_vector, stored_vector) / denom)
        )

        scored.append(
            {
                "score": similarity,
                "metadata": metadata,
                "vector": item["vector"],
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]
