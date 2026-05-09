# Uniden Assistant

A web application for managing Uniden Scanner Favourites lists. Import, edit, and export scanner configuration files with an intuitive interface.

## Features

- **Import** - Load Uniden scanner configuration files (`.cfg`, `.hpd`)
- **Edit** - Manage favourites lists, scanner profiles, and channel groups
- **Export** - Save your configurations back to scanner-compatible formats
- **Organize** - Create and manage multiple favourites lists

## Running in Docker

Running the published container image is the easiest way to use Uniden Assistant.

Published image:

- `ghcr.io/wysemanjc/uniden_assistant:stable`

The container serves the frontend and backend together, so you only need to publish one port and mount persistent storage for the SQLite databases.

### Quick start with `docker run`

```bash
docker run --rm \
   -p 8080:80 \
   -e EXTERNAL_URL='http://localhost:8080' \
   -v uniden_assistant_data:/data/uniden_assistant \
   ghcr.io/wysemanjc/uniden_assistant:stable
```

Then open `http://localhost:8080` in your browser.

Example for access from another machine on your LAN:

```bash
docker run --rm \
   -p 8080:80 \
   -e EXTERNAL_URL='http://192.168.1.10:8080' \
   -v uniden_assistant_data:/data/uniden_assistant \
   ghcr.io/wysemanjc/uniden_assistant:stable
```

### Example `docker-compose.yml`

```yaml
services:
   uniden-assistant:
      image: ghcr.io/wysemanjc/uniden_assistant:stable
      container_name: uniden_assistant
      restart: unless-stopped
      ports:
         - "8080:80"
      environment:
         EXTERNAL_URL: http://localhost:8080
      volumes:
         - uniden_assistant_data:/data/uniden_assistant

volumes:
   uniden_assistant_data:
```

Start it with:

```bash
docker compose up -d
```

### `EXTERNAL_URL`

`EXTERNAL_URL` is the full public URL used to reach the application, including the scheme and port when needed.

Examples:

- `http://localhost:8080`
- `http://192.168.1.10:8080`
- `https://scanner.example.com`

In most deployments, this is the only environment variable you need to set explicitly. The application derives the host, CORS, and CSRF settings from this value automatically. For long-lived production deployments, you may also want to review the additional environment variables documented in [docs/docker.md](docs/docker.md).

## Development Environment

If you want to run the project from source instead of the published container, see [docs/development.md](docs/development.md). That guide covers local setup, the supported management scripts, browser access during development, system requirements, and the application architecture.

## File Specifications

Documentation for supported file formats and record types is available in [docs/Input_File_Specification/](docs/Input_File_Specification/).

## License

Apache License 2.0

Pull requests welcome.
