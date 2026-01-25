import numpy as np
from rag.embeddings import embed_query
from rag.vector_store import load_index
from core.logging import get_logger

logger = get_logger(__name__)

async def retrieve_context(
    tenant_id: str,
    query: str,
    top_k: int = 4
) -> str | None:
    index, metadata = load_index(tenant_id)

    if index.ntotal == 0:
        return None

    query_vec = np.array([embed_query(query)]).astype("float32")
    scores, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx]["text"])

    if not results:
        return None

    return "\n".join(results)
