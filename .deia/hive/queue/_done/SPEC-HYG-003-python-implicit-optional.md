# SPEC-HYG-003-python-implicit-optional: Fix implicit Optional type annotations

## Priority
P2

## Depends On
None

## Model Assignment
sonnet

## Objective

Fix 39 implicit Optional violations (PEP 484) across hivenode/, simdecisions/, _tools/, and hodeia_auth/. Every function parameter typed as `def foo(x: str = None)` must be changed to `def foo(x: str | None = None)` using the modern union syntax. This resolves mypy `[assignment]` errors caused by incompatible default values and brings the codebase into PEP 484 compliance.

## Files to Read First

- .deia/reports/mypy.txt
- .deia/reports/code-hygiene-2026-04-12.md

## Acceptance Criteria

- [ ] Zero mypy `[assignment]` errors related to implicit Optional defaults in hivenode/
- [ ] Zero mypy `[assignment]` errors related to implicit Optional defaults in simdecisions/
- [ ] Zero mypy `[assignment]` errors related to implicit Optional defaults in _tools/
- [ ] Zero mypy `[assignment]` errors related to implicit Optional defaults in hodeia_auth/
- [ ] All changed signatures use `X | None = None` syntax (not `Optional[X] = None`)
- [ ] All existing Python tests still pass after changes
- [ ] No functional behavior changed — only type annotations updated

## Smoke Test

- [ ] Run `python -m mypy hivenode/ simdecisions/ _tools/ hodeia_auth/ 2>&1 | grep "Incompatible default"` and confirm zero matches related to None defaults
- [ ] Run `python -m pytest tests/ -x -q` and confirm all tests pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `python -m mypy` to verify fixes
- Use `X | None` union syntax, not `Optional[X]` from typing
- Do not add `from __future__ import annotations` unless the file already has it
- Do not change any runtime behavior — only type annotations
