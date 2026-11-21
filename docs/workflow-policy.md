# GitHub Actions Workflow Policy & Architecture

This document establishes the official workflow architecture, security standards, and configuration policies for repositories across the Blowhorn AI organization.

---

## 1. Universal vs. Optional vs. Excluded Workflows

Workflows are classified into three distinct categories:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          Workflow Taxonomy                             │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│        Universal         │         Optional         │     Excluded     │
│   (Always active)        │   (Project-specific)     │ (Domain-specific)│
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ • ci.yml                 │ • slack.yml              │ • Meshery (25+)  │
│ • labeler.yml            │ • multi-platform.yml     │ • Tells deploy   │
│ • label-commenter.yml    │ • codeql-analysis.yml    │ • npm publish    │
│ • release-drafter.yml    │                          │                  │
└──────────────────────────┴──────────────────────────┴──────────────────┤
```

### A. Universal Workflows
Included in every repository created from this template:
1. **`ci.yml`**: Baseline build and verification gate.
2. **`labeler.yml`**: Applies semantic labels (`area/*`, `component/*`) to pull requests based on changed files.
3. **`label-commenter.yml`**: Posts welcoming contributor guidance and triage reminders when designated labels are applied.
4. **`release-drafter.yml`**: Automatically generates categorized release drafts from merged pull requests.

### B. Optional & Configurable Workflows
Enabled or configured based on project needs:
1. **`slack.yml`**: Chatops notifications for issue and project events. Safely disabled by default if credentials are absent.
2. **`multi-platform.yml`**: Manual-dispatch container build for multi-architecture deployment (`linux/amd64`, `linux/arm64`). Defaults to non-publishing (`push: false`) to prevent accidental releases.
3. **CodeQL / Security Scanners**: Configured when repositories introduce public APIs, compiled binaries, or sensitive web endpoints.

### C. Intentionally Excluded Workflows
These workflows exist in other repositories (like Layer5, Meshery, or Tells) but are **strictly excluded** from this template baseline:
- **Tells-Specific Workflows**:
  - `deploy.yml`: Cloudflare Workers deployment tightly coupled to Tells edge endpoints and Cloudflare API credentials.
  - `publish-blowhorn-tells.yml`: npm trusted publishing for the `@blowhorn/tells` package.
- **Meshery-Specific Workflows**:
  - `codeql-analysis.yml` (monolithic Meshery config): Coupled to Meshery Go/JS matrices.
  - `mesheryctl-ci.yml`, `build-and-release-ctl.yml`: Meshery command-line CLI packaging (Homebrew, Scoop).
  - `helm-chart-releaser.yml`: Kubernetes Helm chart releases.
  - `build-ui-and-server.yml`: Monolithic Meshery UI/Server compilation.
  - `model-generator.yml`, `integrations-updater.yml`: Meshery cloud models and meshsync integrations catalog.
  - `preview-site.yml`, `redocly.yml`, `graphql.yml`: Meshery documentation portals and GraphQL schema generators.

---

## 2. Configuration & Secrets Management

| Workflow | Required Secrets | Optional Variables | Permissions Required | Failure Mode if Secret Missing |
| :--- | :--- | :--- | :--- | :--- |
| `ci.yml` | None | None | `contents: read` | Fails only on real test/build failure |
| `labeler.yml` | `GITHUB_TOKEN` (auto) | None | `contents: read`, `pull-requests: write` | N/A |
| `label-commenter.yml` | `GITHUB_TOKEN` (auto) | None | `contents: read`, `issues: write`, `pull-requests: write` | N/A |
| `release-drafter.yml` | `GITHUB_TOKEN` (auto) | None | `contents: read`, `pull-requests: read` | N/A |
| `slack.yml` | `SLACK_BOT_TOKEN` | `SLACK_CHANNEL` | `contents: read`, `issues: read` | **Graceful skip** (logs notice, exits 0) |
| `multi-platform.yml` | `GITHUB_TOKEN` (or registry token) | `REGISTRY` | `contents: read`, `packages: write` | Build proceeds; push aborted unless flag set |

### Graceful Secret Degradation
All optional workflows must check for credentials prior to execution. For example, `slack.yml` implements:
```bash
if [ -z "$SLACK_BOT_TOKEN" ]; then
  echo "SLACK_BOT_TOKEN is not configured; skipping Slack notifications."
  exit 0
fi
```
Workflows must **never** crash or produce red build badges solely because optional secrets are not populated in a fork or fresh template clone.

---

## 3. Practical Implementation Examples

### Example 1: Adapting CI for a Node.js / TypeScript Project
In `ci.yml`, replace the placeholder verification step with:
```yaml
jobs:
  verify:
    name: Build & Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

### Example 2: Adapting CI for a Python / Go Project
```yaml
jobs:
  verify:
    name: Python Test Matrix
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - run: pytest
```

### Example 3: Running Multi-Platform Container Builds
The `multi-platform.yml` workflow can be triggered manually via the GitHub Actions UI (`workflow_dispatch`) or GitHub CLI:
```bash
gh workflow run multi-platform.yml \
  -f registry=ghcr.io \
  -f image=ghcr.io/blowhorn-ai/my-service \
  -f tag=v1.0.0 \
  -f platforms=linux/amd64,linux/arm64 \
  -f push=true
```
By defaulting `push` to `false`, developers can test container compilation across ARM and x86 without publishing partial images.

---

## 4. Security & Permissions Policy

1. **Principle of Least Privilege**: Each job declares explicit top-level or job-level `permissions:`. Never grant `permissions: write-all`.
2. **`pull_request_target` Safety**: Only used for workflows needing token write privileges (such as labeling). Workflows triggered by `pull_request_target` must **never** checkout and execute untrusted code from fork branches.
3. **Third-Party Action Pinning**: Actions must be pinned to major versions or immutable commit SHAs from verified publishers (`actions/*`, `docker/*`, `peaceiris/*`, `release-drafter/*`).
4. **Credential Isolation**: No secrets, auth tokens, Slack webhook URLs, or internal endpoints may ever be committed directly to workflow files.
