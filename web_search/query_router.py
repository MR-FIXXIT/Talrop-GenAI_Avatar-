from web_search.searxng_client import searxng_search

TRIGGER_KEYWORDS = [
    "today",
    "latest",
    "current",
    "news",
    "price",
    "release",
    "version",
    "weather",
    "stock",
    "score"
]

async def maybe_search_web(user_message: str) -> str | None:
    """
    Runs web search only if the query likely needs fresh info.
    """
    lowered = user_message.lower()

    if any(keyword in lowered for keyword in TRIGGER_KEYWORDS):
        return await searxng_search(user_message)

    return None
