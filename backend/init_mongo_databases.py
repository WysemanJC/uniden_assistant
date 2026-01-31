#!/usr/bin/env python
"""Initialize required MongoDB databases for Uniden Assistant.

This script ensures the HPDB, User Settings, and App Config databases exist by
creating a small marker document in each database. MongoDB creates databases on
first write.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

try:
    from pymongo import MongoClient
    from pymongo.uri_parser import parse_uri
except Exception as exc:  # pragma: no cover - safety for missing deps
    print(f"ERROR: pymongo is required to initialize MongoDB databases: {exc}", file=sys.stderr)
    sys.exit(1)


def find_config_env(start: Path) -> Path:
    for candidate_root in [start, *start.parents]:
        candidate = candidate_root / "config.env"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("config.env not found in any parent directory")


def load_config_env() -> None:
    """Load config.env into environment."""
    script_path = Path(__file__).resolve()
    config_file = find_config_env(script_path)

    with config_file.open("r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key and key not in os.environ:
                os.environ[key] = value


def with_credentials(uri: str, user: str | None, password: str | None) -> str:
    if not uri or not user:
        return uri
    if "@" in uri:
        return uri
    safe_user = quote_plus(user)
    safe_password = quote_plus(password or "")
    if uri.startswith("mongodb://"):
        return uri.replace("mongodb://", f"mongodb://{safe_user}:{safe_password}@", 1)
    if uri.startswith("mongodb+srv://"):
        return uri.replace("mongodb+srv://", f"mongodb+srv://{safe_user}:{safe_password}@", 1)
    return uri


def ensure_database(uri: str, label: str) -> None:
    if not uri:
        print(f"WARNING: {label} URI not set; skipping")
        return

    info = parse_uri(uri)
    db_name = info.get("database")
    if not db_name:
        print(f"ERROR: {label} URI is missing a database name: {uri}", file=sys.stderr)
        sys.exit(1)

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[db_name]

    db["system_init"].update_one(
        {"_id": "initialized"},
        {
            "$set": {
                "_id": "initialized",
                "label": label,
                "initialized_at": datetime.now(timezone.utc).isoformat(),
            }
        },
        upsert=True,
    )

    client.close()
    print(f"Initialized {label} database: {db_name}")


def main() -> None:
    load_config_env()

    hpdb_uri = with_credentials(
        os.getenv("UNIDEN_HPDB_DB", ""),
        os.getenv("UNIDEN_HPDB_DB_USER"),
        os.getenv("UNIDEN_HPDB_DB_PASSWORD"),
    )
    usersettings_uri = with_credentials(
        os.getenv("UNIDEN_USERSETTINGS_DB", ""),
        os.getenv("UNIDEN_USERSETTINGS_DB_USER"),
        os.getenv("UNIDEN_USERSETTINGS_DB_PASSWORD"),
    )
    appconfig_uri = with_credentials(
        os.getenv("UNIDEN_APP_DB", ""),
        os.getenv("UNIDEN_APP_DB_USER"),
        os.getenv("UNIDEN_APP_DB_PASSWORD"),
    )

    ensure_database(hpdb_uri, "HPDB")
    ensure_database(usersettings_uri, "User Settings")
    ensure_database(appconfig_uri, "App Config")


if __name__ == "__main__":
    main()
