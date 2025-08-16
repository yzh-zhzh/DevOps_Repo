# Containerizing Smart Fire Alert System

This repo contains two Docker build targets:

- `simulator` (default): portable image without Raspberry Pi hardware. It exposes `/data` and `/video_feed` endpoints for demo/testing.
- `rpi` (experimental): arm64 build intended for Raspberry Pi OS with camera/sensors and HAL available.

## Build

### Simulator (runs anywhere)
```bash
docker build -f docker/Dockerfile -t <hub-user>/<repo>:sim --target simulator .
```

### Raspberry Pi (arm64)
```bash
docker buildx create --use --name multi || true
docker buildx build --platform linux/arm64 -f docker/Dockerfile -t <hub-user>/<repo>:rpi --target rpi .
```
> Replace `<hub-user>` and `<repo>` with your Docker Hub username and repository name.

## Using Docker Compose

To build and run both services together:
```bash
docker-compose up --build
```
- The `website` service will be available on [http://localhost:5001](http://localhost:5001)
- If running on real Raspberry Pi hardware, uncomment the device mappings in `docker-compose.yml