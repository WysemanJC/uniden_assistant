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

- `SECRET_KEY` — Django secret key. Always set this in production.
- `EXTERNAL_URL` — The full public URL the app is accessed from, including scheme. For example `https://scanner.example.com` or `http://192.168.1.10:8080`. Setting this one variable automatically configures `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `CORS_ALLOWED_ORIGINS`. **This is the recommended way to deploy behind a reverse proxy or with a custom hostname.**
- `UNIDEN_DATA_DIR` — Base persistent data directory, default `/data/uniden_assistant`.
- `UNIDEN_DB_DIR` — Database directory, default `/data/uniden_assistant/db`.

Optional values:

- `DEBUG` — Set to `0` (default) for production.
- `MEDIA_ROOT` — Override media storage location.
- `STATIC_ROOT` — Override collected static output location.
- `USE_X_FORWARDED_HOST` — Defaults to `0`. Leave this disabled unless your upstream proxy rewrites `X-Forwarded-Host` to a Django-safe hostname and you explicitly need Django to trust it.
- `GUNICORN_WORKERS` — Number of gunicorn workers, default `3`.
- `GUNICORN_LOG_LEVEL` — Gunicorn log verbosity (`debug`, `info`, `warning`, `error`), default `info`.

Advanced overrides (normally derived automatically from `EXTERNAL_URL`):

- `ALLOWED_HOSTS` — Comma-separated Django host allowlist. Overrides `EXTERNAL_URL` host if set. Loopback addresses are always included regardless.
- `CORS_ALLOWED_ORIGINS` — Comma-separated list of allowed browser origins. Overrides `EXTERNAL_URL` if set.
- `CORS_ALLOW_ALL_ORIGINS` — Set to `1` only if you explicitly want to allow all origins.
- `CORS_ALLOW_CREDENTIALS` — Defaults to `1`.
- `CSRF_TRUSTED_ORIGINS` — Comma-separated list of trusted origins with scheme. Overrides `EXTERNAL_URL` if set.

## Build

Use the build helper script:

```bash
./scripts/build_docker.sh
```

By default, the script will:
- Calculate semantic version from Git state using `scripts/version.sh`
- Build the image and tag it with both the calculated version and `latest`
- Example tags: `uniden-assistant:1.4.0`, `uniden-assistant:latest`

You can also pass a custom image tag:

```bash
./scripts/build_docker.sh my-registry/uniden-assistant:latest
```

## Versioning

The application uses semantic versioning derived from Git tags:

- **Release versions**: Created from Git tags matching `v*.*.* (e.g., `v1.4.0` → image tagged `1.4.0`)
- **Development versions**: Main branch commits produce `1.4.1-dev+gabc1234` format
- **Test versions**: CI builds on test branches produce `1.4.1-test+gabc1234` format

### Version calculation

The `scripts/version.sh` script calculates the semantic version based on:
1. Latest Git tag matching `v*` pattern (e.g., `v1.4.0`)
2. Number of commits since that tag
3. Current branch or CI environment
4. Current commit short SHA

### Version availability

The calculated version is available:

- **Docker image tag**: Image is tagged with the version (e.g., `uniden-assistant:1.4.0`)
- **API endpoint**: `GET /api/uniden_manager/version/` returns version details
- **Environment variable**: `UNIDEN_ASSISTANT_VERSION` available inside container
- **Runtime module**: `backend/uniden_assistant/version.py` exports `VERSION_INFO` dict

### Example API response

```bash
curl http://localhost/api/uniden_manager/version/
```

```json
{
  "version": "1.4.0",
  "semver": "1.4.0",
  "is_release": true,
  "pre_release": "",
  "build_metadata": ""
}
```

### Creating a release

To create a release:

1. Create a Git tag: `git tag v1.4.0`
2. Push to main: `git push origin main --tags`
3. CI/CD automatically builds and tags image as `uniden-assistant:1.4.0`

## Run

Example Docker run command:

```bash
docker run --rm \
  -p 80:80 \
  -e SECRET_KEY='change-me' \
  -e EXTERNAL_URL='https://uniden.example.com' \
  -e UNIDEN_DATA_DIR=/data/uniden_assistant \
  -v uniden_assistant_data:/data/uniden_assistant \
  uniden-assistant:latest
```

For a local/LAN deployment without a hostname:

```bash
docker run --rm \
  -p 80:80 \
  -e SECRET_KEY='change-me' \
  -e EXTERNAL_URL='http://192.168.1.10' \
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
- API calls use the same-origin `/api` base path — no CORS configuration is needed when accessing through the container's own nginx.
- When placing the app behind a reverse proxy or TLS terminator (e.g. Traefik, Nginx Proxy Manager), set `EXTERNAL_URL` to the public URL. This is sufficient for `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `CORS_ALLOWED_ORIGINS` to be configured correctly.
- The container automatically trusts `X-Forwarded-Proto` headers from an upstream proxy so HTTPS is detected correctly.
- The container does not trust `X-Forwarded-Host` by default. This avoids `400 Bad Request` failures when an upstream proxy forwards public hostnames that Django rejects, such as names containing underscores.