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
Included and enabled in every repository created from this template:
1. **`ci.yml`**: Baseline build and verification gate. Supports both `main` and `master` primary branch conventions.
2. **`labeler.yml`**: Applies semantic labels (`area/*`, `component/*`) to pull requests based on changed files.
3. **`label-commenter.yml`**: Posts welcoming contributor guidance and triage reminders when designated labels are applied.
4. **`release-drafter.yml`**: Automatically generates categorized release drafts from merged pull requests targeting either `main` or `master`.

### B. Optional & Configurable Workflows
Configured based on specific project needs and technology stack:
1. **`slack.yml`**: Automated notifications for issue and project events using Slack's standard Web API (`chat.postMessage`). Safely disabled by default if `SLACK_BOT_TOKEN` is absent (graceful skip without failing the build). Target channel is configurable via `vars.SLACK_CHANNEL` (defaults to `general`).
2. **`multi-platform.yml`**: Manual-dispatch container build for multi-architecture deployment (`linux/amd64`, `linux/arm64`). Triggered manually via `workflow_dispatch` with parameters for registry, image name, and tag. Defaults to non-publishing (`push: false`) to prevent accidental releases.
3. **`codeql-analysis.yml`**: Optional automated Static Application Security Testing (SAST) using GitHub CodeQL. Configured with a default language matrix (`javascript-typescript`) that project owners customize for their language stack (e.g. `python`, `go`, `c-cpp`, `java-kotlin`). Runs weekly and on pull requests targeting `main` or `master`.

### C. Intentionally Excluded Workflows
These workflows exist in other repositories (like Layer5, Meshery, or Tells) but are **strictly excluded** from this template baseline:
- **Tells-Specific Workflows**:
  - `deploy.yml`: Cloudflare Workers deployment tightly coupled to Tells edge endpoints and Cloudflare API credentials.
  - `publish-blowhorn-tells.yml`: npm trusted publishing for the `@blowhorn/tells` package.
- **Meshery-Specific Workflows**:
  - `codeql-analysis.yml` (monolithic Meshery config): Excluded in favor of the generic, lightweight CodeQL starter provided above.
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
| `codeql-analysis.yml`| None | None | `contents: read`, `security-events: write` | Fails if codeql cannot analyze language |

### Graceful Secret Degradation
All optional workflows check for credentials prior to execution:
```bash
if [ -z "$SLACK_BOT_TOKEN" ]; then
  echo "SLACK_BOT_TOKEN is not configured; skipping Slack notifications."
  exit 0
fi
```
Workflows must **never** fail solely because optional secrets are not configured in a fork or test repository.

---

## 3. Primary Branch Conventions (`main` vs. `master`)

Repositories across Blowhorn and open source projects vary in their primary branch naming (`master` in `blowhorn-ai/repo-template` and Layer5; `main` in many modern repositories). 

All template workflows (`ci.yml`, `release-drafter.yml`, `codeql-analysis.yml`) are configured with dual-branch triggers:
```yaml
branches: ["main", "master"]
```
This ensures workflows operate correctly immediately upon repository initialization, whether the default branch is `main` or `master`.

---

## 4. Security & Permissions Policy

1. **Principle of Least Privilege**: Each job declares explicit top-level or job-level `permissions:`. Never grant `permissions: write-all`.
2. **`pull_request_target` Safety**: Only used for workflows needing token write privileges (such as labeling). Workflows triggered by `pull_request_target` must **never** checkout and execute untrusted code from fork branches.
3. **Third-Party Action Pinning**: Actions must be pinned to major versions or immutable commit SHAs from verified publishers (`actions/*`, `docker/*`, `github/*`, `peaceiris/*`, `release-drafter/*`).
4. **Credential Isolation**: No secrets, auth tokens, Slack webhook URLs, or internal endpoints may ever be committed directly to workflow files.
