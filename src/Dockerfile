# Use Raspberry Pi OS Bullseye base image
FROM arm32v7/debian:bullseye-slim

# Add Raspberry Pi OS repository and keys
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add -
RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" >> /etc/apt/sources.list.d/raspi.list

# Install required packages (no RFID/SPI dependencies)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    v4l-utils \
    i2c-tools \
    python3-rpi.gpio \
    python3-smbus \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Script needs to run as root to access camera
USER root

# Command to run your main application
CMD ["python3", "main.py"]