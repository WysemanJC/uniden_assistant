FROM node:20-bookworm-slim AS frontend-build

WORKDIR /workspace/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
ENV VITE_API_URL=/api
RUN npm run build

FROM python:3.11-slim AS python-deps

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY backend/requirements.txt ./backend/requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libssl-dev \
    && pip install --upgrade pip \
    && pip install -r backend/requirements.txt \
    && apt-get purge -y --auto-remove build-essential libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=uniden_assistant.settings
ENV PYTHONPATH=/app/backend
ENV UNIDEN_DATA_DIR=/data/uniden_assistant
ENV UNIDEN_DB_DIR=/data/uniden_assistant/db
ENV MEDIA_ROOT=/data/uniden_assistant/media
ENV STATIC_ROOT=/app/staticfiles

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=python-deps /usr/local /usr/local
COPY backend/ /app/backend/
COPY --from=frontend-build /workspace/frontend/dist/ /usr/share/nginx/html/
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && mkdir -p /data/uniden_assistant/db /data/uniden_assistant/media /app/staticfiles

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]