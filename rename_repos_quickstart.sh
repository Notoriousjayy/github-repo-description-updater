#!/usr/bin/env bash
set -euo pipefail

SCRIPT="${SCRIPT:-github_repo_renamer.py}"
PY="${PYTHON:-python3}"

if [[ ! -f "$SCRIPT" ]]; then
  echo "ERROR: $SCRIPT not found in $(pwd)"
  echo "Set SCRIPT=/path/to/github_repo_renamer.py or run from the directory containing it."
  exit 1
fi

DEFAULT_USER="$(gh api user -q .login 2>/dev/null || true)"
read -r -p "GitHub username (owner) [default: ${DEFAULT_USER}]: " USERNAME
if [[ -z "${USERNAME}" ]]; then
  USERNAME="${DEFAULT_USER}"
fi
if [[ -z "${USERNAME}" ]]; then
  echo "ERROR: Could not determine username. Provide it explicitly."
  exit 1
fi

echo
echo "1) Preview plan"
echo "2) Dry run (simulate)"
echo "3) Execute ALL renames"
echo "4) Execute by priority (high/medium/low)"
echo "5) Execute specific repos"
echo "6) Export plan.json"
echo "7) Exit"
echo

read -r -p "Select option (1-7): " OPT

case "$OPT" in
  1)
    "$PY" "$SCRIPT" --username "$USERNAME" --preview
    ;;
  2)
    "$PY" "$SCRIPT" --username "$USERNAME" --dry-run
    ;;
  3)
    "$PY" "$SCRIPT" --username "$USERNAME" --execute
    ;;
  4)
    read -r -p "Priority (high|medium|low): " PRI
    "$PY" "$SCRIPT" --username "$USERNAME" --priority "$PRI" --execute
    ;;
  5)
    read -r -p "Repos (space-separated): " -a REPOS
    "$PY" "$SCRIPT" --username "$USERNAME" --repos "${REPOS[@]}" --execute
    ;;
  6)
    # IMPORTANT: your current github_repo_renamer.py exports only if preview isn't auto-selected.
    # Using --dry-run ensures export runs without making changes.
    "$PY" "$SCRIPT" --username "$USERNAME" --dry-run --export plan.json
    echo "Wrote: $(pwd)/plan.json"
    ;;
  7)
    exit 0
    ;;
  *)
    echo "Invalid option: '$OPT' (choose 1-7)"
    exit 1
    ;;
esac
