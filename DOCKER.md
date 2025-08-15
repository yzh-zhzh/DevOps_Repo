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

## Run

```bash
docker run --rm -p 5000:5000 <hub-user>/<repo>:sim
# open http://localhost:5000
```

For the `rpi` image, you may need device access and privileges to use camera/sensors on a Raspberry Pi:
```bash
docker run --rm -p 5000:5000 \
  --device /dev/video0 \
  --privileged \
  <hub-user>/<repo>:rpi
```

## Push to Docker Hub

```bash
docker login
docker tag <hub-user>/<repo>:sim <hub-user>/<repo>:latest
docker push <hub-user>/<repo>:sim
docker push <hub-user>/<repo>:rpi
docker push <hub-user>/<repo>:latest
```

> Replace `<hub-user>` and `<repo>` with your Docker Hub username and repository name.