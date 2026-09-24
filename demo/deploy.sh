#!/usr/bin/env bash
# Deploy a storefront commit on the shop host. Called by the storefront repo's
# deploy workflow (via SSM) on every push to main:
#
#   /opt/storefront/deploy.sh <sha>
#
# Only services whose code changed since the last deploy are rebuilt, like a
# real release: shipping checkout-api doesn't restart the catalog.
set -euo pipefail
cd "$(dirname "$0")"

SHA=$1
REPO=https://github.com/ai-sre-lab/storefront.git
COMPOSE="docker compose --env-file .env --env-file .deploy-state"
ALL="web checkout payments catalog"

touch .env .deploy-state
[ -d .deploy ] || git clone -q "$REPO" .deploy
git -C .deploy fetch -q --tags --force origin
PREV=$(cat .last-deployed 2>/dev/null || true)   # written only after a deploy succeeds
git -C .deploy checkout -q "$SHA"

# Which services does this deploy touch?
if [ -z "$PREV" ] || ! git -C .deploy cat-file -e "$PREV" 2>/dev/null; then
  SERVICES=$ALL
else
  changed=$(git -C .deploy diff --name-only "$PREV" "$SHA")
  if grep -qE '^(Dockerfile|requirements\.txt|services/common/)' <<<"$changed"; then
    SERVICES=$ALL
  else
    SERVICES=$(grep -oE '^services/(web|checkout|payments|catalog)/' <<<"$changed" \
      | cut -d/ -f2 | sort -u | tr '\n' ' ' || true)
  fi
fi

VERSION=$(git -C .deploy describe --tags --exact-match "$SHA" 2>/dev/null | sed 's/^v//' || true)
printf 'GIT_COMMIT=%s\nGIT_REPO=ai-sre-lab/storefront\nCHECKOUT_VERSION=%s\n' \
  "$SHA" "${VERSION:-${SHA:0:7}}" > .deploy-state

$COMPOSE up -d --build collector psp
[ -n "${SERVICES// /}" ] && $COMPOSE up -d --build --no-deps $SERVICES
$COMPOSE up -d --build loadgen
echo "$SHA" > .last-deployed
echo "deployed ${SHA:0:7} (${VERSION:-untagged}) to: ${SERVICES:-nothing changed}"
