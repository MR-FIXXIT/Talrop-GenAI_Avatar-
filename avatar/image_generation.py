import os
import uuid
import torch
from diffusers import StableDiffusionPipeline

from core.config import settings
from core.logging import get_logger
from avatar.identity.lora_manager import load_lora

logger = get_logger(__name__)

_PIPELINE = None


def _get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def _load_pipeline():
    """
    Loads Stable Diffusion and applies LoRA ONCE.
    """
    global _PIPELINE

    if _PIPELINE is not None:
        return _PIPELINE

    logger.info("Loading Stable Diffusion pipeline")
    device = _get_device()

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        safety_checker=None,   # recommended for avatars
    )

    pipe = pipe.to(device)
    pipe.enable_attention_slicing()

    # 🔥 APPLY YOUR TRAINED LORA HERE
    if settings.LORA_PATH:
        if not os.path.exists(settings.LORA_PATH):
            raise FileNotFoundError(
                f"LoRA file not found: {settings.LORA_PATH}"
            )

        logger.info(
            f"Applying LoRA: {settings.LORA_PATH} "
            f"(scale={settings.LORA_SCALE})"
        )

        load_lora(
            pipe=pipe,
            lora_path=settings.LORA_PATH,
            scale=settings.LORA_SCALE
        )

    _PIPELINE = pipe
    logger.info("Stable Diffusion pipeline ready")

    return _PIPELINE


def _output_path() -> str:
    os.makedirs(settings.IMAGE_OUTPUT_DIR, exist_ok=True)
    return os.path.join(
        settings.IMAGE_OUTPUT_DIR,
        f"{uuid.uuid4()}.png"
    )


async def generate_avatar_image(
    tenant_id: str,
    emotion: str = "neutral"
) -> str:
    """
    Generates a LoRA-consistent avatar image.
    """
    pipe = _load_pipeline()

    prompt = (
        "high quality portrait photo of a person, "
        "sharp focus, professional studio lighting, "
        "clean background, ultra realistic, "
        f"emotion: {emotion}, looking at camera"
    )

    negative_prompt = (
        "blurry, low quality, distorted face, extra limbs, "
        "deformed eyes, bad anatomy"
    )

    logger.info(
        f"Generating avatar image | tenant={tenant_id} | emotion={emotion}"
    )

    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=30,
        guidance_scale=7.5,
        height=settings.AVATAR_IMAGE_SIZE,
        width=settings.AVATAR_IMAGE_SIZE,
    ).images[0]

    path = _output_path()
    image.save(path)

    return path
