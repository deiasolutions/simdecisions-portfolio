# SPEC-HYG-004-python-dead-code: Remove dead code identified by vulture

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Remove 15 dead code imports and 3 redefined-while-unused (F811) violations identified by vulture and ruff. Each removal must be verified to not break any imports, re-exports, or test dependencies before deletion. This reduces codebase noise and eliminates misleading symbols.

## Files to Read First

- .deia/reports/vulture.txt
- .deia/reports/code-hygiene-2026-04-12.md

## Acceptance Criteria

- [ ] All 15 dead imports identified in vulture.txt are removed (or explicitly marked with justification if kept)
- [ ] All 3 F811 redefined-while-unused violations are resolved
- [ ] `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/ --select F811` reports zero violations
- [ ] No import errors when running `python -c "import hivenode; import simdecisions"`
- [ ] All existing Python tests still pass after changes

## Smoke Test

- [ ] Run `ruff check hivenode/ simdecisions/ _tools/ hodeia_auth/ tests/ --select F811` and confirm zero violations
- [ ] Run `python -m pytest tests/ -x -q` and confirm all tests pass
- [ ] Run `python -c "import hivenode.main; import simdecisions"` and confirm no import errors

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `ruff check` to verify fixes
- Before removing any import, grep the codebase to confirm it is not used as a re-export
- If an import is used as a public API re-export, keep it and add `# noqa: F401`
