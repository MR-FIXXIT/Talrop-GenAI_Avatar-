from core.constants import EMOTIONS

def extract_emotion(text: str) -> str:
    """
    Looks for emotion tags like:
    [emotion: happy]
    """
    text_lower = text.lower()

    for emotion in EMOTIONS:
        if f"[emotion:{emotion}]" in text_lower:
            return emotion

    return "neutral"
