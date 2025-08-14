# --- Stage 1: Python backend ---
FROM python:3.11-slim AS backend

# Set workdir
WORKDIR /app

# Copy Python backend
COPY src/ /app/

# --- Stage 2: Final image with backend + frontend ---
FROM python:3.11-slim

# Install a simple web server tool for static files
RUN pip install --no-cache-dir flask

WORKDIR /app

# Copy backend from build stage
COPY --from=backend /app /app

# Copy frontend (assuming in 'website' folder at repo root)
COPY website/ /app/static/

# Expose port (change if different)
EXPOSE 8000

# Command: run main.py
CMD ["python", "main.py"]