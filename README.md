# Blowhorn AI Repository Template

Standard repository baseline for software projects maintained by the [Blowhorn AI](https://github.com/blowhorn-ai) organization.

## Features Included

- **Canonical Issue Labels**: Unified taxonomy of `kind/*`, `area/*`, `component/*`, `status/*`, and community labels defined in [`.github/labels.yml`](.github/labels.yml).
- **Automated Label Synchronization**: Helper script [`scripts/sync-labels.sh`](scripts/sync-labels.sh) to apply canonical labels to new repositories.
- **Structured Issue Templates**: Bug reports, feature requests, documentation improvements, CI/DevOps tasks, and disabled blank issues via [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).
- **Standard Pull Request Template**: Comprehensive checklist and evidence requirements in [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
- **Core GitHub Actions Workflows**:
  - Baseline CI verification: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
  - Pull request labeler: [`.github/workflows/labeler.yml`](.github/workflows/labeler.yml)
  - Welcoming label commenter: [`.github/workflows/label-commenter.yml`](.github/workflows/label-commenter.yml)
  - Automated release drafter: [`.github/workflows/release-drafter.yml`](.github/workflows/release-drafter.yml)
  - Configurable Slack notifications: [`.github/workflows/slack.yml`](.github/workflows/slack.yml)
  - Generic multi-architecture container build: [`.github/workflows/multi-platform.yml`](.github/workflows/multi-platform.yml)
- **Agent Ergonomics & Skills**: Repository guidance in [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md), and reusable skills in [`.agents/skills/`](.agents/skills/).
- **Governance & Policy Documentation**:
  - [Workflow Policy & Exclusions](docs/workflow-policy.md)
  - [Issue Templates & Labels Taxonomy](docs/templates-and-labels.md)
  - [Upstreaming & Synchronization Guide](UPSTREAMING.md)

---

## Quickstart: Creating a New Repository from this Template

1. Click **Use this template** on GitHub or clone this repository.
2. Review and update project details in [`README.md`](README.md), [`AGENTS.md`](AGENTS.md), and [`CONTRIBUTING.md`](CONTRIBUTING.md).
3. Synchronize repository labels:
   ```bash
   # Preview label sync:
   bash scripts/sync-labels.sh --dry-run

   # Apply labels using GitHub CLI:
   bash scripts/sync-labels.sh
   ```
4. Configure Continuous Integration in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for your language toolchain (see [docs/workflow-policy.md](docs/workflow-policy.md)).
5. (Optional) Configure Slack notifications by adding the `SLACK_BOT_TOKEN` secret in repository settings.

---

## Repository Setup Checklist

- [ ] Update project title and description in `README.md`.
- [ ] Configure `AGENTS.md` build and test verification commands.
- [ ] Run `bash scripts/sync-labels.sh` to populate labels.
- [ ] Adapt `.github/workflows/ci.yml` for project dependencies and tests.
- [ ] Review `.github/labeler.yml` path globs to match repository folder structure.
- [ ] Set `SLACK_BOT_TOKEN` secret if Slack notifications are desired.
