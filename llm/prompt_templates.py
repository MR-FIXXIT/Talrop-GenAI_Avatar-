from core.constants import SYSTEM_PROMPT

def base_avatar_prompt() -> str:
    return SYSTEM_PROMPT

def emotion_instruction() -> str:
    return (
        "Include at most one emotion tag in the format "
        "[emotion: happy | sad | angry | surprised | calm | neutral]."
    )

def safety_instruction() -> str:
    return (
        "Do not provide medical, legal, or financial advice. "
        "Decline unsafe requests politely."
    )
