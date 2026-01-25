import asyncio

from llm.ollama_client import generate_llm_response
from avatar.image_generation import generate_avatar_image
from tts.coqui_tts import synthesize_speech


async def main():
    print("🔥 Warming up models...")

    await generate_llm_response("Hello")
    await synthesize_speech("Hello world", "neutral")
    await generate_avatar_image("tenant_123", "neutral")

    print("✅ Models warmed up")


if __name__ == "__main__":
    asyncio.run(main())
