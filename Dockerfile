# Markdowner — Hugging Face Spaces (Docker SDK)
FROM python:3.11-slim

# System dependency: ffmpeg enables markitdown's audio/video transcription.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY . .

# Hugging Face Spaces routes traffic to port 7860.
ENV PORT=7860
EXPOSE 7860

# 2 workers; long timeout so large file conversions are not killed mid-request.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120"]
