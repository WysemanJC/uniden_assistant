"""
Version information for Uniden Assistant.
Populated at build time with version calculated from Git.
"""

import os
from pathlib import Path

# Version is set at build time via environment variable or version file
# Priority: ENV var > version file > fallback

DEFAULT_VERSION = "0.0.0-dev.gunknown"

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
    # Support both legacy build metadata (e.g. 1.2.3-dev+gabc1234)
    # and Docker-safe prerelease format (e.g. 1.2.3-dev.gabc1234).
    parts = VERSION.split("+", 1)
    main_version = parts[0]
    build_metadata = parts[1] if len(parts) > 1 else ""
    
    # Parse main version (semantic version with optional pre-release)
    version_parts = main_version.split("-", 1)
    semver = version_parts[0]
    pre_release = version_parts[1] if len(version_parts) > 1 else ""

    # If no '+' metadata is present, expose trailing .g<sha> prerelease token
    # as build_metadata for compatibility with existing API consumers.
    if not build_metadata and ".g" in pre_release:
        maybe_meta = pre_release.rsplit(".g", 1)[1]
        if maybe_meta:
            build_metadata = f"g{maybe_meta}"
    
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

