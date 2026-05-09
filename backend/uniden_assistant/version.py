"""
Version information for Uniden Assistant.
Populated at build time with version calculated from Git.
"""

import os
from pathlib import Path

# Version is set at build time via environment variable or version file
# Priority: ENV var > version file > fallback

DEFAULT_VERSION = "0.0.0-dev+unknown"

# Try environment variable first (set by build scripts)
VERSION = os.environ.get("UNIDEN_ASSISTANT_VERSION")

# Try version file (created during build)
if not VERSION:
    version_file = Path(__file__).parent / ".version"
    if version_file.exists():
        try:
            VERSION = version_file.read_text(encoding="utf-8").strip()
        except Exception:
            pass

# Fallback to default
if not VERSION:
    VERSION = DEFAULT_VERSION

# Parse semantic version components
def parse_version():
    """Parse version string into components."""
    parts = VERSION.split("+", 1)
    main_version = parts[0]
    build_metadata = parts[1] if len(parts) > 1 else ""
    
    # Parse main version (semantic version with optional pre-release)
    version_parts = main_version.split("-", 1)
    semver = version_parts[0]
    pre_release = version_parts[1] if len(version_parts) > 1 else ""
    
    return {
        "full": VERSION,
        "semver": semver,
        "pre_release": pre_release,
        "build_metadata": build_metadata,
        "is_release": not pre_release and not build_metadata,
    }

# Export parsed version info for use throughout the app
VERSION_INFO = parse_version()

__version__ = VERSION

