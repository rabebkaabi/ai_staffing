import hashlib


def compute_file_hash(file_path: str) -> str:
    """
    Génère un hash SHA256 d'un fichier.
    Utilisé pour identifier si un document a déjà été traité.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha256.update(chunk)

    return sha256.hexdigest()
