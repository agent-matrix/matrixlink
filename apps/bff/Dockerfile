FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    CLOUD_PROVIDER=local

WORKDIR /app

# Optional: handy tools for probes/debug
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates tzdata \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/

EXPOSE 8080
CMD ["uvicorn","app.main:app","--host=0.0.0.0","--port=8080","--proxy-headers"]
