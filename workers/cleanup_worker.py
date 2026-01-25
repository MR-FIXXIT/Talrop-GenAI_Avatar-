import os
import time
from workers.celery_app import celery_app
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)

MAX_AGE_SECONDS = 24 * 60 * 60  # 24 hours


@celery_app.task
def cleanup_old_files():
    """
    Deletes old generated files to save disk space.
    """
    now = time.time()

    for directory in [
        settings.IMAGE_OUTPUT_DIR,
        settings.VIDEO_OUTPUT_DIR,
        settings.AUDIO_OUTPUT_DIR,
    ]:
        if not os.path.exists(directory):
            continue

        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isfile(path):
                if now - os.path.getmtime(path) > MAX_AGE_SECONDS:
                    os.remove(path)
                    logger.info(f"Deleted old file: {path}")
