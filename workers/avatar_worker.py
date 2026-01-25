from workers.celery_app import celery_app
from core.logging import get_logger
from avatar.image_generation import generate_avatar_image
from avatar.video_generation import generate_avatar_video
from tts.coqui_tts import synthesize_speech

logger = get_logger(__name__)


@celery_app.task(bind=True)
def generate_avatar_video_task(
    self,
    tenant_id: str,
    text: str,
    emotion: str = "neutral"
):
    """
    Full avatar pipeline (GPU-heavy).
    """
    try:
        logger.info(
            f"Avatar worker started | tenant={tenant_id}"
        )

        # 1. TTS
        audio_path = synthesize_speech.__wrapped__(
            text=text,
            emotion=emotion
        )

        # 2. Image generation
        image_path = generate_avatar_image.__wrapped__(
            tenant_id=tenant_id,
            emotion=emotion
        )

        # 3. Video generation
        video_path = generate_avatar_video.__wrapped__(
            image_path=image_path,
            audio_path=audio_path,
            emotion=emotion
        )

        return {
            "video_path": video_path,
            "status": "completed"
        }

    except Exception as e:
        logger.exception("Avatar generation failed")
        self.retry(exc=e, countdown=10, max_retries=3)
