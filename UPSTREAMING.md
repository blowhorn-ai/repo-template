# Upstreaming & Synchronization Guide

This document explains the relationship, differences, and synchronization process between the **Blowhorn AI repository template** (located at the repository root) and the **organization-neutral upstream version** (located in `upstream/`).

---

## 1. Executive Summary

- **Blowhorn Version (Root)**: Tailored for repositories created within the [Blowhorn AI](https://github.com/blowhorn-ai) organization. Includes organizational links, Blowhorn triage channels, and Blowhorn community guidance.
- **Upstream Version (`upstream/`)**: Completely decoupled and organization-neutral. Replaces all Blowhorn-specific identities, email addresses, and URLs with standardized placeholders (`<ORGANIZATION>`, `<PROJECT_NAME>`, `support@example.com`). Designed to be directly contributed to public upstream template registries or adopted by other organizations.
- **Structural Equivalence**: Both versions share identical workflow architectures, label taxonomies, issue forms, PR structures, and agent skills.

---

## 2. Organization-Specific vs. Generic Elements

| Dimension | Blowhorn Version (Root) | Upstream Version (`upstream/`) |
| :--- | :--- | :--- |
| **Organization Name** | `Blowhorn AI` | `<ORGANIZATION>` |
| **GitHub Organization** | `blowhorn-ai` | `<ORGANIZATION>` |
| **Project Name / Repo** | `repo-template` | `<PROJECT_NAME>` / `<REPO>` |
| **Support Email** | `support@blowhorn.ai` | `support@example.com` |
| **Security Email** | `security@blowhorn.ai` | `security@example.com` |
| **Community Email** | `community@blowhorn.ai` | `community@example.com` |
| **Discussions URL** | `https://github.com/blowhorn-ai/repo-template/discussions` | `https://github.com/<ORGANIZATION>/<REPO>/discussions` |
| **Default Image Target** | `ghcr.io/blowhorn-ai/repo-template` | `ghcr.io/<ORGANIZATION>/<PROJECT_NAME>` |
| **Community Footer** | *Blowhorn AI Community Automation* | *Community Automation* |

---

## 3. Complete File Comparison & Difference Matrix

Both implementations maintain an identical 32-file topology:

| Category | File Path | Differences Between Blowhorn & Upstream |
| :--- | :--- | :--- |
| **Root Docs** | `README.md` | Blowhorn branding vs generic project quickstart. |
| | `CONTRIBUTING.md` | Contact emails (`support@blowhorn.ai` vs `support@example.com`). |
| | `CODE_OF_CONDUCT.md` | Enforcement email (`community@blowhorn.ai` vs `community@example.com`). |
| | `SECURITY.md` | Disclosure email (`security@blowhorn.ai` vs `security@example.com`). |
| | `AGENTS.md` | Organization header (`Blowhorn AI` vs `<ORGANIZATION>`). |
| | `CLAUDE.md` | Identical (points to `AGENTS.md`). |
| | `LICENSE` | Identical (Apache 2.0). |
| **Docs** | `docs/workflow-policy.md` | Blowhorn-specific references vs generic platform guidelines. |
| | `docs/templates-and-labels.md` | Support contact details. |
| **Scripts** | `scripts/sync-labels.sh` | Identical logic (operates on relative `.github/labels.yml`). |
| **GitHub Config** | `.github/labels.yml` | Identical 37 canonical labels (including language/framework presets). |
| | `.github/labeler.yml` | Identical path glob rules. |
| | `.github/label-commenter-config.yml` | Blowhorn branding footer and contact links. |
| | `.github/release-drafter.yml` | Identical release drafter categories. |
| | `.github/stale.yml` | Identical stale triage thresholds. |
| | `.github/PULL_REQUEST_TEMPLATE.md`| Identical contributor PR checklist. |
| **Issue Templates**| `.github/ISSUE_TEMPLATE/bug_report.md` | Blowhorn title header vs generic. |
| | `.github/ISSUE_TEMPLATE/feature_request.md`| Blowhorn title header vs generic. |
| | `.github/ISSUE_TEMPLATE/documentation.md` | Identical fields. |
| | `.github/ISSUE_TEMPLATE/ci.md` | Identical fields. |
| | `.github/ISSUE_TEMPLATE/config.yml` | Contact links (`support@blowhorn.ai` vs `support@example.com`). |
| **Workflows** | `.github/workflows/ci.yml` | Identical verification structure. |
| | `.github/workflows/codeql-analysis.yml`| Identical security scanning workflow. |
| | `.github/workflows/slack.yml` | Identical safe Slack token check and degradation. |
| | `.github/workflows/labeler.yml` | Identical `actions/labeler@v5` configuration. |
| | `.github/workflows/label-commenter.yml`| Identical label commenter setup. |
| | `.github/workflows/release-drafter.yml`| Identical release drafter job. |
| | `.github/workflows/multi-platform.yml` | Default container tag/name placeholder. |
| **Agent Skills** | `.agents/skills/code-review/SKILL.md` | Identical review criteria. |
| | `.agents/skills/documentation/SKILL.md`| Identical documentation rules. |
| | `.agents/skills/repo-navigation/SKILL.md`| Identical navigation steps. |
| | `.agents/skills/testing/SKILL.md` | Identical testing guidance. |

---

## 4. Drift Prevention & Synchronization

To ensure the Blowhorn template and the upstream-ready version do not diverge over time, an automated synchronization check script is provided:

```bash
# Verify parity and check for organizational leaks in upstream/:
bash scripts/sync-upstream.sh --check
```

### Synchronization Protocol
1. **Source of Truth**: When updating workflows, issue templates, or skills, update the Blowhorn template at root first.
2. **Propagate to Upstream**: Apply corresponding changes to `upstream/`, replacing any Blowhorn-specific URLs or emails with the canonical placeholders.
3. **Run Parity Verification**: Execute `bash scripts/sync-upstream.sh --check` to confirm:
   - Every root template file has an exact upstream counterpart.
   - No occurrences of `blowhorn-ai`, `blowhorn.ai`, or `@blowhorn.ai` exist in `upstream/`.
4. **CI Integration**: Add `bash scripts/sync-upstream.sh --check` to CI to prevent pull requests from introducing unmirrored drift.

---

## 5. Upstream Contribution Prerequisites & Open Decisions

Before contributing `upstream/` to an external repository or public template catalog:

1. **License Selection**: Confirm whether upstream repositories require Apache 2.0 (current default) or MIT.
2. **Contact Placeholders**: Verify whether the upstream host project specifies its own security and code of conduct contact channels or prefers `<CONTACT_EMAIL>` placeholders.
3. **Default Branch Alignment**: Confirm whether upstream projects use `main` or `master` as their canonical default branch (the template workflows natively support both `main` and `master`).
4. **Container Registry**: The multi-platform build workflow defaults to GitHub Container Registry (`ghcr.io`); verify if upstream projects require Docker Hub (`docker.io`) examples.
