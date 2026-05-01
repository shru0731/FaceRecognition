# Face Recognition on Raspberry Pi - Docker Guide

## Prerequisites

1. **Raspberry Pi** (Pi 4 or Pi 5 recommended for better performance)
2. **Raspberry Pi OS** (64-bit recommended)
3. **Camera module** or USB webcam

## Installation Steps

### 1. Install Docker on Raspberry Pi

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -sSL https://get.docker.com | sh

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again for group changes to take effect
```

### 2. Clone/Transfer Your Project

Copy your project folder to the Raspberry Pi:
```bash
scp -r Face_2 pi@<raspberry-pi-ip>:/home/pi/
```

### 3. Build and Run

```bash
cd /home/pi/Face_2

# Build the image
docker build -t face-recognition .

# Run the container
docker run --rm -it \
    --device /dev/video0:/dev/video0 \
    -v $(pwd)/dataset:/app/dataset \
    -v model-cache:/root/.deepface \
    face-recognition
```

**Or use docker-compose:**

```bash
docker-compose up --build
```

## Important Notes for Raspberry Pi

### Performance Optimization

1. **Use a smaller model** - Edit `recognition.py` to use "Facenet" instead of "ArcFace" for faster inference on Pi

2. **Reduce frame resolution** - The Dockerfile includes optimizations, but you may want to modify the recognition.py to process smaller frames

3. **First run is slow** - DeepFace downloads models on first run (~100MB+). Subsequent runs use cached models.

### Headless Operation

For running without a display (recommended for Pi):

1. Install virtual framebuffer:
```bash
sudo apt-get install -y xvfb
```

2. Run with virtual display:
```bash
xvfb-run -a docker run --rm -it \
    --device /dev/video0:/dev/video0 \
    -v $(pwd)/dataset:/app/dataset \
    face-recognition
```

### Camera Permissions

If the container can't access the camera:
```bash
sudo chmod 666 /dev/video0
```

## Building for ARM Architecture

If you're building on a non-ARM machine (x86_64) for Raspberry Pi:

```bash
# Build for ARM64
docker buildx build --platform linux/arm64 -t face-recognition:arm64 .

# Or use multi-arch build
docker buildx build --platform linux/arm64,linux/amd64 -t face-recognition:multi-arch .
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container exits immediately | Check if camera is connected: `ls /dev/video0` |
| "No module named cv2" | Rebuild container: `docker-compose build --no-cache` |
| Slow performance | Use smaller model, reduce frame size |
| Camera permission denied | `sudo chmod 666 /dev/video0` |
| Out of memory | Close other applications, use swap file |

## First Time Setup

1. **Capture faces** (on Pi with camera):
```bash
docker run --rm -it --device /dev/video0:/dev/video0 -v $(pwd)/dataset:/app/dataset face-recognition python3 capture.py
```

2. **Train the model**:
```bash
docker run --rm -it -v $(pwd)/dataset:/app/dataset face-recognition python3 train.py
```

3. **Run recognition**:
```bash
docker run --rm -it --device /dev/video0:/dev/video0 -v $(pwd)/dataset:/app/dataset face-recognition
```
