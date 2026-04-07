import json
import os
from typing import Any, Dict, Optional


class CacheManager:

    def __init__(self):
        self.base_path = "app/cache"

        self.paths = {
            "parsed": os.path.join(self.base_path, "parsed"),
            "processed": os.path.join(self.base_path, "processed"),
            "extracted": os.path.join(self.base_path, "extracted"),
            "query": os.path.join(self.base_path, "query"),
        }

        # Création des dossiers
        for path in self.paths.values():
            os.makedirs(path, exist_ok=True)

    # =========================
    # Utils internes
    # =========================
    def _get_file_path(self, category: str, key: str) -> str:
        return os.path.join(self.paths[category], f"{key}.json")

    def _read_json(self, path: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # fichier corrompu -> on ignore
            return None

    def _write_json(self, path: str, data: Dict[str, Any]):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # =========================
    # PARSED (raw text)
    # =========================
    def get_parsed(self, file_hash: str):
        path = self._get_file_path("parsed", file_hash)
        return self._read_json(path)

    def set_parsed(self, file_hash: str, text: str):
        path = self._get_file_path("parsed", file_hash)
        self._write_json(path, {"text": text})

    # =========================
    # PROCESSED (text nettoyé + indexation)
    # =========================
    def get_processed(self, file_hash: str):
        path = self._get_file_path("processed", file_hash)
        return self._read_json(path)

    def set_processed(self, file_hash: str, data: Dict[str, Any]):
        path = self._get_file_path("processed", file_hash)
        self._write_json(path, data)

    # =========================
    # EXTRACTED (skills + tasks)
    # =========================
    def get_extracted(self, file_hash: str):
        path = self._get_file_path("extracted", file_hash)
        return self._read_json(path)

    def set_extracted(self, file_hash: str, data: Dict[str, Any]):
        path = self._get_file_path("extracted", file_hash)
        self._write_json(path, data)

    # =========================
    # QUERY (réponses LLM)
    # =========================
    def get_query(self, cache_key: str):
        path = self._get_file_path("query", cache_key)
        return self._read_json(path)

    def set_query(self, cache_key: str, data: Dict[str, Any]):
        path = self._get_file_path("query", cache_key)
        self._write_json(path, data)
