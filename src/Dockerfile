
# Use official ARMv7 Python image for Raspberry Pi compatibility
FROM arm32v7/python:3.11

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and picamera2
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
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (except picamera2, which is installed via apt)
COPY requirements.txt ./
RUN grep -v '^picamera2' requirements.txt > requirements_nocam.txt && \
    pip3 install --no-cache-dir -r requirements_nocam.txt && rm requirements_nocam.txt


# Copy all files from the build context (src/) into the container at /app
COPY . ./

# Add hal directory to PYTHONPATH so 'import spi' works in Docker

# Compatibility shim: make 'smbus' importable as 'smbus2'
RUN ln -s /usr/local/lib/python3.11/site-packages/smbus2 /usr/local/lib/python3.11/site-packages/smbus || true

ENV PYTHONPATH="/app/hal:${PYTHONPATH}"

# Run main.py when the container launches
CMD ["python3", "main.py"]