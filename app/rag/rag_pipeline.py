from app.rag.embeddings import embed
from app.rag.vector_store import search_vectors, store_vector
from app.utils.text_chunker import chunk_text


async def rag_store(text: str, metadata: dict):
    vector = embed(text)
    store_vector(vector, metadata)


async def index_document(
    document_id: str, document_type: str, source_path: str, text: str
):
    chunks = chunk_text(text)

    for idx, chunk in enumerate(chunks):
        await rag_store(
            text=chunk,
            metadata={
                "entity_type": "document_chunk",
                "document_id": document_id,
                "document_type": document_type,
                "source_path": source_path,
                "chunk_index": idx,
                "chunk_text": chunk,
            },
        )

    return {
        "document_id": document_id,
        "document_type": document_type,
        "chunks_indexed": len(chunks),
    }


async def rag_search(query: str, top_k: int = 5, filters: dict | None = None):
    vector = embed(query)
    return search_vectors(vector, top_k=top_k, filters=filters)
