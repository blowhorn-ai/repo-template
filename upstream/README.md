# Repository Template

A standardized, organization-neutral repository baseline for modern open-source software projects.

## Included Features

- **Canonical Issue Labels**: Unified taxonomy of `kind/*`, `area/*`, `component/*`, `status/*`, and community labels in [`.github/labels.yml`](.github/labels.yml).
- **Label Synchronization Tool**: Helper script [`scripts/sync-labels.sh`](scripts/sync-labels.sh) for applying labels via the GitHub CLI.
- **Structured Issue Templates**: Standardized bug report, feature request, documentation improvement, and CI/DevOps templates under [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).
- **Pull Request Template**: Comprehensive verification checklist in [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
- **Core GitHub Actions Workflows**:
  - Baseline CI verification: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
  - Pull request labeler: [`.github/workflows/labeler.yml`](.github/workflows/labeler.yml)
  - Welcoming label commenter: [`.github/workflows/label-commenter.yml`](.github/workflows/label-commenter.yml)
  - Automated release drafter: [`.github/workflows/release-drafter.yml`](.github/workflows/release-drafter.yml)
  - Configurable Slack notifications: [`.github/workflows/slack.yml`](.github/workflows/slack.yml)
  - Generic multi-architecture container build: [`.github/workflows/multi-platform.yml`](.github/workflows/multi-platform.yml)
- **Agent Ergonomics & Skills**: Repository guidance in [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), and reusable skills in [`.agents/skills/`](.agents/skills/).
- **Governance & Policy Documentation**:
  - [Workflow Policy & Architecture](docs/workflow-policy.md)
  - [Issue Templates & Labels Taxonomy](docs/templates-and-labels.md)

---

## Quickstart

1. Click **Use this template** on GitHub or clone this repository.
2. Customize project details in [`README.md`](README.md), [`AGENTS.md`](AGENTS.md), and [`CONTRIBUTING.md`](CONTRIBUTING.md).
3. Synchronize repository labels:
   ```bash
   bash scripts/sync-labels.sh --dry-run
   bash scripts/sync-labels.sh
   ```
4. Configure Continuous Integration in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
5. (Optional) Configure Slack notifications by setting `SLACK_BOT_TOKEN`.
