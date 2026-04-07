from pathlib import Path

from google.adk import Agent
from pydantic import PrivateAttr

from app.rag.rag_pipeline import index_document
from app.utils.cache_manager import CacheManager
from app.utils.docx_parser import parse_docx
from app.utils.file_hash import compute_file_hash
from app.utils.pdf_parser import parse_pdf
from app.utils.text_cleaner import clean_text
from app.utils.txt_parser import parse_txt
from app.utils.xlsx_parser import parse_xlsx


class DocumentProcessingAgent(Agent):
    name: str = "document_processing_agent"

    _cache: CacheManager = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cache = CacheManager()

    async def run(self, file_path: str, document_type: str):
        file_hash = compute_file_hash(file_path)
        cached = self._cache.get_processed(file_hash)

        if cached:
            return {
                "text": cached["text"],
                "indexation": {
                    "document_id": f"{document_type}::{file_path}",
                    "document_type": document_type,
                    "status": "already_indexed_from_cache",
                },
                "cache": "hit",
            }

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            raw_text = parse_pdf(file_path)
        elif extension == ".docx":
            raw_text = parse_docx(file_path)
        elif extension in [".xlsx", ".xls"]:
            raw_text = parse_xlsx(file_path)
        elif extension == ".txt":
            raw_text = parse_txt(file_path)
        else:
            raise ValueError(f"Format non supporté: {extension}")

        text = clean_text(raw_text)

        if not text or not text.strip():
            raise ValueError(f"Document vide ou illisible: {file_path}")

        index_result = await index_document(
            document_id=f"{document_type}::{file_path}",
            document_type=document_type,
            source_path=file_path,
            text=text,
        )

        self._cache.set_processed(file_hash, {"text": text})

        return {"text": text, "indexation": index_result, "cache": "miss"}
