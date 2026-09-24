#!/usr/bin/env bash
# Build the `storefront` app repo from storefront-src/commit-NN overlays.
#
# This repo is what the agent reads through the GitHub MCP server, so it must
# contain NOTHING about the workshop: no incident, no harness, no answer key.
# Each commit-NN/ holds only the files that change, plus a MESSAGE that is not
# itself committed.
#
#   ./build-storefront.sh          # rebuild storefront/ and print the SHAs
set -euo pipefail
cd "$(dirname "$0")"

SRC=storefront-src
OUT=storefront
AUTHORS=(
  "Mira Halvorsen|mira@storefront.example"
  "Tomas Ek|tomas@storefront.example"
  "Priya Raman|priya@storefront.example"
  "Jonas Weber|jonas@storefront.example"
)
# Days before today that each commit was authored. The last three land together
# on release day: one release, three commits, one of them the cause.
DAYS_AGO=(61 54 47 40 31 23 0 0 0)
HOURS=(10 14 11 16 9 15 13 14 15)

rm -rf "$OUT"; mkdir -p "$OUT"; git -C "$OUT" init -q

i=0
for dir in "$SRC"/commit-*; do
  n=$(basename "$dir")
  rsync -a --exclude MESSAGE "$dir/" "$OUT/"
  who=${AUTHORS[$((i % ${#AUTHORS[@]}))]}
  when=$(python3 -c "
import datetime,sys
d=datetime.datetime.now()-datetime.timedelta(days=${DAYS_AGO[$i]})
print(d.replace(hour=${HOURS[$i]},minute=(7+$i*13)%60,second=0).strftime('%Y-%m-%dT%H:%M:%S'))")
  git -C "$OUT" add -A
  GIT_AUTHOR_NAME="${who%%|*}"    GIT_AUTHOR_EMAIL="${who##*|}"    GIT_AUTHOR_DATE="$when" \
  GIT_COMMITTER_NAME="${who%%|*}" GIT_COMMITTER_EMAIL="${who##*|}" GIT_COMMITTER_DATE="$when" \
    git -C "$OUT" -c commit.gpgsign=false commit -q --no-verify -F "$PWD/$dir/MESSAGE"
  i=$((i + 1))
done

# Tag the two releases the harness deploys.
git -C "$OUT" tag -f v3.1.0 "$(git -C "$OUT" log --format=%H --reverse | sed -n 6p)" >/dev/null
git -C "$OUT" tag -f v3.2.0 HEAD >/dev/null

{
  echo "GOOD_SHA=$(git -C "$OUT" rev-parse --short v3.1.0)"
  echo "BAD_SHA=$(git -C "$OUT" rev-parse --short v3.2.0)"
} > .storefront-shas

echo "storefront/ built:"
git -C "$OUT" log --format='  %h  %ad  %an  %s' --date=short
echo
cat .storefront-shas
echo
echo "Commit dates are relative to today, so rebuilding on another day produces"
echo "different SHAs. Once this repo is pushed to GitHub, stop rebuilding it --"
echo "edit it there, or re-push and re-read .storefront-shas."
