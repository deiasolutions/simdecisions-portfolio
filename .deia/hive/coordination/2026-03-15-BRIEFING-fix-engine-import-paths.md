# BRIEFING: Fix Engine Import Paths (WAVE0-02)

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-15
**Spec:** `.deia/hive/queue/2026-03-15-WAVE0-02-SPEC-fix-engine-import-paths.md`
**Model Assignment:** haiku

---

## Objective

Fix import path errors in `tests/engine/des/test_des_ledger_emission.py` which is importing from the old platform path `src.simdecisions.runtime.ledger` instead of the correct shiftcenter path `engine`.

---

## Context

This is part of WAVE0 cleanup — fixing residual import paths from the platform port. The engine module was ported from `platform/efemera/src/efemera/` to `engine/` in shiftcenter, but some test files still reference the old paths.

The file in question is:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\des\test_des_ledger_emission.py`

---

## Acceptance Criteria from Spec

- [ ] `test_des_ledger_emission.py` imports from correct paths (engine module, not src.simdecisions)
- [ ] All engine tests collect without import errors
- [ ] All engine tests pass (or existing failures are documented)

---

## Constraints

- **TDD:** Run tests before and after fix
- **No stubs**
- **Max 500 lines per file**
- **Only fix import paths** — do not refactor other code

---

## Smoke Test

- [ ] `python -m pytest tests/engine/ -v` runs without import errors
- [ ] No new test failures introduced

---

## Files to Reference

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\des\test_des_ledger_emission.py` (file to fix)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\` (correct import root)

---

## Instructions for Q33N

1. Read the test file to understand current imports
2. Read the engine module structure to understand correct import paths
3. Write ONE task file for a bee (haiku model)
4. The task should be simple: fix imports, run tests, verify no regressions
5. Return the task file for my review before dispatching

---

## Expected Deliverable from Q33N

One task file in `.deia/hive/tasks/` with:
- Absolute file paths
- Clear test requirements (before/after test runs)
- 8-section response file requirement
- No CSS (not applicable)
- No file size concerns (this is a simple import fix)

---

**Do NOT dispatch bees yet. Return the task file to me (Q33NR) for review first.**
