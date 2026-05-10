#!/usr/bin/env bash
# Calculate semantic version from Git state
# Output: version string suitable for use in app, Docker image, and metadata
# Reproducible: same Git state always produces same version

set -euo pipefail

# Get the directory this script is in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root for Git operations
cd "$PROJECT_ROOT"

# Ensure we have Git available
if ! command -v git &>/dev/null; then
    echo "ERROR: git not found in PATH" >&2
    exit 1
fi

# Get the latest reachable tag name matching v*.
# --abbrev=0 avoids describe suffixes like -4-g<sha>, which break semver parsing.
LATEST_TAG=$(git describe --tags --match 'v*' --abbrev=0 2>/dev/null || echo "v0.0.0")

# Extract version from tag (strip leading 'v')
LATEST_VERSION="${LATEST_TAG#v}"

# Check if current HEAD is exactly on the tag (release build)
CURRENT_TAG=$(git describe --exact-match --tags 2>/dev/null || echo "")
if [ -n "$CURRENT_TAG" ]; then
    # We are on a release tag
    echo "${CURRENT_TAG#v}"
    exit 0
fi

# Not on a tag: we're in development
# Calculate commits since the last tag
COMMIT_COUNT=$(git rev-list --count "${LATEST_TAG}..HEAD" 2>/dev/null || echo "0")

# Get short SHA
SHORT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Get the branch or ref name for label
REF_NAME=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null || echo "detached")

# Determine pre-release label based on branch/environment
if [ "$REF_NAME" = "main" ] || [ "$REF_NAME" = "master" ]; then
    LABEL="dev"
elif [[ "$REF_NAME" == *"release"* ]] || [[ "$REF_NAME" == *"rc"* ]]; then
    LABEL="rc"
else
    # Feature branch or PR
    LABEL="test"
fi

# Increment patch version
IFS='.' read -r MAJOR MINOR PATCH <<< "$LATEST_VERSION"
NEXT_PATCH=$((PATCH + 1))
NEXT_VERSION="${MAJOR}.${MINOR}.${NEXT_PATCH}"

# Construct version string using a Docker-safe SemVer pre-release.
# Format: MAJOR.MINOR.PATCH-LABEL.gSHA
VERSION="${NEXT_VERSION}-${LABEL}.g${SHORT_SHA}"

echo "$VERSION"
