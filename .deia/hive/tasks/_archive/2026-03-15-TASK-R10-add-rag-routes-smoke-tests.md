# TASK-R10: Add 2 smoke tests to RAG routes test file

**Priority:** P0.50
**Original:** TASK-163 (RAG routes smoke test)
**Rebuild Batch:** 02
**Date:** 2026-03-15

---

## Objective

Restore two test methods added to `tests/hivenode/rag/test_rag_routes.py` that were lost in the git reset.

---

## Context

After `git reset --hard HEAD`, the test file `tests/hivenode/rag/test_rag_routes.py` survived (it was already tracked), but two new test methods added in TASK-163 were lost:
- `test_query_endpoint_exists` — verifies `/query` endpoint responds
- `test_query_missing_query_param` — validates required query parameter

These tests were added to a new `TestQueryRoute` class in the existing test file.

**Dependencies:**
- This task is INDEPENDENT of other rebuild tasks (test file changes only)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_rag_routes.py` (current state — missing 2 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-163-RESPONSE.md` (original smoke test details)

---

## Deliverables

### 1. Add `TestQueryRoute` Class with 2 Tests

Add this class to the test file (after existing test classes):

```python
class TestQueryRoute:
    """Smoke tests for POST /rag/query endpoint."""

    def test_query_endpoint_exists(self, client):
        """Test that /query endpoint responds (200 or 503 if synthesizer unavailable)."""
        response = client.post("/rag/query", json={"query": "test query"})
        # Accept 200 (success) or 503 (service unavailable — embedder not ready)
        assert response.status_code in [200, 503], f"Expected 200 or 503, got {response.status_code}"

    def test_query_missing_query_param(self, client):
        """Test that missing query parameter returns validation error."""
        response = client.post("/rag/query", json={})
        # Expect 422 (Pydantic validation) or 400 (custom validation)
        assert response.status_code in [422, 400], f"Expected 422 or 400, got {response.status_code}"
```

### 2. Verify Test Class Placement

- [ ] Place `TestQueryRoute` class AFTER existing test classes
- [ ] Maintain consistent indentation and style with existing tests
- [ ] Use same `client` fixture as other tests

---

## Test Requirements

### Tests Written FIRST (TDD)
- [ ] Read existing test file structure first
- [ ] Add 2 new test methods to `TestQueryRoute` class
- [ ] Follow existing test patterns (same fixtures, same assertions)

### All Tests Pass
- [ ] Run: `python -m pytest tests/hivenode/rag/test_rag_routes.py -v`
- [ ] Expected: **14 total tests PASSING** (12 existing + 2 new)

### Test Breakdown
- [ ] `TestStatusRoute` — 1 test (existing)
- [ ] `TestIndexRoute` — 2 tests (existing)
- [ ] `TestIngestChatRoute` — 2 tests (existing)
- [ ] `TestSearchRoute` — 4 tests (existing)
- [ ] `TestResetRoute` — 1 test (existing)
- [ ] `TestQueryRoute` — 2 tests (NEW — this task)
- [ ] `TestEmbedderUnavailable` — 2 tests (existing)

---

## Constraints

- No file over 500 lines (test file is currently ~300 lines — well within limits)
- No stubs (test methods must be fully implemented)
- Follow existing test patterns exactly (same fixtures, same assertion style)
- Do NOT modify existing tests — only add new `TestQueryRoute` class

---

## Acceptance Criteria

- [x] `TestQueryRoute` class added to test file
- [x] `test_query_endpoint_exists` method added (accepts 200 or 503)
- [x] `test_query_missing_query_param` method added (expects 422 or 400)
- [x] All 14 tests pass (12 existing + 2 new)
- [x] No test file over 500 lines
- [x] Consistent style with existing tests

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R10-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts (show all 14 tests)
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

**Model Assignment:** Haiku (simple test addition)
**Estimated Duration:** 5 minutes
**Depends On:** None (independent test file change)
