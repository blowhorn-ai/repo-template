# Issue Templates & Labels Taxonomy

This document provides a comprehensive accounting of all issue labels, issue templates, and triage configurations implemented in the Blowhorn AI repository template, along with explicit rationale for conventions adopted from or intentionally excluded from Layer5 and Meshery.

---

## 1. Issue Templates

All issue templates are stored under `.github/ISSUE_TEMPLATE/` and configured via `config.yml`.

### Implemented Templates

| Template | File | Default Labels | Purpose |
| :--- | :--- | :--- | :--- |
| **Bug Report** | `bug_report.md` | `['kind/bug', 'help wanted']` | Captures defect reports with reproduction steps, environment specifications, and error logs. |
| **Feature Request** | `feature_request.md` | `['kind/enhancement', 'help wanted']` | Gathers structured proposals for new functionality, user experience improvements, and acceptance criteria. |
| **Documentation** | `documentation.md` | `['area/docs', 'help wanted']` | Tracks documentation gaps, corrections, or structural guide updates. |
| **CI / DevOps** | `ci.md` | `['area/ci', 'help wanted']` | Manages tasks related to GitHub Actions, build scripts, toolchain upgrades, and release automation. |

### Issue Form Configuration (`config.yml`)
- **`blank_issues_enabled: false`**: Blank issues are explicitly disabled. Contributors must select an appropriate issue template to ensure consistent context and actionable details.
- **`contact_links`**:
  - `Email Support`: Routes general queries and non-bug support to `support@blowhorn.ai`.
  - `Security Vulnerability`: Directs private vulnerability disclosures to `security@blowhorn.ai` instead of public issues.
  - `Community Discussions`: Points to GitHub Discussions for open questions, design brainstorms, and community conversations.

### Intentionally Excluded Issue Templates (from Meshery/Layer5)

| Template | Upstream Origin | Status | Rationale for Exclusion |
| :--- | :--- | :--- | :--- |
| `models.md` | Meshery | **Excluded** | Specific to Meshery cloud architecture models and design catalog generation. Unrelated to general Blowhorn projects. |
| `playground.md` | Meshery | **Excluded** | Dedicated to the hosted Meshery interactive playground environment. |
| `mesheryctl_bug.md` | Meshery | **Excluded** | Tailored specifically to the `mesheryctl` CLI binary. Blowhorn CLI projects use `bug_report.md` with label `component/cli`. |
| `meshery-ui_bug.md` | Meshery | **Excluded** | Tailored to Meshery's Next.js/Cypress frontend. Blowhorn projects use `bug_report.md` with label `component/ui`. |
| `meshery-extensions_bug.md` | Meshery | **Excluded** | Pertains to Meshery proprietary remote provider extensions. |
| `question.md` | Layer5 | **Adapted** | Replaced with GitHub Discussions link and `support@blowhorn.ai` contact link in `config.yml` to keep the issue tracker focused on actionable work. |

---

## 2. Issue Labels

The canonical label taxonomy is defined in `.github/labels.yml` and synchronized via `scripts/sync-labels.sh`.

### Implemented Labels Taxonomy

#### A. Kinds (`kind/*`)
Indicates the nature of the issue or pull request:
- `kind/bug` (`#d73a4a`): Something is not working as expected.
- `kind/enhancement` (`#a2eeef`): Improve existing functionality or UX.
- `kind/feature` (`#0e8a16`): New functionality or capability.
- `kind/chore` (`#ededed`): Maintenance, dependency updates, or housekeeping.
- `kind/documentation` (`#0075ca`): Improvements or additions to documentation.
- `kind/refactor` (`#d4c5f9`): Code refactoring without behavioral changes.
- `kind/test` (`#bfdadc`): Adding or improving test suites.

#### B. Functional Areas (`area/*`)
Indicates the technical subsystem involved:
- `area/ci` (`#5319e7`): Build, test, continuous integration, or automation.
- `area/docs` (`#0075ca`): Documentation guides, READMEs, or references.
- `area/security` (`#ee0701`): Security fixes, vulnerability reports, or audits.
- `area/infra` (`#1d76db`): Infrastructure, deployment, or hosting.
- `area/build` (`#bfdadc`): Build system, compilation, and package configuration.

#### C. Components (`component/*`)
Identifies the repository component affected:
- `component/ui` (`#1d76db`): User interface, frontend, and presentation layers.
- `component/backend` (`#5319e7`): Backend services, APIs, and business logic.
- `component/cli` (`#0052cc`): Command-line tools and utilities.
- `component/api` (`#0e8a16`): Public and private API interfaces.

#### D. Status (`status/*`)
Reflects triage and workflow state:
- `status/accepted` (`#0e8a16`): Issue triaged and accepted for implementation.
- `status/in-progress` (`#fbca04`): Work is actively ongoing.
- `status/blocked` (`#e11d21`): Blocked on external dependency or decision.
- `status/stale` (`#ededed`): No recent activity or contributor response.
- `status/duplicate` (`#cfd3d7`): Duplicate of another issue or pull request.
- `status/wontfix` (`#ffffff`): Will not be implemented or resolved.

#### E. Community & Onboarding
Encourages community engagement and signals accessible tasks:
- `help wanted` (`#008672`): Extra attention is welcome from community contributors.
- `good first issue` (`#7057ff`): Well-scoped task suitable for new contributors.
- `first-timers-only` (`#fbca04`): Reserved specifically for first-time open source contributors.

---

## 3. Label Synchronization

To sync these canonical labels to a newly created repository:
```bash
# Preview changes without modifying repository settings:
bash scripts/sync-labels.sh --dry-run

# Apply labels using GitHub CLI:
bash scripts/sync-labels.sh
```
This ensures consistent label colors, descriptions, and naming across all Blowhorn AI repositories.
