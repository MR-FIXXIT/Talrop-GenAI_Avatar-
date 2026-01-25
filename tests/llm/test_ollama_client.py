from unittest.mock import patch, AsyncMock
from llm.ollama_client import generate_llm_response


@patch("httpx.AsyncClient.post")
async def test_generate_llm_response(mock_post):
    mock_post.return_value.json = lambda: {"response": "Hello!"}
    mock_post.return_value.raise_for_status = lambda: None

    text = await generate_llm_response("Hello")
    assert isinstance(text, str)
    assert len(text) > 0
