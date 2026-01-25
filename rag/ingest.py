from rag.chunker import chunk_text
from rag.embeddings import embed_texts
from rag.vector_store import load_index, save_index
from core.logging import get_logger

logger = get_logger(__name__)

async def ingest_document(
    tenant_id: str,
    text: str,
    source: str = "uploaded"
):
    logger.info(f"Ingesting document | tenant={tenant_id}")

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    index, metadata = load_index(tenant_id)

    index.add_embeddings(embeddings)
    for chunk in chunks:
        metadata.append({
            "text": chunk,
            "source": source
        })

    save_index(tenant_id, index, metadata)
