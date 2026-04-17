## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

---
id: SPEC-CODE-HYGIENE-001
title: Repo Code Hygiene Audit
version: 0.1.0
status: ready
author: Q88N
created: 2026-04-12
depends_on: []
dispatch_to: BEE
priority: P1
---

## Purpose

Identify dead code, lint violations, unused dependencies, and integration issues across the simdecisions monorepo (Python + JS/TS).

## Scope

Directories to analyze:
- `hivenode/`
- `simdecisions/`
- `_tools/`
- `browser/`
- `hodeia_auth/`

## Tools Required

| Language | Tool | Install | Function |
|----------|------|---------|----------|
| Python | vulture | `pip install vulture` | Dead code detection |
| Python | ruff | `pip install ruff` | Linting, style |
| Python | mypy | `pip install mypy` | Type/integration issues |
| JS/TS | knip | `npm install -g knip` | Dead exports, unused deps, stranded files |
| JS/TS | tsc | (bundled with typescript) | Type-based integration check |

## Execution

```bash
# Python analysis
vulture hivenode/ simdecisions/ _tools/ hodeia_auth/ --min-confidence 80 > .deia/reports/vulture.txt
ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ --output-format=json > .deia/reports/ruff.json
mypy hivenode/ simdecisions/ _tools/ hodeia_auth/ --ignore-missing-imports > .deia/reports/mypy.txt

# JS/TS analysis
cd browser/
npx knip --reporter json > ../.deia/reports/knip.json
npx tsc --noEmit 2>&1 > ../.deia/reports/tsc.txt
```

## Acceptance Criteria

- [ ] vulture report generated, reviewed for false positives
- [ ] ruff check with zero critical violations or documented exceptions
- [ ] mypy report generated, critical type errors catalogued
- [ ] knip report generated for browser/ and any JS/TS service dirs
- [ ] tsc --noEmit passes or violations catalogued
- [ ] Consolidated summary in `.deia/reports/code-hygiene-2026-04-12.md`

## Output Format

Consolidated report should include:

1. **Dead Code** — list of unreachable functions/classes/variables with file:line
2. **Lint Violations** — grouped by severity (error, warning, info)
3. **Type Issues** — mismatched signatures, missing attributes
4. **Unused Dependencies** — npm and pip packages installed but never imported
5. **Stranded Files** — files that exist but are never imported/referenced

## Whitelisting

Create whitelist files as needed for:
- CLI entry points (`if __name__ == "__main__"`)
- Test fixtures
- Framework convention files (e.g., `__init__.py`, `index.ts`)
- Intentionally unused exports (public API surface)

Whitelist location: `.deia/config/hygiene-whitelist.txt`

## Smoke Test

```bash
# Quick validation that tools are installed and runnable
vulture --version
ruff --version
mypy --version
npx knip --version
npx tsc --version
```

## Notes

- Run from repo root
- Expect noise on first run; triage into real issues vs. false positives
- Results feed into technical debt backlog

## Triage History
- 2026-04-12T22:28:11.830651Z — requeued (empty output)
- 2026-04-12T22:33:11.836075Z — requeued (empty output)
- 2026-04-12T22:38:11.842323Z — requeued (empty output)
