# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for hardware access (Raspberry Pi example)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    python3-rpi.gpio \
    libffi-dev \
    libssl-dev \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies if requirements.txt exists
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory contents into the container at /app
COPY src/ ./

# Run main.py when the container launches
CMD ["python", "main.py"]