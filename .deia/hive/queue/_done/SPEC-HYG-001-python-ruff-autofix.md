# SPEC-HYG-001-python-ruff-autofix: Auto-fix Python lint violations with ruff

## Priority
P2

## Depends On
None

## Model Assignment
sonnet

## Objective

Run `ruff check --fix` across all Python code in hivenode/, simdecisions/, _tools/, hodeia_auth/, and tests/ to auto-fix 313 unused imports (F401), 46 f-strings missing placeholders (F541), 36 unused variables (F841), 9 multi-imports (E401), 3 bare excepts (E722), and 2 none comparisons (E711). Verify all existing tests still pass after the auto-fix, then manually review and fix any remaining violations that ruff cannot auto-fix.

## Files to Read First

- .deia/reports/code-hygiene-2026-04-12.md
- .deia/reports/ruff.json

## Acceptance Criteria

- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/` reports zero F401 violations
- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/` reports zero F541 violations
- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/` reports zero F841 violations
- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/` reports zero E401 violations
- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/` reports zero E722 violations
- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/` reports zero E711 violations
- [ ] All existing Python tests still pass after changes
- [ ] No functional behavior changed (only lint cleanup)

## Smoke Test

- [ ] Run `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/ --select F401,F541,F841,E401,E722,E711` and confirm zero violations
- [ ] Run `python -m pytest tests/ -x -q` and confirm all tests pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `ruff check` to verify fixes
- Do not change any functional logic — only remove unused imports, fix lint issues
- If removing an import breaks a re-export, keep the import and add a `# noqa: F401` comment
