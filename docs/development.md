# Development Environment

This guide covers running Uniden Assistant from source for local development and testing.

## Development System Requirements

- **OS**: Debian/Ubuntu Linux or WSL (Windows Subsystem for Linux)
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **Disk Space**: approximately 500 MB including dependencies

## Setup and Run

The project uses two management scripts.

### `setup_uniden.sh`

Use `./setup_uniden.sh` for first-time setup, dependency refreshes, and environment repair.

It:

- Installs required OS packages
- Validates Python and Node.js requirements
- Creates and configures the Python virtual environment
- Installs backend dependencies from `backend/requirements.txt`
- Installs frontend dependencies
- Runs database migrations and connectivity checks

Typical usage:

```bash
./setup_uniden.sh
```

For a clean reinstall:

```bash
./setup_uniden.sh --clean
```

### `uniden_assistant`

Use `./uniden_assistant` for day-to-day application lifecycle management.

Common commands:

```bash
./uniden_assistant start
./uniden_assistant stop
./uniden_assistant restart
./uniden_assistant status
./uniden_assistant logs both
```

This script manages the backend and frontend together, handles stale processes, runs startup validation, and writes logs and PID files to the project workspace.

## Local Browser Access

After setup, start the application with:

```bash
./uniden_assistant start
```

Then open the frontend in your browser at:

- `http://localhost:9001`

For log inspection and status checks, use the orchestration script rather than starting backend or frontend services directly.

## Architecture

The application consists of:

- **Backend** - Django 4.2 REST API
- **Frontend** - Vue 3 with Quasar Framework
- **Database** - SQLite for Django core data and a separate SQLite database for favourites data

### API Architecture

The project enforces a strict multi-tier API hierarchy.

#### Uniden Manager

- Base path: `/api/uniden_manager/`
- The frontend must call this API only
- This layer does not access any database directly
- It acts as the gateway for front-end requests

#### Favourites API

- Base path: `/api/favourites/`
- Handles favourites lists, scanner profiles, and related data
- Uses its own dedicated SQLite database
- Must not read from or write to any other database

### Database Isolation

- The default SQLite database is reserved for Django core tables such as auth, admin, and sessions
- Favourites and scanner profile data live in a dedicated SQLite database configured through the database router

For the more detailed architecture reference, see [architecture.md](architecture.md).