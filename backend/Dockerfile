FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libgl1 libglib2.0-0 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /tmp/requirements.txt
COPY analytics/requirements.txt /tmp/analytics-requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt -r /tmp/analytics-requirements.txt
COPY backend /app/
COPY analytics /app/analytics/
COPY videos /app/videos/
COPY evidence /app/evidence/
COPY vision /app/vision/
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
