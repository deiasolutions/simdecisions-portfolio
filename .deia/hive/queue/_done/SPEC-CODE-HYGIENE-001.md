# SPEC-CODE-HYGIENE-001: Repo Code Hygiene Audit

**MODE: EXECUTE**

**Spec ID:** SPEC-CODE-HYGIENE-001
**Created:** 2026-04-12
**Author:** Q88N
**Status:** READY

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

---

## Purpose

Identify dead code, lint violations, unused dependencies, and integration issues
across the simdecisions monorepo (Python + JS/TS) after the repo flatten from
`packages/*/src/` to top-level directories.

---

## Files to Read First

- `pyproject.toml` — Python project config, dependencies, pythonpath setting
- `browser/package.json` — JS/TS dependencies
- `hivenode/__init__.py` — top-level Python package entry
- `simdecisions/__init__.py` — engine package entry
- `_tools/__init__.py` — tools package entry

## Scope

Directories to analyze:

| Directory | Language | What it contains |
|-----------|----------|------------------|
| `hivenode/` | Python | FastAPI backend, scheduler, routes, relay, ledger |
| `simdecisions/` | Python | Simulation engine (DES, optimization, Phase-IR) |
| `_tools/` | Python | Dev tooling (inventory, estimates, restart scripts) |
| `hodeia_auth/` | Python | Auth service (standalone Railway deploy) |
| `browser/src/` | TypeScript/React | Frontend app, adapters, primitives, shell |

## Tools Required

| Language | Tool | Install | Function |
|----------|------|---------|----------|
| Python | vulture | `pip install vulture` | Dead code detection |
| Python | ruff | `pip install ruff` | Linting, style |
| Python | mypy | `pip install mypy` | Type/integration issues |
| JS/TS | knip | `npx knip` | Dead exports, unused deps, stranded files |
| JS/TS | tsc | (bundled) | Type-based integration check |

## Execution

Run all commands from repo root.

```bash
# Step 1: Verify tools are installed
vulture --version
ruff --version
mypy --version
npx tsc --version

# Step 2: Create reports directory
mkdir -p .deia/reports

# Step 3: Python — dead code detection
vulture hivenode/ simdecisions/ _tools/ hodeia_auth/ --min-confidence 80 > .deia/reports/vulture.txt

# Step 4: Python — lint check
ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ --output-format=json > .deia/reports/ruff.json

# Step 5: Python — type check
mypy hivenode/ simdecisions/ _tools/ hodeia_auth/ --ignore-missing-imports > .deia/reports/mypy.txt

# Step 6: JS/TS — dead exports and unused deps
cd browser && npx knip --reporter json > ../.deia/reports/knip.json && cd ..

# Step 7: JS/TS — type check
cd browser && npx tsc --noEmit 2>&1 > ../.deia/reports/tsc.txt && cd ..
```

## Acceptance Criteria

- [ ] All 5 tools run without crashing (install missing tools if needed)
- [ ] `vulture.txt` generated — reviewed for false positives, real dead code catalogued with file:line
- [ ] `ruff.json` generated — zero critical violations or documented exceptions
- [ ] `mypy.txt` generated — critical type errors catalogued separately from noise
- [ ] `knip.json` generated — unused exports, stranded files, unused dependencies listed
- [ ] `tsc.txt` generated — TypeScript errors catalogued (pre-existing vs new)
- [ ] Consolidated summary written to `.deia/reports/code-hygiene-2026-04-12.md`
- [ ] Summary includes all 5 sections: Dead Code, Lint Violations, Type Issues, Unused Dependencies, Stranded Files
- [ ] Each finding includes file path and line number where applicable
- [ ] False positives triaged and added to `.deia/config/hygiene-whitelist.txt`

## Output Format

Consolidated report (`.deia/reports/code-hygiene-2026-04-12.md`) must include:

1. **Dead Code** — unreachable functions/classes/variables with `file:line`
2. **Lint Violations** — grouped by severity (error, warning, info), count per category
3. **Type Issues** — mismatched signatures, missing attributes, with `file:line`
4. **Unused Dependencies** — npm and pip packages installed but never imported
5. **Stranded Files** — files that exist but are never imported or referenced

## Whitelisting

Create `.deia/config/hygiene-whitelist.txt` for known false positives:
- CLI entry points (`if __name__ == "__main__"`)
- Test fixtures and conftest.py files
- Framework convention files (`__init__.py`, `index.ts`)
- Intentionally unused public API exports
- `.deia/hive/scripts/` — queue runner internals (non-standard import patterns)

## Constraints

- No code changes — this is audit only
- No git operations
- Do not delete or modify any source files
- Report noise honestly — first run will have false positives, that's expected
- Results feed into technical debt backlog for future cleanup specs

## Response File

`.deia/hive/responses/20260412-SPEC-CODE-HYGIENE-001-RESPONSE.md`

---

*SPEC-CODE-HYGIENE-001 — Q88N — 2026-04-12*
