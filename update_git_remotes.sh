#!/usr/bin/env bash
set -euo pipefail

ROOT="."
PLAN="plan.json"
DRY_RUN="false"
OWNER=""

usage() {
  echo "Usage: $0 [--root DIR] [--plan plan.json] [--owner USER] [--dry-run]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2;;
    --plan) PLAN="$2"; shift 2;;
    --owner) OWNER="$2"; shift 2;;
    --dry-run) DRY_RUN="true"; shift 1;;
    -h|--help) usage;;
    *) echo "Unknown arg: $1"; usage;;
  esac
done

if [[ -z "${OWNER}" ]]; then
  OWNER="$(gh api user -q .login 2>/dev/null || true)"
fi
if [[ -z "${OWNER}" ]]; then
  echo "ERROR: Could not determine --owner. Provide --owner USER."
  exit 1
fi

if [[ ! -f "$PLAN" ]]; then
  echo "ERROR: Plan file not found: $PLAN"
  echo "Create it with: python3 github_repo_renamer.py --username $OWNER --dry-run --export plan.json"
  exit 1
fi

MAP_FILE="$(mktemp)"
python3 - "$PLAN" > "$MAP_FILE" <<'PY'
import json, sys
p = json.load(open(sys.argv[1], "r", encoding="utf-8"))
for x in p.get("proposals", []):
    old = x.get("current_name")
    new = x.get("new_name")
    if old and new and old != new:
        print(f"{old}\t{new}")
PY

declare -A MAP
while IFS=$'\t' read -r OLD NEW; do
  MAP["$OLD"]="$NEW"
done < "$MAP_FILE"
rm -f "$MAP_FILE"

echo "Scanning for git repos under: $ROOT"
echo "Owner: $OWNER"
echo "Plan: $PLAN"
echo "Dry run: $DRY_RUN"
echo

UPDATED=0
SKIPPED=0

while IFS= read -r -d '' GITDIR; do
  REPO_DIR="$(dirname "$GITDIR")"
  URL="$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null || true)"
  [[ -z "$URL" ]] && continue

  REPO_NAME=""
  if [[ "$URL" =~ ^https://github\.com/${OWNER}/([^/]+)(\.git)?$ ]]; then
    REPO_NAME="${BASH_REMATCH[1]}"
  elif [[ "$URL" =~ ^git@github\.com:${OWNER}/([^/]+)(\.git)?$ ]]; then
    REPO_NAME="${BASH_REMATCH[1]}"
  else
    SKIPPED=$((SKIPPED+1))
    continue
  fi

  NEW_NAME="${MAP[$REPO_NAME]:-}"
  if [[ -z "$NEW_NAME" ]]; then
    SKIPPED=$((SKIPPED+1))
    continue
  fi

  if [[ "$URL" =~ ^git@github\.com: ]]; then
    NEW_URL="git@github.com:${OWNER}/${NEW_NAME}.git"
  else
    NEW_URL="https://github.com/${OWNER}/${NEW_NAME}.git"
  fi

  if [[ "$URL" == "$NEW_URL" ]]; then
    SKIPPED=$((SKIPPED+1))
    continue
  fi

  echo "Repo: $REPO_DIR"
  echo "  origin: $URL"
  echo "  ->     $NEW_URL"

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY RUN] not updating"
  else
    git -C "$REPO_DIR" remote set-url origin "$NEW_URL"
    UPDATED=$((UPDATED+1))
  fi
  echo
done < <(find "$ROOT" -type d -name ".git" -print0)

echo "Done."
echo "Updated: $UPDATED"
echo "Skipped: $SKIPPED"
