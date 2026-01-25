import re

MAX_SENTENCE_LENGTH = 200

def enforce_spoken_style(text: str) -> str:
    """
    Ensures short, spoken-style output for avatar lip-sync.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    cleaned = []

    for s in sentences:
        s = s.strip()
        if len(s) > MAX_SENTENCE_LENGTH:
            s = s[:MAX_SENTENCE_LENGTH] + "..."
        cleaned.append(s)

    return " ".join(cleaned)

def remove_multiple_emotions(text: str) -> str:
    """
    Keeps only the first emotion tag if multiple exist.
    """
    matches = re.findall(r"\[emotion:[^\]]+\]", text)
    if len(matches) <= 1:
        return text

    first = matches[0]
    text = re.sub(r"\[emotion:[^\]]+\]", "", text)
    return f"{text.strip()} {first}"
