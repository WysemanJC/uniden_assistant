#!/usr/bin/env bash
set -euo pipefail

image_name="${1:-uniden-assistant:latest}"

docker build -t "${image_name}" "$(cd "$(dirname "$0")/.." && pwd)"