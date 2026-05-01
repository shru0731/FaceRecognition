# Dockerfile for Face Recognition - Raspberry Pi 3 (ARM v7)
# Uses bullseye base to avoid newer Debian package naming issues

# FROM arm32v7/python:3.9-slim-bullseye  # ARMv7 (Raspberry Pi 3)
# AMD64 (PC/Laptop)
FROM python:3.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /app

# Install system deps - bullseye has the old/stable package names
RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
#COPY capture.py train.py train_proper.py recognition.py recognition_headless.py ./
COPY capture.py train.py train_proper.py recognition.py recognition_headless.py ./
COPY dataset/ ./dataset/

RUN mkdir -p /root/.deepface

VOLUME ["/root/.deepface", "/app/dataset"]

CMD ["python3", "recognition_headless.py"]
