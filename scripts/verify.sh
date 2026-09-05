#!/usr/bin/env bash
set -euo pipefail

command -v docker >/dev/null 2>&1 || {
  echo "docker is required to verify this repository" >&2
  exit 1
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UV_VERSION="${UV_VERSION:-0.12.1}"
TRIVY_VERSION="${TRIVY_VERSION:-0.74.0}"
TRIVY_CACHE_DIR="${TRIVY_CACHE_DIR:-${HOME}/.cache/asuswrt-mcp/trivy}"
mkdir -p "$TRIVY_CACHE_DIR"

UV_IMAGE="${UV_IMAGE:-ghcr.io/astral-sh/uv:0.12.4-python3.12-trixie-slim}"

echo "==> Python 3.11 and 3.13: sync, compile, tests"
docker run --rm \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e PYTHONPYCACHEPREFIX=/tmp/pycache \
  -v "$ROOT:/work:ro" \
  "$UV_IMAGE" \
  bash -lc 'set -euo pipefail; cp -a /work /tmp/project; cd /tmp/project; uv python install 3.11 3.13; for py in 3.11 3.13; do export UV_PROJECT_ENVIRONMENT="/tmp/venv-$py"; rm -rf "$UV_PROJECT_ENVIRONMENT"; uv sync --locked --extra dev --python "$py"; uv run --locked --extra dev --python "$py" python -m compileall -q src tests; uv run --locked --extra dev --python "$py" pytest -q -p no:cacheprovider; done'

echo "==> Build wheel and sdist"
docker run --rm \
  -v "$ROOT:/work:ro" \
  "$UV_IMAGE" \
  bash -lc 'set -euo pipefail; cp -a /work /tmp/project; cd /tmp/project; mkdir -p /tmp/dist; uv build --out-dir /tmp/dist; test -n "$(find /tmp/dist -maxdepth 1 -type f -name "*.whl" -print -quit)"; test -n "$(find /tmp/dist -maxdepth 1 -type f -name "*.tar.gz" -print -quit)"; ls -1 /tmp/dist'

echo "==> Trivy HIGH/CRITICAL source scan"
docker run --rm \
  -v "$ROOT:/work:ro" \
  -v "$TRIVY_CACHE_DIR:/root/.cache/trivy" \
  "ghcr.io/aquasecurity/trivy:${TRIVY_VERSION}" filesystem \
  --scanners vuln,secret,misconfig \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  --exit-code 1 \
  --no-progress \
  /work

if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$ROOT" diff --check
fi

echo "verification=ok"
