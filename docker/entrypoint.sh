#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/app/backend"
DATA_DIR="${UNIDEN_DATA_DIR:-/data/uniden_assistant}"
DB_DIR="${UNIDEN_DB_DIR:-${DATA_DIR}/db}"
MEDIA_DIR="${MEDIA_ROOT:-${DATA_DIR}/media}"
STATIC_DIR="${STATIC_ROOT:-/app/staticfiles}"

# Read version from build artifact (if exists)
if [ -f "/app/.version" ]; then
    export UNIDEN_ASSISTANT_VERSION=$(cat /app/.version)
fi

mkdir -p "${DB_DIR}" "${MEDIA_DIR}" "${STATIC_DIR}"

export UNIDEN_DATA_DIR="${DATA_DIR}"
export UNIDEN_DB_DIR="${DB_DIR}"
export MEDIA_ROOT="${MEDIA_DIR}"
export STATIC_ROOT="${STATIC_DIR}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-uniden_assistant.settings}"

cd "${APP_DIR}"

python manage.py migrate --noinput
python manage.py migrate --database=favorites --noinput
python manage.py collectstatic --noinput --clear

gunicorn uniden_assistant.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --log-level "${GUNICORN_LOG_LEVEL:-info}" \
    --access-logfile - \
    --error-logfile - &

exec nginx -g 'daemon off;'