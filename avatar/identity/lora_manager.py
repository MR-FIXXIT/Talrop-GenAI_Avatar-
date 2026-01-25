import torch
from core.logging import get_logger

logger = get_logger(__name__)

def load_lora(pipe, lora_path: str, scale: float = 1.0):
    """
    Applies LoRA weights to Stable Diffusion pipeline.
    """
    logger.info(f"Loading LoRA from {lora_path}")
    pipe.load_lora_weights(lora_path)
    pipe.fuse_lora(lora_scale=scale)
