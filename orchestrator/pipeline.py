from core.logging import get_logger
from core.constants import SYSTEM_PROMPT, EMOTIONS
from llm.ollama_client import generate_llm_response
from rag.retriever import retrieve_context
from web_search.query_router import maybe_search_web
from memory.redis_short_term import get_short_term_memory, save_short_term_memory
from tts.coqui_tts import synthesize_speech
from avatar.image_generation import generate_avatar_image
from avatar.video_generation import generate_avatar_video
from orchestrator.emotion_parser import extract_emotion
from orchestrator.response_formatter import format_for_avatar

logger = get_logger(__name__)

async def run_pipeline(
    tenant_id: str,
    message: str,
    session_id: str | None = None
):
    logger.info(f"Pipeline start | tenant={tenant_id}")

    # 1. Load conversation memory
    memory = await get_short_term_memory(tenant_id, session_id)

    # 2. Retrieve RAG context
    rag_context = await retrieve_context(tenant_id, message)

    # 3. Optional web search
    web_context = await maybe_search_web(message)

    # 4. Build final prompt
    prompt = format_for_avatar(
        system_prompt=SYSTEM_PROMPT,
        memory=memory,
        rag_context=rag_context,
        web_context=web_context,
        user_message=message
    )

    # 5. LLM inference
    llm_output = await generate_llm_response(prompt)

    # 6. Emotion extraction
    emotion = extract_emotion(llm_output)

    # 7. Save memory
    await save_short_term_memory(
        tenant_id=tenant_id,
        session_id=session_id,
        user_message=message,
        assistant_message=llm_output
    )

    # 8. TTS
    audio_path = await synthesize_speech(
        text=llm_output,
        emotion=emotion
    )

    # 9. Avatar image
    avatar_image_path = await generate_avatar_image(
        tenant_id=tenant_id,
        emotion=emotion
    )

    # 10. Avatar video
    video_path = generate_avatar_video(
        image_path=avatar_image_path,
        audio_path=audio_path,
        output_dir="storage/videos",
    )

    logger.info("Pipeline complete")

    return {
        "text": llm_output,
        "emotion": emotion,
        "video_url": video_path
    }
