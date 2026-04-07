import hashlib

import numpy as np

EMBEDDING_DIM = 128


def _token_to_vector(token: str) -> np.ndarray:
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    values = np.frombuffer(digest, dtype=np.uint8).astype(np.float32)

    repeated = np.resize(values, EMBEDDING_DIM)

    return repeated / 255.0


def embed(text: str) -> np.ndarray:
    if not text or not text.strip():
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)

    tokens = text.split()

    vectors = [_token_to_vector(token.lower()) for token in tokens]

    return np.mean(vectors, axis=0).astype(np.float32)
