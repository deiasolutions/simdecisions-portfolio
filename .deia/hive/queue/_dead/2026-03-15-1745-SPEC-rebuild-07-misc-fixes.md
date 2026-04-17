# SPEC: Rebuild miscellaneous small fixes (pyproject, main.py, test selectors, mocks)

## Priority
P0.35

## Model Assignment
haiku

## Objective
Re-apply 4 small fixes from various tasks lost in a git reset.

### Fix 1: pyproject.toml (TASK-132)
Add `"engine.des"` to the setuptools packages list (around line 53).

### Fix 2: tests/engine/des/test_des_ledger_emission.py (TASK-132)
Replace old platform imports with a MockLedger class. The test file needs to work without platform dependencies.

### Fix 3: hivenode/main.py (TASK-126A)
Enhance inventory store initialization with try/except and logging (around lines 187-204).

### Fix 4: browser/.../FileOperations.test.tsx (TASK-139)
Restructure CloudAPIClient mock in `browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx` (lines 37-61). The mock pattern uses `vi.fn(() => mockClient)`.

## Recovery Sources
- `.deia/hive/responses/20260315-TASK-132-RESPONSE.md` (fixes 1 + 2)
- `.deia/hive/responses/20260315-TASK-126A-RESPONSE.md` (fix 3)
- `.deia/hive/responses/20260315-TASK-139-RESPONSE.md` (fix 4)

## Acceptance Criteria
- [ ] `python -c "import engine.des"` works (pyproject fix)
- [ ] `python -m pytest tests/engine/des/test_des_ledger_emission.py -v` passes
- [ ] hivenode starts without inventory store errors
- [ ] `cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx` — all 57 tests pass
- [ ] No regressions

## Constraints
- Max 500 lines per file
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-07-misc-fixes", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-07-misc-fixes", "files": ["pyproject.toml", "tests/engine/des/test_des_ledger_emission.py", "hivenode/main.py", "browser/src/apps/sim/components/flow-designer/__tests__/FileOperations.test.tsx"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
