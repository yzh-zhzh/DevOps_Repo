
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for camera and GPIO (Raspberry Pi)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-rpi.gpio \
    libffi-dev \
    libssl-dev \
    build-essential \
    gcc \
    libjpeg-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libfontconfig1 \
    libdbus-1-3 \
    libglib2.0-0t64 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies if requirements.txt exists
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the website_integrated directory contents into the container at /app
COPY website_integrated/ ./

# Expose port 5000 for Flask
EXPOSE 5000

USER root

# Run app.py when the container launches
CMD ["python", "app.py"]
