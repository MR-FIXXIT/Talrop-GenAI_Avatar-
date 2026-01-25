FROM python:3.10-bullseye

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    git \
    curl \
    wget \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Python tooling
# =========================
RUN python -m pip install --upgrade pip setuptools wheel

# =========================
# NumPy (TTS compatibility)
# =========================
RUN pip install numpy==1.22.0

# =========================
# Coqui TTS
# =========================
RUN pip install TTS==0.22.0 --no-cache-dir

# Verify TTS install
RUN python - <<EOF
from TTS.api import TTS
print("TTS INSTALLED SUCCESSFULLY")
EOF

# =========================
# SadTalker setup
# =========================

# Clone SadTalker repository
RUN git clone https://github.com/OpenTalker/SadTalker.git /app/SadTalker

# Install SadTalker Python dependencies
RUN pip install -r /app/SadTalker/requirements.txt

# Download SadTalker checkpoints (OFFICIAL METHOD)
RUN cd /app/SadTalker && \
    python scripts/download_models.py

# =========================
# Project dependencies
# =========================
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# =========================
# Project source
# =========================
COPY . .
ENV PYTHONPATH=/app

# =========================
# Run API
# =========================
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
