from unittest.mock import patch
from rag.retriever import retrieve_context


async def test_retrieve_context_empty():
    with patch("rag.vector_store.load_index") as mock_load:
        mock_load.return_value = (type("I", (), {"ntotal": 0})(), [])

        result = await retrieve_context("tenant_123", "test query")
        assert result is None
