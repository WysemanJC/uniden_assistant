# Docker Deployment

This project is designed to run as a single container that serves the Vue UI and proxies API requests to Django through nginx on port 80.

## Image layout

- Frontend is built with Vite during the image build step and copied into nginx's web root.
- Django runs behind gunicorn on `127.0.0.1:8000` inside the container.
- nginx listens on container port `80` and proxies `/api/` and `/admin/` to gunicorn.
- Static files are collected into `/app/staticfiles` at container startup.
- Persistent SQLite databases live under `/data/uniden_assistant/db` by default.

## Database files

The container uses these default database names:

- `/data/uniden_assistant/db/uniden_assistant.sqlite3`
- `/data/uniden_assistant/db/uniden_assistant_favourites.sqlite3`

The deployer should map `/data/uniden_assistant` to a persistent Docker volume or host directory.

## Environment variables

The container is configured entirely from environment variables.

Required or strongly recommended values:

- `SECRET_KEY` - Django secret key.
- `ALLOWED_HOSTS` - Comma-separated Django host allowlist, such as `localhost,127.0.0.1,my-host`.
- `UNIDEN_DATA_DIR` - Base persistent data directory, default `/data/uniden_assistant`.
- `UNIDEN_DB_DIR` - Database directory, default `/data/uniden_assistant/db`.

Optional values:

- `DEBUG` - Set to `0` for production.
- `MEDIA_ROOT` - Override media storage location.
- `STATIC_ROOT` - Override collected static output location.
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed browser origins when cross-origin access is required.
- `CORS_ALLOW_ALL_ORIGINS` - Set to `1` only if you explicitly want to allow all origins.
- `CORS_ALLOW_CREDENTIALS` - Defaults to `1`.
- `CSRF_TRUSTED_ORIGINS` - Comma-separated list of trusted origins with scheme, such as `http://localhost`.
- `GUNICORN_WORKERS` - Number of gunicorn workers, default `3`.

For the normal single-port deployment, the frontend and backend are same-origin through nginx, so CORS can usually stay empty.

## Build

Use the build helper script:

```bash
./scripts/build_docker.sh
```

You can pass a custom image tag:

```bash
./scripts/build_docker.sh my-registry/uniden-assistant:latest
```

## Run

Example Docker run command:

```bash
docker run --rm \
  -p 80:80 \
  -e SECRET_KEY='change-me' \
  -e ALLOWED_HOSTS='localhost,127.0.0.1,my-host' \
  -e DEBUG=0 \
  -e UNIDEN_DATA_DIR=/data/uniden_assistant \
  -v uniden_assistant_data:/data/uniden_assistant \
  uniden-assistant:latest
```

## Startup sequence

When the container starts it will:

1. Create the persistent data directories if they do not exist.
2. Run Django migrations with `migrate --noinput` (default database).
3. Run Django migrations with `migrate --database=favorites --noinput` (favourites database).
4. Collect static files with `collectstatic --noinput`.
5. Start gunicorn and nginx.

## Notes

- The container only exposes port `80` externally.
- API calls should use the same-origin `/api` base path.
- If you place the app behind another proxy or TLS terminator, update `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` accordingly.