from workers.celery_app import celery_app
from core.logging import get_logger
from tts.coqui_tts import synthesize_speech

logger = get_logger(__name__)


@celery_app.task(bind=True)
def tts_task(
    self,
    text: str,
    emotion: str = "neutral"
):
    try:
        logger.info("TTS worker started")
        audio_path = synthesize_speech.__wrapped__(
            text=text,
            emotion=emotion
        )
        return audio_path

    except Exception as e:
        logger.exception("TTS failed")
        self.retry(exc=e, countdown=5, max_retries=3)
