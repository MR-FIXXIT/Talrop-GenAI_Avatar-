import subprocess
import sys
from pathlib import Path

SADTALKER_DIR = Path("/app/SadTalker")
PROJECT_ROOT = Path("/app")


def generate_avatar_video(
    image_path: str,
    audio_path: str,
    output_dir: str,
):
    output_dir = PROJECT_ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    image_path = PROJECT_ROOT / image_path
    audio_path = PROJECT_ROOT / audio_path

    cmd = [
        sys.executable,
        str(SADTALKER_DIR / "inference.py"),
        "--driven_audio", str(audio_path),
        "--source_image", str(image_path),
        "--result_dir", str(output_dir),
        "--checkpoint_dir", str(SADTALKER_DIR / "checkpoints"),
        "--still",
        "--preprocess", "full",
    ]

    subprocess.run(cmd, check=True)

    return str(output_dir)
