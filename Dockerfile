FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UZIX_API_HOST=0.0.0.0 \
    UZIX_API_PORT=5000 \
    UZIX_LOG_LEVEL=INFO \
    UZIX_JSON_LOGS=true \
    UZIX_WARMUP_MODEL=true

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -e . && python detector/ml_model.py

EXPOSE 5000

CMD ["uzix-serve"]
