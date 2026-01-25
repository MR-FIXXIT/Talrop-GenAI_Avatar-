# Emotion tags used across LLM → Avatar → Video
EMOTIONS = [
    "neutral",
    "happy",
    "sad",
    "angry",
    "surprised",
    "calm"
]

# Default system prompt
SYSTEM_PROMPT = (
    "You are a real-time talking avatar. "
    "Respond with short, spoken-style sentences. "
    "Avoid long explanations."
)

# Rate limits
DEFAULT_RATE_LIMIT_PER_MINUTE = 60

# File formats
AUDIO_FORMAT = "wav"
VIDEO_FORMAT = "mp4"
