#!/usr/bin/env bash
set -euo pipefail

# scripts/sync-upstream.sh
# Validates structural parity and detects organizational leaks between
# the Blowhorn AI template baseline and the organization-neutral upstream/ version.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
UPSTREAM_DIR="${REPO_ROOT}/upstream"

MODE="check"
for arg in "$@"; do
  case "$arg" in
    --check)
      MODE="check"
      shift
      ;;
    -h|--help)
      echo "Usage: bash scripts/sync-upstream.sh [--check]"
      echo "Validates that upstream/ remains structurally synchronized and neutral."
      exit 0
      ;;
  esac
done

if [[ ! -d "${UPSTREAM_DIR}" ]]; then
  echo "Error: upstream directory does not exist at ${UPSTREAM_DIR}" >&2
  exit 1
fi

echo "================================================================="
echo "Upstream Synchronization Verification"
echo "================================================================="
echo "Comparing Blowhorn baseline against upstream/..."

FAILURES=0

# List of expected upstream files corresponding to repository template files
EXPECTED_FILES=(
  "README.md"
  "CONTRIBUTING.md"
  "CODE_OF_CONDUCT.md"
  "LICENSE"
  "SECURITY.md"
  "AGENTS.md"
  "CLAUDE.md"
  "docs/workflow-policy.md"
  "docs/templates-and-labels.md"
  "scripts/sync-labels.sh"
  ".github/labels.yml"
  ".github/labeler.yml"
  ".github/label-commenter-config.yml"
  ".github/release-drafter.yml"
  ".github/stale.yml"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/ISSUE_TEMPLATE/documentation.md"
  ".github/ISSUE_TEMPLATE/ci.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  ".github/workflows/ci.yml"
  ".github/workflows/slack.yml"
  ".github/workflows/labeler.yml"
  ".github/workflows/label-commenter.yml"
  ".github/workflows/release-drafter.yml"
  ".github/workflows/multi-platform.yml"
  ".github/workflows/codeql-analysis.yml"
  ".agents/skills/code-review/SKILL.md"
  ".agents/skills/documentation/SKILL.md"
  ".agents/skills/repo-navigation/SKILL.md"
  ".agents/skills/testing/SKILL.md"
)

echo "1. Checking presence of all corresponding upstream files..."
for file in "${EXPECTED_FILES[@]}"; do
  if [[ ! -f "${UPSTREAM_DIR}/${file}" ]]; then
    echo "  [FAIL] Missing in upstream: ${file}"
    FAILURES=$((FAILURES + 1))
  else
    echo "  [OK] Found upstream/${file}"
  fi
done

echo ""
echo "2. Checking for unintended Blowhorn organization leaks in upstream/..."
LEAK_PATTERNS=("blowhorn-ai" "blowhorn.ai" "@blowhorn.ai")

for pattern in "${LEAK_PATTERNS[@]}"; do
  # Search within upstream files, ignoring git metadata
  LEAK_MATCHES=$(grep -rn "${pattern}" "${UPSTREAM_DIR}" 2>/dev/null || true)
  if [[ -n "${LEAK_MATCHES}" ]]; then
    echo "  [FAIL] Detected leaked organization pattern '${pattern}' in upstream files:"
    echo "${LEAK_MATCHES}"
    FAILURES=$((FAILURES + 1))
  else
    echo "  [OK] No occurrences of '${pattern}' in upstream/"
  fi
done

echo ""
echo "================================================================="
if [[ ${FAILURES} -eq 0 ]]; then
  echo "All upstream synchronization checks passed successfully!"
  exit 0
else
  echo "Upstream verification failed with ${FAILURES} error(s)." >&2
  exit 1
fi
