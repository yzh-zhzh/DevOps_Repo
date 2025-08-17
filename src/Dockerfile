
# Use official ARMv7 Python image for Raspberry Pi compatibility
FROM arm32v7/python:3.11

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and multimedia libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    python3-spidev \
    python3-rpi.gpio \
    python3-smbus \
    python3-smbus2 \
    libffi-dev \
    libssl-dev \
    build-essential \
    gcc \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libopenjp2-7 \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libilmbase-dev \
    libraw-dev \
    libwebp-dev \
    libx264-dev \
    libx265-dev \
    python3-virtualenv \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with better error handling
COPY requirements.txt ./

# Create a virtual environment to satisfy the av package requirement
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies in order of complexity (simple ones first)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir requests && \
    pip install --no-cache-dir flask && \
    pip install --no-cache-dir smbus2 && \
    pip install --no-cache-dir RPi.GPIO && \
    pip install --no-cache-dir spidev

# Try to install picamera2, but don't fail the build if it doesn't work
RUN pip install --no-cache-dir picamera2 || echo "Warning: picamera2 installation failed, continuing without it"


# Copy all files from the build context (src/) into the container at /app
COPY . ./

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app/hal:${PYTHONPATH}"

# Compatibility shim: make 'smbus' importable as 'smbus2' (if needed)
RUN ln -sf /opt/venv/lib/python3.11/site-packages/smbus2 /opt/venv/lib/python3.11/site-packages/smbus || true

# Run main.py when the container launches
CMD ["/opt/venv/bin/python", "main.py"]