from sentence_transformers import SentenceTransformer
from core.logging import get_logger

logger = get_logger(__name__)

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        logger.info("Loading embedding model")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True).tolist()

def embed_query(text: str) -> list[float]:
    model = get_embedding_model()
    return model.encode(text, normalize_embeddings=True).tolist()
