from rag.embeddings import embed_texts
from rag.vector_store import load_index, save_index

async def store_semantic_memory(
    tenant_id: str,
    text: str,
    source: str = "conversation"
):
    embeddings = embed_texts([text])
    index, metadata = load_index(tenant_id)

    import numpy as np
    index.add(np.array(embeddings).astype("float32"))
    metadata.append({
        "text": text,
        "source": source
    })

    save_index(tenant_id, index, metadata)
