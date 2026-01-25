import httpx
from core.config import settings


async def generate_llm_response(prompt: str) -> str:
    """
    Generate a response from Ollama.
    """

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

    return data.get("response", "")
