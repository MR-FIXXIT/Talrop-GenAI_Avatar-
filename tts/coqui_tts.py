import os
import uuid
from TTS.api import TTS
from core.config import settings

_tts = None


def get_tts():
    global _tts
    if _tts is None:
        _tts = TTS(
            model_name=settings.TTS_MODEL,
            progress_bar=False,
            gpu=False,  # CPU-safe
        )
    return _tts


async def synthesize_speech(
    text: str,
    output_path: str | None = None,
    speaker: str | None = None,
    emotion: str | None = None,
):
    """
    Generate speech audio file from text.
    """

    tts = get_tts()

    # Default speaker for multi-speaker models
    if speaker is None:
        speaker = "p225"

    # 🔑 Auto-generate output path if missing
    if output_path is None:
        filename = f"{uuid.uuid4()}.wav"
        output_path = os.path.join(
            settings.AUDIO_OUTPUT_DIR,
            filename,
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker=speaker,
    )

    return output_path
