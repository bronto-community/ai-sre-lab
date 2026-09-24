#!/usr/bin/env bash
# One-off host prerequisites, safe to re-run: the Amazon Linux docker package
# ships buildx 0.12, and `docker compose build` needs 0.17 or later. Plugins in
# /usr/local/lib/docker/cli-plugins take precedence over the packaged ones.
set -euo pipefail
BUILDX=v0.30.1
dir=/usr/local/lib/docker/cli-plugins
mkdir -p "$dir"
if [ "$(docker buildx version 2>/dev/null | awk '{print $2}')" != "$BUILDX" ]; then
  curl -fsSL -o "$dir/docker-buildx" \
    "https://github.com/docker/buildx/releases/download/$BUILDX/buildx-$BUILDX.linux-arm64"
  chmod +x "$dir/docker-buildx"
fi
docker buildx version
docker compose version
