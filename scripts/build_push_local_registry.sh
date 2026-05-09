#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
config_file="${script_dir}/local_registry.conf"
config_example_file="${script_dir}/local_registry.conf.example"
version_script="${script_dir}/version.sh"

if [[ ! -f "${config_file}" ]]; then
    echo "ERROR: Missing config file: ${config_file}"
    if [[ -f "${config_example_file}" ]]; then
        echo "Create it from the example:"
        echo "  cp ${config_example_file} ${config_file}"
    fi
    echo "Then set your registry URL and credentials in ${config_file}."
    exit 1
fi

if [[ ! -x "${version_script}" ]]; then
    echo "ERROR: Missing executable version script: ${version_script}"
    exit 1
fi

# shellcheck source=/dev/null
source "${config_file}"

required_vars=(REGISTRY_URL REGISTRY_USERNAME REGISTRY_PASSWORD REGISTRY_REPOSITORY)
for var_name in "${required_vars[@]}"; do
    if [[ -z "${!var_name:-}" ]]; then
        echo "ERROR: ${var_name} must be set in ${config_file}"
        exit 1
    fi
done

if [[ "${REGISTRY_URL}" == http://* || "${REGISTRY_URL}" == https://* ]]; then
    echo "ERROR: REGISTRY_URL must not include protocol. Use host only, e.g. registry.example.com"
    exit 1
fi

image_name="${IMAGE_NAME:-uniden-assistant}"
registry_repository="${REGISTRY_REPOSITORY}"

# Docker image repository/name components must be lowercase.
image_name="$(echo "${image_name}" | tr '[:upper:]' '[:lower:]')"
registry_repository="$(echo "${registry_repository}" | tr '[:upper:]' '[:lower:]')"

calculate_version_fallback() {
    local latest_tag latest_version current_tag short_sha ref_name label
    local major minor patch next_patch

    cd "${repo_root}"

    latest_tag="$(git describe --tags --abbrev=0 --match 'v*' 2>/dev/null || echo 'v0.0.0')"
    latest_version="${latest_tag#v}"
    current_tag="$(git describe --exact-match --tags 2>/dev/null || echo '')"

    if [[ -n "${current_tag}" ]]; then
        echo "${current_tag#v}"
        return 0
    fi

    short_sha="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
    ref_name="$(git symbolic-ref --short HEAD 2>/dev/null || echo 'detached')"

    if [[ "${ref_name}" == "main" || "${ref_name}" == "master" ]]; then
        label="dev"
    elif [[ "${ref_name}" == *"release"* || "${ref_name}" == *"rc"* ]]; then
        label="rc"
    else
        label="test"
    fi

    IFS='.' read -r major minor patch <<< "${latest_version}"
    major="${major:-0}"
    minor="${minor:-0}"
    patch="${patch:-0}"

    if ! [[ "${patch}" =~ ^[0-9]+$ ]]; then
        patch=0
    fi

    next_patch=$((patch + 1))
    echo "${major}.${minor}.${next_patch}-${label}+g${short_sha}"
}

if ! version="$("${version_script}" 2>/dev/null)"; then
    echo "WARNING: scripts/version.sh failed, using fallback version calculation."
    version="$(calculate_version_fallback)"
fi

# Docker image tags do not allow '+' (SemVer build metadata separator).
# Keep original semantic version for display, but sanitize for tag usage.
docker_version="$(echo "${version}" | sed 's/+/-/g')"

image_repo="${REGISTRY_URL}/${registry_repository}/${image_name}"

tags=("${image_repo}:${docker_version}")

# Keep moving tags aligned with existing build logic without changing GHCR behavior.
if [[ "${version}" == *"-dev"* ]]; then
    tags+=("${image_repo}:dev" "${image_repo}:main" "${image_repo}:latest")
elif [[ "${version}" == *"-test"* ]]; then
    tags+=("${image_repo}:test" "${image_repo}:develop")
elif [[ "${version}" == *"-rc"* ]]; then
    tags+=("${image_repo}:rc")
else
    major_minor="$(echo "${version}" | cut -d. -f1-2)"
    tags+=("${image_repo}:latest" "${image_repo}:stable" "${image_repo}:${major_minor}")
fi

echo "Logging in to ${REGISTRY_URL}..."
printf '%s' "${REGISTRY_PASSWORD}" | docker login "${REGISTRY_URL}" --username "${REGISTRY_USERNAME}" --password-stdin

echo "Building image for version ${version}..."
build_args=("--build-arg" "APP_VERSION=${version}")
for tag in "${tags[@]}"; do
    build_args+=("-t" "${tag}")
done

docker build "${build_args[@]}" "${repo_root}"

echo "Pushing image tags..."
for tag in "${tags[@]}"; do
    echo "Pushing ${tag}"
    docker push "${tag}"
done

echo "Done."
echo "Version: ${version}"
echo "Pushed tags:"
for tag in "${tags[@]}"; do
    echo "  - ${tag}"
done
