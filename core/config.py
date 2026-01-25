import os
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Central configuration for the Avatar Chatbot API.
    Loaded from environment variables with sane defaults for Docker.
    """

    # =========================
    # APP
    # =========================
    APP_NAME: str = "avatar-chatbot-api"
    ENV: str = Field(default="development")

    # =========================
    # SECURITY / AUTH
    # =========================
    API_KEY: str = Field(default="dev-key")

    # =========================
    # REDIS (Short-term memory)
    # IMPORTANT: use service name, NOT localhost
    # =========================
    REDIS_URL: str = Field(
        default="redis://redis:6379",
        description="Redis connection URL (Docker service name)",
    )

    # =========================
    # DATABASE (Long-term memory)
    # =========================
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/avatar",
    )

    # =========================
    # LLM (Ollama)
    # =========================
    OLLAMA_BASE_URL: str = Field(
        default="http://host.docker.internal:11434",
        description="Ollama API URL",
    )
    OLLAMA_MODEL: str = Field(default="gemma:2b")

    # =========================
    # RAG
    # =========================
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2"
    )
    VECTOR_STORE_PATH: str = Field(default="./storage/vector_store")

    # =========================
    # TTS (Coqui)
    # =========================
    TTS_MODEL: str = Field(
        default="tts_models/en/vctk/vits",
        description="Coqui TTS model name",
    )
    TTS_SAMPLE_RATE: int = 22050

    # =========================
    # AVATAR / DIFFUSION
    # =========================
    SD_MODEL_ID: str = Field(
        default="runwayml/stable-diffusion-v1-5"
    )
    LORA_PATH: str = Field(
        default="./avatar/lora/LoRATrainedModel.safetensors"
    )
    LORA_SCALE: float = 1.0
    
    AVATAR_IMAGE_SIZE: int = 512
    AVATAR_INFERENCE_STEPS: int = 30
    AVATAR_GUIDANCE_SCALE: float = 7.5
    AVATAR_SEED: int | None = None
    # =========================
    # STORAGE PATHS
    # =========================
    AUDIO_OUTPUT_DIR: str = Field(default="./storage/audio")
    IMAGE_OUTPUT_DIR: str = Field(default="./storage/images")
    VIDEO_OUTPUT_DIR: str = Field(default="./storage/videos")

    # =========================
    # WORKERS / CELERY
    # =========================
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/1")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()


# Export a singleton-style object for easy imports
settings = get_settings()
