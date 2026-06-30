#!/usr/bin/env bash
# Sync the awaken-csv skill from the i2 project into this plugin repo.
# Source of truth: i2/.claude/skills/awaken-csv. This repo is the published snapshot.
#
# Usage:
#   ./sync.sh            # sync files, then show what changed
#   SOURCE=/path ./sync.sh   # override the source skill dir
set -euo pipefail

SOURCE="${SOURCE:-/home/user/code/foxreymann/i2/.claude/skills/awaken-csv}"
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HERE/plugins/awaken-csv/skills/awaken-csv"
MANIFEST="$HERE/plugins/awaken-csv/.claude-plugin/plugin.json"

command -v rsync >/dev/null 2>&1 || { echo "Error: rsync is not installed" >&2; exit 1; }
[ -d "$SOURCE" ] || { echo "Error: source not found: $SOURCE" >&2; exit 1; }
[ -f "$MANIFEST" ] || { echo "Error: manifest not found: $MANIFEST" >&2; exit 1; }

rsync -a --delete "$SOURCE/" "$DEST/"

# Verify sync produced the expected skill file
[ -f "$DEST/SKILL.md" ] || { echo "Error: sync did not produce SKILL.md in $DEST" >&2; exit 1; }

echo "Synced $SOURCE -> $DEST"
echo
echo "Changed files:"
if ! git -C "$HERE" status --porcelain "$DEST"; then
  echo "Warning: git status failed — is this a git repo?" >&2
fi
echo

VERSION=$(grep -oE '"version"[^,]*' "$MANIFEST") || { echo "Error: could not read version from $MANIFEST" >&2; exit 1; }
echo "Current version: $VERSION"
echo "Next steps if anything changed:"
echo "  1. Bump \"version\" in $MANIFEST"
echo "  2. git add -A && git commit -m \"Sync awaken-csv to vX.Y.Z\" && git push"
echo "  3. Users update with: /plugin marketplace update awaken-csv-skill"
