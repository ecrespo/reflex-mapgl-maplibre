#!/usr/bin/env bash
# Create the public GitHub repository and push the initial commit.
# Requirement: be authenticated with gh  ->  gh auth login   (or export GH_TOKEN)
set -euo pipefail

REPO_NAME="reflex-mapgl-maplibre"
DESC="Reflex wrapper for react-map-gl (maplibre endpoint) — interactive MapLibre GL JS maps in pure Python"

cd "$(dirname "$0")/.."

# Verify authentication
if ! gh auth status >/dev/null 2>&1; then
  echo "Not authenticated with gh. Run first:  gh auth login" >&2
  exit 1
fi

# Create the public repo under your account, add the 'origin' remote and push
gh repo create "$REPO_NAME" \
  --public \
  --source=. \
  --remote=origin \
  --description "$DESC" \
  --push

echo "Done: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
