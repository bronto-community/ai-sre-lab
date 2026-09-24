#!/usr/bin/env bash
# One-off host prerequisites, safe to re-run: the Amazon Linux docker package
# ships without the buildx plugin that `docker compose build` needs.
set -euo pipefail
dir=/usr/local/lib/docker/cli-plugins
mkdir -p "$dir"
if ! docker buildx version >/dev/null 2>&1; then
  v=$(curl -fsSL https://api.github.com/repos/docker/buildx/releases/latest | sed -n 's/.*"tag_name": *"\(v[^"]*\)".*/\1/p')
  curl -fsSL -o "$dir/docker-buildx" "https://github.com/docker/buildx/releases/download/$v/buildx-$v.linux-arm64"
  chmod +x "$dir/docker-buildx"
fi
docker buildx version
docker compose version
