---
name: testing
description: Use when adding or changing tests, selecting verification commands, or reporting test evidence.
---

# Testing guidance

1. Find the project's documented test commands and existing test conventions.
2. Prefer tests that exercise public behavior and meaningful failure cases.
3. Do not use source-text grep tests as a substitute for behavior tests.
4. Run the narrowest relevant test first, then broader checks when practical.
5. Report exactly what ran, what passed, and what was not run.
