# GitHub Actions Workflow Policy & Architecture

This document establishes the workflow architecture, security standards, and configuration policies for repositories adopting this template.

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
│ • ci.yml                 │ • slack.yml              │ • Domain release │
│ • labeler.yml            │ • multi-platform.yml     │ • Cloud hosting  │
│ • label-commenter.yml    │ • codeql-analysis.yml    │ • Package pubs   │
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
1. **`slack.yml`**: Chat notifications for issue and project events. Safely disabled by default if credentials are absent.
2. **`multi-platform.yml`**: Manual-dispatch container build for multi-architecture deployment (`linux/amd64`, `linux/arm64`). Defaults to non-publishing (`push: false`) to prevent accidental releases.
3. **CodeQL / Security Scanners**: Configured when repositories introduce public APIs, compiled binaries, or web endpoints.

### C. Excluded Domain-Specific Workflows
Workflows specific to specialized frameworks, custom deployment platforms (e.g. Cloudflare Workers, Helm charts), or specific package publishing registries (e.g. npm trusted publishing) should not be part of the common template baseline. They must be added as project-specific configurations after reviewing secrets and permissions.

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
All optional workflows must check for credentials prior to execution:
```bash
if [ -z "$SLACK_BOT_TOKEN" ]; then
  echo "SLACK_BOT_TOKEN is not configured; skipping Slack notifications."
  exit 0
fi
```
Workflows must **never** fail solely because optional secrets are not configured in a fork or test repository.

---

## 3. Security & Permissions Policy

1. **Principle of Least Privilege**: Each job declares explicit top-level or job-level `permissions:`. Never grant `permissions: write-all`.
2. **`pull_request_target` Safety**: Only used for workflows needing token write privileges (such as labeling). Workflows triggered by `pull_request_target` must **never** checkout and execute untrusted code from fork branches.
3. **Third-Party Action Pinning**: Actions must be pinned to major versions or immutable commit SHAs from verified publishers (`actions/*`, `docker/*`, `peaceiris/*`, `release-drafter/*`).
4. **Credential Isolation**: No secrets, auth tokens, Slack webhook URLs, or internal endpoints may ever be committed directly to workflow files.
