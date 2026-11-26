# Repository Guidance for Coding Agents

This document defines repository conventions, development rules, and verification standards for autonomous AI agents and contributors working in Blowhorn AI repositories.

## 1. Project Overview

- **Organization**: Blowhorn AI
- **Repository**: Repository Template (`blowhorn-ai/repo-template`)
- **Default Branch**: `master` (Note: While this repository uses `master`, template consumers may adopt either `main` or `master` as their primary branch; template workflows support both).
- **Architecture**: Reusable repository template providing GitHub Actions workflows, issue templates, issue labels, and agent skills.

## 2. Setup and Verification

When adapting this repository for a new project, configure the real commands below:

- **Install Dependencies**: `npm install` / `pip install -r requirements.txt` / `go mod download`
- **Lint & Format**: `npm run lint` / `flake8` / `golangci-lint run`
- **Run Tests**: `npm test` / `pytest` / `go test ./...`
- **Build**: `npm run build` / `go build ./...`

> **Agent Rule**: Never claim a check passed unless you ran the command and observed a successful exit code and output.

## 3. Working Rules

1. **Scope Discipline**: Keep changes strictly focused on the requested task. Do not execute unsolicited broad refactorings or reformat unrelated files.
2. **Read Skills First**: Review the corresponding skill in `.agents/skills/` before performing code review, documentation changes, testing, or repository exploration.
3. **Secret Safety**: Never commit credentials, API keys, tokens, or personal identifiers. Use environment variables or documented configuration placeholders.
4. **Documentation Sync**: Whenever user-facing interfaces, configuration parameters, or CLI flags change, immediately update the relevant documentation.
5. **No Hallucinated Commands**: Only reference and invoke tools, commands, or packages verified to exist in the environment.

## 4. Agent Skills

- **`code-review`** ([`.agents/skills/code-review/SKILL.md`](.agents/skills/code-review/SKILL.md)): Systematically evaluates pull requests and changes for correctness, security, regressions, test coverage, and documentation.
- **`documentation`** ([`.agents/skills/documentation/SKILL.md`](.agents/skills/documentation/SKILL.md)): Maintains accurate single-source-of-truth documentation without duplicating content.
- **`repo-navigation`** ([`.agents/skills/repo-navigation/SKILL.md`](.agents/skills/repo-navigation/SKILL.md)): Explores unfamiliar codebases, identifies entry points, and locates code ownership.
- **`testing`** ([`.agents/skills/testing/SKILL.md`](.agents/skills/testing/SKILL.md)): Designs, executes, and reports verifiable behavior tests.
