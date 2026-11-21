# Implementation Plan: Blowhorn Repository Template

## 1. Context & Objectives

As Blowhorn AI expands across multiple software projects, repositories must maintain high quality, standard governance, automated workflows, and agent ergonomics without drifting apart. Historically, repositories like `blowhorn-ai/tells` adopted portions of Layer5 and Meshery conventions, but no standardized template existed.

This implementation fulfills GitHub issue [#89](https://github.com/blowhorn-ai/tells/issues/89) and official instructions from Lee Calcote for [`blowhorn-ai/repo-template`](https://github.com/blowhorn-ai/repo-template).

### Primary Goals
1. **Blowhorn Standard Template**: Establish an authoritative repository template containing GitHub workflows, issue templates, label taxonomies, PR templates, agent instructions, and community policies adapted specifically for Blowhorn AI.
2. **Upstream Reusability (`upstream/`)**: Provide a completely decoupled, organization-neutral version in `upstream/` ready for contribution to upstream open-source repositories or adoption by other organizations.
3. **Workflow Strategy & Exclusions**: Define clear boundaries between universal, optional, and intentionally excluded workflows (such as Meshery-specific orchestration or Tells-specific Cloudflare/npm deploy pipelines).
4. **Complete Accounting**: Account for all common issue labels and templates from Layer5 and Meshery, documenting explicit rationales for inclusions, adaptations, and exclusions.
5. **Quality & Security**: Enforce strict workflow permissions (least privilege), secure action pinning, robust secret handling, and automated validation.

---

## 2. Issue Templates & Labels Taxonomy

### A. Issue Templates
- **Bug Report (`.github/ISSUE_TEMPLATE/bug_report.md`)**: Structured bug report with reproduction steps, environment details, logs, and default labels `['kind/bug', 'help wanted']`.
- **Feature Request (`.github/ISSUE_TEMPLATE/feature_request.md`)**: Structured enhancement proposal with problem context, proposed solution, alternatives, and default labels `['kind/enhancement', 'help wanted']`.
- **Documentation (`.github/ISSUE_TEMPLATE/documentation.md`)**: Targeted documentation gap or improvement request with default labels `['area/docs', 'help wanted']`.
- **CI / DevOps (`.github/ISSUE_TEMPLATE/ci.md`)**: Automation and workflow task template with default labels `['area/ci', 'help wanted']`.
- **Template Configuration (`.github/ISSUE_TEMPLATE/config.yml`)**: Disables blank issues (`blank_issues_enabled: false`) to enforce structured triage; provides contact links for email support (`support@blowhorn.ai`), security advisories, and community questions.
- **Intentionally Excluded Meshery Templates**:
  - `models.md`, `playground.md`, `meshery-ui_*.md`, `mesheryctl_*.md`, `meshery-extensions_*.md`: Excluded because they encode Meshery-specific architecture and CLI tooling. Documented in `docs/templates-and-labels.md`.

### B. Issue Labels (`.github/labels.yml`)
- **Kinds**: `kind/bug`, `kind/enhancement`, `kind/feature`, `kind/chore`, `kind/documentation`, `kind/refactor`, `kind/test`
- **Areas**: `area/ci`, `area/docs`, `area/security`, `area/infra`, `area/build`
- **Components**: `component/ui`, `component/backend`, `component/cli`, `component/api`
- **Status**: `status/accepted`, `status/in-progress`, `status/blocked`, `status/stale`, `status/duplicate`, `status/wontfix`
- **Community**: `help wanted`, `good first issue`, `first-timers-only`
- **Synchronization**: `scripts/sync-labels.sh` provides safe, idempotent label creation and updates using the GitHub CLI with dry-run support.

---

## 3. GitHub Actions Workflows Architecture

### Universal Workflows (Enabled by default)
1. **`ci.yml`**: Baseline continuous integration workflow with a safe configuration check and structured guidance for adding language-specific test matrices.
2. **`labeler.yml`**: Automatic path-based PR labeling using `actions/labeler@v5` triggered on `pull_request_target` with read-only repository access (`contents: read`, `pull-requests: write`).
3. **`label-commenter.yml`**: Responsive guidance bot using `peaceiris/actions-label-commenter@v1` posting helpful onboarding messages when `help wanted`, `good first issue`, or specific areas are labeled.
4. **`release-drafter.yml`**: Automated GitHub release notes generator categorizing merged PRs into Features, Bug Fixes, Maintenance, and Security.

### Optional & Configurable Workflows
1. **`slack.yml`**: Configurable Slack notifications for stars and new issues. Safely checks if `SLACK_BOT_TOKEN` secret is configured; degrades gracefully with a clear skip log if absent.
2. **`multi-platform.yml`**: Generic container image builder using Docker Buildx and QEMU. Triggered via `workflow_dispatch` (manual), configurable for target image, tag, and registry (GHCR/Docker Hub), multi-architecture (`linux/amd64`, `linux/arm64`).

### Intentionally Excluded Workflows
- **Tells-specific deployment**: Cloudflare Workers deployment (`deploy.yml`) and npm package publishing (`publish-blowhorn-tells.yml`) are excluded from the template baseline.
- **Meshery-specific workflows**: 25+ workflows (`codeql-analysis.yml` without matrix, `go-testing-ci.yml`, `helm-chart-releaser.yml`, `mesheryctl-ci.yml`, `model-generator.yml`, etc.) are documented in `docs/workflow-policy.md` as domain-specific.

---

## 4. Agent Guidelines & Skills System

- **`AGENTS.md`**: Canonical instructions for coding agents operating in repositories derived from this template. Defines project boundaries, build commands, verification expectations, and working rules.
- **`CLAUDE.md`**: Claude Code compatibility entry point pointing directly to `AGENTS.md` as the single source of truth.
- **Commonplace Skills (`.agents/skills/`)**:
  - `code-review`: Checklist and criteria for verifying correctness, security, regressions, and tests.
  - `documentation`: Rules for maintaining single-source-of-truth documentation and updating links.
  - `repo-navigation`: Guidelines for exploring unfamiliar repositories safely.
  - `testing`: Standards for choosing, running, and reporting behavioral tests.

---

## 5. Upstream Neutrality & Synchronization Strategy

- **`upstream/` directory**: Contains an identical mirror of the repository template with all Blowhorn-specific identifiers (`blowhorn-ai`, `Blowhorn AI`, `support@blowhorn.ai`, etc.) replaced by documented upstream placeholders (`<ORGANIZATION>`, `<PROJECT_NAME>`, `support@example.com`).
- **`UPSTREAMING.md`**: Comprehensive upstreaming guide detailing differences, mapping variables, and upstream contribution prerequisites.
- **`scripts/sync-upstream.sh`**: Automated validator and synchronizer verifying that core workflow structures, templates, and skills stay in sync between Blowhorn and upstream without unintended drift.

---

## 6. Implementation & Validation Steps

1. [x] Clone `blowhorn-ai/repo-template` and branch to `feat/repository-template`.
2. [ ] Flesh out and adapt all Blowhorn configuration files, workflows, documentation, and agent skills.
3. [ ] Flesh out `docs/workflow-policy.md` and `docs/templates-and-labels.md`.
4. [ ] Implement complete `upstream/` directory structure.
5. [ ] Provide synchronization tool `scripts/sync-upstream.sh`.
6. [ ] Author `UPSTREAMING.md`.
7. [ ] Perform comprehensive validation (YAML syntax, Action syntax, shell script checks, executable permissions, link validation, upstream parity).
8. [ ] Commit focused changes with clear commit messages.
