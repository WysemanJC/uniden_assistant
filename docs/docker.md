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