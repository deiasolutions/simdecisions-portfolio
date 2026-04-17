# TASK-CLOUD-STORAGE-E: Cloud Storage Smoke Test & Regression Check

## Objective

Run smoke tests for cloud storage (all new tests pass) and regression tests (existing hivenode tests still pass). Verify no regressions introduced by cloud storage implementation.

---

## Context

TASK-A, TASK-B, and TASK-C created cloud storage store, routes, and integration tests. This task verifies:

1. All new cloud storage tests pass
2. No regressions in existing hivenode tests
3. Smoke test script for quick validation

This is a validation task, not a coding task. If failures occur, diagnose and fix (or report for follow-up).

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cloud_store.py` — TASK-A tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_cloud_storage_routes.py` — TASK-B tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cloud_storage_integration.py` — TASK-C tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\` — all hivenode source

---

## Deliverables

- [ ] Smoke test script: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_cloud_storage.sh`
- [ ] All new cloud storage tests pass (minimum 46 tests: 18 + 20 + 8)
- [ ] All existing hivenode tests pass (no regressions)
- [ ] Test summary report in response file

---

## Test Commands

### New Cloud Storage Tests

```bash
# Store tests (TASK-A)
cd hivenode && python -m pytest tests/hivenode/test_cloud_store.py -v

# Route tests (TASK-B)
cd hivenode && python -m pytest tests/hivenode/routes/test_cloud_storage_routes.py -v

# Integration tests (TASK-C)
cd hivenode && python -m pytest tests/hivenode/test_cloud_storage_integration.py -v
```

### Regression Tests (Existing Hivenode Tests)

```bash
# Full hivenode test suite
cd hivenode && python -m pytest tests/ -v
```

### Smoke Test Script

Create `_tools/smoke_test_cloud_storage.sh`:

```bash
#!/bin/bash
set -e

echo "=== Cloud Storage Smoke Test ==="
echo ""

echo "1. Running cloud store tests..."
cd hivenode && python -m pytest tests/hivenode/test_cloud_store.py -v --tb=short
echo "✓ Cloud store tests passed"
echo ""

echo "2. Running cloud storage route tests..."
cd hivenode && python -m pytest tests/hivenode/routes/test_cloud_storage_routes.py -v --tb=short
echo "✓ Cloud storage route tests passed"
echo ""

echo "3. Running cloud storage integration tests..."
cd hivenode && python -m pytest tests/hivenode/test_cloud_storage_integration.py -v --tb=short
echo "✓ Cloud storage integration tests passed"
echo ""

echo "4. Running regression tests (existing hivenode tests)..."
cd hivenode && python -m pytest tests/ -v --tb=short -k "not cloud_storage"
echo "✓ Regression tests passed"
echo ""

echo "=== All Cloud Storage Tests Passed ==="
```

---

## Expected Results

### New Tests (Minimum Counts)

- `test_cloud_store.py`: **18+ tests passing**
- `test_cloud_storage_routes.py`: **20+ tests passing**
- `test_cloud_storage_integration.py`: **8+ tests passing**
- **Total new tests:** 46+ passing

### Existing Tests (Regression)

All existing hivenode tests should pass. Current count from MEMORY.md:

- Hivenode: **969 tests passing**
- After cloud storage: **969 + 46 = 1,015+ tests passing**

### Failure Handling

If ANY test fails:

1. **Diagnose:** Read failure output, identify root cause
2. **Fix:** Correct the issue in source code
3. **Re-run:** Verify fix resolves failure
4. **Report:** Document fix in response file

Common issues:

- **Import errors:** Missing module imports, incorrect paths
- **Database connection:** PostgreSQL not available (use SQLite for tests via `DATABASE_URL=sqlite:///...`)
- **JWT mocking:** `verify_jwt()` not properly mocked in tests
- **Route conflicts:** Both `storage_routes` and `cloud_storage_routes` registered (should be conditional)

---

## Constraints

- **All tests must pass:** No skipped tests, no failures
- **Regression tests:** Existing tests must not break
- **Smoke test script:** Executable bash script in `_tools/`
- **Report failures:** If unfixable, document in response file with root cause analysis

---

## Acceptance Criteria

- [ ] Smoke test script created: `_tools/smoke_test_cloud_storage.sh`
- [ ] All 18+ store tests pass
- [ ] All 20+ route tests pass
- [ ] All 8+ integration tests pass
- [ ] All existing hivenode tests pass (969+ tests)
- [ ] Total: 1,015+ tests passing (969 existing + 46 new)
- [ ] No regressions
- [ ] If failures occur: root cause identified and documented

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-CLOUD-STORAGE-E-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — smoke test script path
3. **What Was Done** — bullet list of tests run
4. **Test Results** — DETAILED: list each test file with pass/fail counts
5. **Build Verification** — full test suite output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any failures, root causes, fixes applied

DO NOT skip any section.

**CRITICAL:** Test Results section must include:
- `test_cloud_store.py`: X passed
- `test_cloud_storage_routes.py`: X passed
- `test_cloud_storage_integration.py`: X passed
- Existing tests: X passed
- Total: X passed

---

## Dependencies

- **TASK-CLOUD-STORAGE-A** (store) must complete first
- **TASK-CLOUD-STORAGE-B** (routes) must complete first
- **TASK-CLOUD-STORAGE-C** (integration) must complete first

---

## Test Command

```bash
# Run smoke test script
bash _tools/smoke_test_cloud_storage.sh
```
