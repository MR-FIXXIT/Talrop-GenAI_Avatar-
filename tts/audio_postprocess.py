import librosa
import soundfile as sf

def normalize_audio(
    input_path: str,
    output_path: str | None = None
) -> str:
    """
    Normalizes audio loudness for better lip-sync.
    """
    y, sr = librosa.load(input_path, sr=None)
    y = librosa.util.normalize(y)

    out = output_path or input_path
    sf.write(out, y, sr)

    return out
