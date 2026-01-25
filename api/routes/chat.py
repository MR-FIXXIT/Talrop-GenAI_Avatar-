from fastapi import APIRouter, Depends
from api.schemas.chat import ChatRequest, ChatResponse
from api.middleware.auth_middleware import require_api_key
from orchestrator.pipeline import run_pipeline

router = APIRouter()

@router.post("/avatar", response_model=ChatResponse)
async def chat_with_avatar(
    payload: ChatRequest,
    tenant=Depends(require_api_key)
):
    """
    Main avatar chat endpoint
    """
    result = await run_pipeline(
        tenant_id=tenant.id,
        message=payload.message,
        session_id=payload.session_id
    )

    return ChatResponse(
        text=result["text"],
        emotion=result["emotion"],
        video_url=result["video_url"]
    )
