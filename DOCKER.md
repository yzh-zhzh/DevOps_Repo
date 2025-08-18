# Containerizing Smart Fire Alert System

This repo contains two Docker build targets:

- `hardware` (src/main.py): for hardware system functions; initialise all hardware components.
- `website` (website/app.py): hosts a website that provides a web-interface for users.

## Build

### Hardware
```bash
docker pull yzhzh09/smart-fire-alert-hardware:latest2
docker run --privileged yzhzh09/smart-fire-alert-hardware:latest2
```

### Website
```bash
docker pull yzhzh09/smart-fire-alert-website:latest
docker run --privileged -p 5000:5000 yzhzh09/smart-fire-alert-website:latest
```

## Using Docker Compose

To build and run both services together:
```bash
docker-compose up --build
```
- The `website` service will be available on the Raspberry Pi IP Address
