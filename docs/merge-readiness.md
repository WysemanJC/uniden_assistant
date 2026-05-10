# Merge Readiness Checklist

This checklist is for preparing a pre-release branch for merge into main.

## Required Script-Based Workflow

Use only these scripts:

1. `./setup_uniden.sh` for setup/repairs/dependency refresh.
2. `./uniden_assistant` for start/stop/restart/status/logs.

Do not bypass these scripts for normal project setup or lifecycle management.

## Ignore/Packaging Hygiene

Verify the following before merge:

1. `.gitignore` excludes local runtime artifacts, virtualenvs, logs, local DB files, and local development data.
2. `.dockerignore` excludes development-only data and files not required in image builds.
3. Build context does not include `DEVELOPMENT/`, `SAMPLE_DATA/`, local logs, or local PID files.

## Architecture Compliance Checks

## Frontend Tier Rule

Frontend must call only Uniden Manager routes:

- Allowed base: `/api/uniden_manager/`
- Frontend API client base should resolve to `/api/uniden_manager`

Quick check:

- Search frontend source for direct `/api/favourites` usage.

## Uniden Manager Tier Rule

Uniden Manager must not access databases directly.

- Must not import model classes from data tiers for direct ORM operations.
- Must call internal tier APIs only.

Quick checks:

1. Search `backend/uniden_assistant/uniden_manager/` for `from uniden_assistant.favourites.models`.
2. Search `backend/uniden_assistant/uniden_manager/` for `.objects.` and `.using(` patterns.

## Favourites Tier Rule

Favourites tier must use only the favourites database.

Quick checks:

1. Search `backend/uniden_assistant/favourites/` for `.using('default')`.
2. Search `backend/uniden_assistant/favourites/` for direct HPDB model/database usage.

## Current Compliance Findings (2026-05-10)

### Pass

1. Frontend API base is routed through Uniden Manager in `frontend/src/api/index.js`.
2. Favourites raw-input persistence has been removed from active schema and routes.
3. Favourites roundtrip verification script passes for NSW, OZ, and VIC.

### Blockers

1. Uniden Manager still performs direct ORM access to favourites models:
   - `backend/uniden_assistant/uniden_manager/views.py` imports `FavoritesList` and queries with ORM.
2. Uniden Manager still performs direct ORM access to HPDB models:
   - `backend/uniden_assistant/uniden_manager/views.py` imports HPDB models and writes raw file/line records.

These blockers violate the architecture rule that Uniden Manager must not directly access databases.

## Validation Commands

Run from repository root.

1. Restart app:

```bash
./uniden_assistant restart
```

2. Favourites roundtrip validation:

```bash
backend/venv/bin/python scripts/test_scripts/test_favorites_roundtrip.py --folders NSW OZ VIC
```

3. Architecture grep checks (examples):

```bash
rg "from uniden_assistant\.(favourites|hpdb)\.models|\.objects\.|\.using\(" backend/uniden_assistant/uniden_manager
rg "/api/favourites|/api/favorites" frontend/src
```

## Merge Decision Guidance

Do not merge while architecture blockers remain in Uniden Manager. Resolve by moving data operations into internal APIs and having Uniden Manager call those APIs only.
