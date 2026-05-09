#!/usr/bin/env bash
set -euo pipefail

# Get the repository root directory
repo_root="$(cd "$(dirname "$0")/.." && pwd)"

# Calculate semantic version from Git state
version_script="${repo_root}/scripts/version.sh"
if [ ! -f "${version_script}" ]; then
    echo "ERROR: version.sh not found at ${version_script}"
    exit 1
fi

# Calculate version (this script returns semantic version)
version=$("${version_script}") || {
    echo "ERROR: Failed to calculate version"
    exit 1
}

# Determine registry and image name
registry="${REGISTRY:-docker.io}"
namespace="${NAMESPACE:-uniden-assistant}"
image_name="${registry}/${namespace}"

# Determine image tags based on version type
image_tags=()

# Always add the full version as immutable tag
image_tags+=("${image_name}:${version}")

# Add moving tags based on version characteristics
if [[ ${version} == *"-dev"* ]]; then
    # Development build (main branch)
    image_tags+=("${image_name}:dev")
    image_tags+=("${image_name}:main")
    image_tags+=("${image_name}:latest")
elif [[ ${version} == *"-test"* ]]; then
    # Test build (develop branch or test CI)
    image_tags+=("${image_name}:test")
    image_tags+=("${image_name}:develop")
elif [[ ${version} == *"-rc"* ]]; then
    # Release candidate
    image_tags+=("${image_name}:rc")
else
    # Release build (from git tag)
    image_tags+=("${image_name}:latest")
    image_tags+=("${image_name}:stable")
    
    # Extract major.minor for moving release tag
    major_minor=$(echo "${version}" | cut -d. -f1-2)
    image_tags+=("${image_name}:${major_minor}")
fi

# Support custom tags via command-line arguments
if [ $# -gt 0 ]; then
    echo "Custom registry configuration provided"
    # User can override with: REGISTRY=ghcr.io NAMESPACE=owner/repo ./build_docker.sh
    image_tags=()
    for arg in "$@"; do
        image_tags+=("${arg}")
    done
fi

# Build image with all tags
build_args=()
for tag in "${image_tags[@]}"; do
    build_args+=("-t" "${tag}")
done

# Add version as build argument for Dockerfile
build_args+=("--build-arg" "APP_VERSION=${version}")

echo "Building Uniden Assistant Docker image..."
echo "Version: ${version}"
echo "Registry: ${registry}"
echo "Namespace: ${namespace}"
echo "Tags: ${image_tags[*]}"
echo ""

docker build "${build_args[@]}" "${repo_root}"

echo ""
echo "Build complete! Image tagged as:"
for tag in "${image_tags[@]}"; do
    echo "  - ${tag}"
done