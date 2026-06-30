#!/usr/bin/env bash
# Sync the awaken-csv skill from the i2 project into this plugin repo.
# Source of truth: i2/.claude/skills/awaken-csv. This repo is the published snapshot.
#
# Usage:
#   SOURCE=/path/to/skill/dir ./sync.sh
set -euo pipefail

if [ -z "${SOURCE:-}" ]; then
  echo "Usage: SOURCE=/path/to/skill/dir ./sync.sh" >&2
  echo "Set SOURCE to the awaken-csv skill directory to sync from." >&2
  exit 1
fi
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HERE/plugins/awaken-csv/skills/awaken-csv"
MANIFEST="$HERE/plugins/awaken-csv/.claude-plugin/plugin.json"

[ -d "$SOURCE" ] || { echo "Source not found: $SOURCE" >&2; exit 1; }

rsync -a --delete "$SOURCE/" "$DEST/"

echo "Synced $SOURCE -> $DEST"
echo
echo "Changed files:"
git -C "$HERE" status --porcelain "$DEST" || true
echo
echo "Current version: $(grep -oE '"version"[^,]*' "$MANIFEST")"
echo "Next steps if anything changed:"
echo "  1. Bump \"version\" in $MANIFEST"
echo "  2. git add -A && git commit -m \"Sync awaken-csv to vX.Y.Z\" && git push"
echo "  3. Users update with: /plugin marketplace update awaken-csv-skill"
