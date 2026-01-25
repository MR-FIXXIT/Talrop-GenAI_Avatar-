EMOTION_TO_STYLE = {
    "neutral": {"pose": 0.5},
    "happy": {"pose": 0.8},
    "sad": {"pose": 0.3},
    "angry": {"pose": 0.7},
    "surprised": {"pose": 0.9},
    "calm": {"pose": 0.4}
}

def get_expression_params(emotion: str) -> dict:
    return EMOTION_TO_STYLE.get(emotion, EMOTION_TO_STYLE["neutral"])
