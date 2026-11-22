#!/usr/bin/env bash
set -euo pipefail

# scripts/sync-labels.sh
# Synchronizes repository labels defined in .github/labels.yml with GitHub.
# Supports --dry-run to validate and preview changes without applying them.

DRY_RUN=false
for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      echo "Usage: bash scripts/sync-labels.sh [--dry-run]"
      echo "Synchronizes labels from .github/labels.yml to the target GitHub repository."
      exit 0
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LABELS_FILE="${REPO_ROOT}/.github/labels.yml"

if [[ ! -f "${LABELS_FILE}" ]]; then
  echo "Error: Labels file not found at ${LABELS_FILE}" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to parse ${LABELS_FILE}" >&2
  exit 1
fi

if [[ "${DRY_RUN}" == "false" ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "Error: gh (GitHub CLI) is required for syncing. Install gh or run with --dry-run." >&2
    exit 1
  fi
  if ! gh auth status >/dev/null 2>&1; then
    echo "Error: gh is not authenticated. Please run 'gh auth login'." >&2
    exit 1
  fi
fi

echo "Reading labels from ${LABELS_FILE}..."
if [[ "${DRY_RUN}" == "true" ]]; then
  echo "[DRY RUN] Previewing label synchronization:"
fi

python3 -c "
import sys
try:
    import yaml
except ImportError:
    sys.exit('Error: PyYAML is required. Install with: pip install pyyaml')

with open('${LABELS_FILE}', 'r', encoding='utf-8') as f:
    try:
        data = yaml.safe_load(f)
    except Exception as e:
        sys.exit(f'Error parsing ${LABELS_FILE}: {e}')

if not isinstance(data, list):
    sys.exit('Error: Expected ${LABELS_FILE} to contain a list of label definitions')

for item in data:
    if not isinstance(item, dict):
        continue
    name = str(item.get('name', '')).strip()
    color = str(item.get('color', '')).strip().lstrip('#')
    desc = str(item.get('description', '')).strip()
    if name:
        print(f'{name}\t{color}\t{desc}')
" | while IFS=$'\t' read -r name color desc; do
  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "  [PLAN] Create/Update label: '${name}' (color: #${color}, description: '${desc}')"
  else
    echo "  Syncing label: '${name}'..."
    gh label create "${name}" --color "${color}" --description "${desc}" --force
  fi
done

echo "Label synchronization complete."
