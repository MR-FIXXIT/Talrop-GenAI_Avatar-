import httpx
from core.logging import get_logger

logger = get_logger(__name__)

# Example: http://localhost:8080
SEARXNG_BASE_URL = "http://localhost:8080"

async def searxng_search(
    query: str,
    max_results: int = 5
) -> str | None:
    """
    Queries SearXNG and returns summarized text results.
    """
    params = {
        "q": query,
        "format": "json",
        "language": "en",
        "categories": "general"
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{SEARXNG_BASE_URL}/search",
                params=params
            )
            resp.raise_for_status()
            data = resp.json()

        results = data.get("results", [])[:max_results]
        if not results:
            return None

        summaries = []
        for r in results:
            title = r.get("title", "")
            content = r.get("content", "")
            summaries.append(f"{title}: {content}")

        return "\n".join(summaries)

    except Exception as e:
        logger.warning(f"SearXNG search failed: {e}")
        return None
