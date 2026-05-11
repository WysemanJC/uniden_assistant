#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/app/backend"
DATA_DIR="${UNIDEN_DATA_DIR:-/data/uniden_assistant}"
DB_DIR="${UNIDEN_DB_DIR:-${DATA_DIR}/db}"
LOG_ROOT="${UNIDEN_RUNTIME_LOG_ROOT:-${DATA_DIR}/logs}"
BACKEND_LOG_DIR="${UNIDEN_LOG_DIR:-${LOG_ROOT}/backend}"
FRONTEND_LOG_DIR="${UNIDEN_FRONTEND_LOG_DIR:-${LOG_ROOT}/frontend}"
MEDIA_DIR="${MEDIA_ROOT:-${DATA_DIR}/media}"
STATIC_DIR="${STATIC_ROOT:-/app/staticfiles}"
EXTERNAL_WEB_PORT="${EXTERNAL_WEB_PORT:-80}"

if ! [[ "${EXTERNAL_WEB_PORT}" =~ ^[0-9]+$ ]] || [ "${EXTERNAL_WEB_PORT}" -lt 1 ] || [ "${EXTERNAL_WEB_PORT}" -gt 65535 ]; then
    echo "ERROR: EXTERNAL_WEB_PORT must be an integer between 1 and 65535 (got: ${EXTERNAL_WEB_PORT})" >&2
    exit 1
fi

# Read version from build artifact (if exists)
if [ -f "/app/.version" ]; then
    export UNIDEN_ASSISTANT_VERSION=$(cat /app/.version)
fi

mkdir -p "${DATA_DIR}" "${LOG_ROOT}"
mkdir -p "${DB_DIR}" "${MEDIA_DIR}" "${STATIC_DIR}" "${BACKEND_LOG_DIR}" "${FRONTEND_LOG_DIR}"

export UNIDEN_DATA_DIR="${DATA_DIR}"
export UNIDEN_DB_DIR="${DB_DIR}"
export UNIDEN_LOG_DIR="${BACKEND_LOG_DIR}"
export UNIDEN_FRONTEND_LOG_DIR="${FRONTEND_LOG_DIR}"
export MEDIA_ROOT="${MEDIA_DIR}"
export STATIC_ROOT="${STATIC_DIR}"
export EXTERNAL_WEB_PORT="${EXTERNAL_WEB_PORT}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-uniden_assistant.settings}"

sed "s/__EXTERNAL_WEB_PORT__/${EXTERNAL_WEB_PORT}/g" /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

cd "${APP_DIR}"

python manage.py migrate --noinput
python manage.py migrate --database=favorites --noinput
python manage.py collectstatic --noinput --clear

gunicorn uniden_assistant.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --log-level "${GUNICORN_LOG_LEVEL:-info}" \
    --access-logfile "${BACKEND_LOG_DIR}/gunicorn-access.log" \
    --error-logfile "${BACKEND_LOG_DIR}/gunicorn-error.log" &

exec nginx -g 'daemon off;'