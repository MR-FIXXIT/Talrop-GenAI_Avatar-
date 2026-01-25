import os
import faiss
import pickle
from core.config import settings

DIMENSION = 384  # all-MiniLM-L6-v2

def _tenant_path(tenant_id: str) -> str:
    path = os.path.join(settings.VECTOR_STORE_PATH, tenant_id)
    os.makedirs(path, exist_ok=True)
    return path

def load_index(tenant_id: str):
    path = _tenant_path(tenant_id)
    index_path = os.path.join(path, "index.faiss")
    meta_path = os.path.join(path, "meta.pkl")

    if not os.path.exists(index_path):
        index = faiss.IndexFlatIP(DIMENSION)
        metadata = []
        return index, metadata

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata

def save_index(tenant_id: str, index, metadata):
    path = _tenant_path(tenant_id)
    faiss.write_index(index, os.path.join(path, "index.faiss"))
    with open(os.path.join(path, "meta.pkl"), "wb") as f:
        pickle.dump(metadata, f)
