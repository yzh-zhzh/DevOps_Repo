# Multi-target Dockerfile for Smart Fire Alert System
#
# Target 1: simulator (default) - runs anywhere, no Raspberry Pi hardware required
# Target 2: rpi (experimental) - arm64 base; intended for Raspberry Pi with camera/sensors
#
# Build examples:
#   docker build -f docker/Dockerfile -t <hub-user>/<repo>:sim --target simulator .
#   docker buildx build --platform linux/arm64 -f docker/Dockerfile -t <hub-user>/<repo>:rpi --target rpi .
#
# Run examples:
#   docker run --rm -p 5000:5000 <hub-user>/<repo>:sim
#   # For rpi, you may need --device and --privileged to access hardware

########################
# Target: simulator
########################
FROM python:3.11-slim AS simulator

WORKDIR /app

# System deps for Flask and numpy (no OpenCV)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy only what we need
COPY docker/simulator_app.py /app/simulator_app.py

# Python deps (minimal, no opencv)
RUN pip install --no-cache-dir Flask numpy

EXPOSE 5000
CMD ["python", "simulator_app.py"]

########################
# Target: rpi (experimental)
########################
FROM --platform=linux/arm64 python:3.11-slim AS rpi

WORKDIR /app

# Raspberry Pi specific system libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libcamera0 libcamera-tools \
    python3-libcamera python3-picamera2 \
    && rm -rf /var/lib/apt/lists/* || true

# Copy your project source
COPY src/ /app/

# Python deps (add more as needed, no opencv)
RUN pip install --no-cache-dir Flask numpy

# Expose Flask default port used in src/app.py
EXPOSE 5000

# Default command to start Flask app if available
# Change this if your entrypoint is different
CMD ["python", "app.py"]