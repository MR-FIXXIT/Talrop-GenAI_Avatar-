import json
import redis.asyncio as redis
from core.config import settings

_redis = None


def _make_key(tenant_id: str, session_id: str) -> str:
    return f"memory:{tenant_id}:{session_id}"


async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis


async def get_short_term_memory(tenant_id: str, session_id: str):
    """
    Retrieve conversation memory for a session.
    """
    r = await get_redis()
    key = _make_key(tenant_id, session_id)
    data = await r.get(key)
    return json.loads(data) if data else []


async def save_short_term_memory(
    tenant_id: str,
    session_id: str,
    user_message: str,
    assistant_message: str,
    ttl: int = 3600,
):
    """
    Append a turn to short-term memory.
    """
    r = await get_redis()
    key = _make_key(tenant_id, session_id)

    existing = await r.get(key)
    history = json.loads(existing) if existing else []

    history.append(
        {
            "user": user_message,
            "assistant": assistant_message,
        }
    )

    await r.set(key, json.dumps(history), ex=ttl)
