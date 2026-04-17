# Briefing: TASK-227 LLM Triage Functions

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-17
**Spec:** TASK-227 — LLM Triage Functions (W3-B)
**Model Assignment:** Sonnet

---

## Objective

Implement three LLM triage functions that add intelligence to the directory state machine: crash recovery triage, failure diagnosis, and completion validation.

---

## Context

This is part of **SPEC-PIPELINE-001** (Unified Build Pipeline), Section 5 — LLM Triage Layer.

These functions use cheap Haiku calls (~$0.01-0.03 per call) to make smart routing decisions instead of blind retries. They integrate into the queue runner's state machine at three critical decision points:

1. **Crash recovery** — when runner finds orphaned work in `_active/` on startup
2. **Failure diagnosis** — when a bee returns error/timeout
3. **Completion validation** — before moving spec to `_done/` (advisory only in Phase 1)

The **holdout principle** is critical: the reviewing LLM must NEVER be the same model/session that did the work.

---

## Dependencies

- **TASK-224** (directory state machine) — COMPLETE (in `_done/`, though there's a P0 fix spec pending)
  - The state machine transitions exist in `run_queue.py`
  - Orphan scan logic exists
  - `_active/`, `_done/`, `_failed/`, `_needs_review/` directories in use

**Dependency Status:** SATISFIED (fix spec won't block this work — triage functions are new additions, not refactoring existing code)

---

## Source Files to Read

Before writing task files, read these:

1. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`**
   Section 5 (LLM Triage Layer) — describes the three triage points, inputs, outputs, verdicts, routing logic

2. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`**
   Lines 1-200 minimum — understand where triage will be called (orphan scan, failure handling, completion)

3. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py`**
   Lines 1-150 minimum — bee dispatch/completion handling, where results come back

4. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\filesystem_store.py`**
   To understand the PipelineStore interface (already implemented per TASK-222)

5. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\ledger_events.py`**
   To understand how to emit events (already implemented per TASK-223)

---

## Deliverables from Spec

The spec lists these deliverables:

1. **Create `.deia/hive/scripts/queue/triage.py`** with three functions:
   - `triage_crash_recovery(spec, diff, tests) -> CrashVerdict`
   - `triage_failure(spec, response, errors) -> FailureClassification`
   - `validate_completion(spec, diff, tests) -> CompletionReview`

2. **Wire triage functions into state machine** (in `run_queue.py`):
   - Call `triage_crash_recovery` during orphan scan
   - Call `triage_failure` when bee returns error/timeout
   - Call `validate_completion` before moving to `_done/`

3. **Create tests** in `.deia/hive/scripts/queue/tests/test_triage.py`:
   - Test each function returns correct verdict type
   - Test routing logic for each verdict
   - Mock LLM calls (no real API calls)
   - Minimum 10 tests

---

## Key Constraints

1. **TDD** — tests first, then implementation (Rule 5)
2. **No files over 500 lines** — modularize if needed (Rule 4)
3. **No stubs** — every function fully implemented (Rule 6)
4. **Holdout principle** — triage LLM must NOT be same session as the bee being reviewed
5. **Phase 1 advisory mode** — `validate_completion` logs review but does NOT gate (spec Section 5.3)
6. **Mock LLM calls in tests** — do not hit real Anthropic API during test runs
7. **Absolute paths** in task files (Rule 8)
8. **LLM dispatch mechanism** — need to determine how to call Haiku from Python (subprocess? HTTP API? direct SDK?)

---

## Technical Decisions Needed

**Q33N, please investigate and decide:**

1. **How to dispatch Haiku calls from triage.py?**
   - Options: subprocess via dispatch.py, direct Anthropic SDK, HTTP to hivenode LLM proxy
   - Requirement: must be lightweight (<1s overhead), mockable for tests
   - Check existing code in hivenode for LLM call patterns

2. **What Git command to use for `git diff` in crash recovery?**
   - Needs to capture changes since bee session started
   - Manifest has `started_at` timestamp — use `git diff HEAD@{timestamp}` or similar?

3. **How to access test output in crash recovery?**
   - Does queue runner capture pytest output to a file?
   - If not, should triage run tests itself or work without test data?

4. **What return types for each function?**
   - Enums? Dataclasses? NamedTuples?
   - Need to be serializable for logging to ledger

---

## Integration Points

Based on spec Section 5, wire these calls:

### 1. Crash Recovery (Section 5.1)

**Location:** `run_queue.py` — orphan scan on startup
**Trigger:** Spec found in `_active/` with no running process
**Inputs:**
- Spec file content
- Manifest (bee_id, session_id, started_at, pid)
- `git diff` since session start
- Test output (if available)

**Verdicts → Actions:**
- `COMPLETE_ENOUGH` → commit diff, move to `_done/`, note recovered
- `PARTIAL_SAFE` → keep diff, generate continuation spec, move original to `_done/` with partial flag
- `REVERT` → `git checkout` changed files, move spec back to `queue/` for retry

### 2. Failure Diagnosis (Section 5.2)

**Location:** `run_queue.py` — after bee returns
**Trigger:** Bee returns NEEDS_DAVE or error
**Inputs:**
- Spec content
- Response file
- Error output
- Test results

**Classifications → Routes:**
- `AMBIGUOUS_SPEC` → `_needs_review/` (human rewrites)
- `CODING_ERROR` → generate fix spec in `queue/`
- `DEPENDENCY_ISSUE` → block on upstream dep, move to `queue/` with dep added
- `ENVIRONMENT_ISSUE` → `_needs_review/` with env tag

### 3. Completion Validation (Section 5.3)

**Location:** `run_queue.py` — before moving to `_done/`
**Trigger:** Bee reports CLEAN
**Inputs:**
- Spec acceptance criteria
- `git diff`
- Test results

**Phase 1 behavior:** Log review, do NOT gate. Always allow move to `_done/`.

---

## Success Criteria

The work is done when:

1. **`triage.py` exists** with all three functions fully implemented
2. **Tests exist** in `test_triage.py` with ≥10 tests, all passing
3. **Integration wired** — `run_queue.py` calls triage functions at the three integration points
4. **LLM calls are mocked** in tests (no real API calls during test runs)
5. **Events logged** — each triage call emits to ledger with verdict, tokens, cost
6. **No stubs** — every code path has real logic
7. **All existing queue tests still pass** (no regressions)

---

## Notes

- **Cost model:** Each triage call ~$0.01-0.03 (Haiku). At 10% failure rate on 50 specs/day = 5 calls = $0.05-0.15/day. Trivial vs. cost of re-running full Sonnet bee.
- **Existing patterns:** Check `ledger_events.py` for event emission patterns. Check `filesystem_store.py` for how queue runner interacts with state.
- **TASK-224 fix pending:** The fix spec for TASK-224 is P0 in queue, but it's about dispatch role detection, not state machine logic. This work can proceed in parallel.

---

## Task File Instructions for Q33N

Write ONE task file for a Sonnet bee:

**File:** `.deia/hive/tasks/2026-03-17-TASK-227-llm-triage-functions.md`

Include:
- Absolute Windows paths for all files
- TDD requirement explicit
- Minimum 10 tests
- All three triage functions with correct signatures
- Integration points clearly specified
- Mock LLM calls requirement
- Response file template (8 sections)

**Do NOT break this into multiple tasks** — it's a cohesive unit of work (three related functions + integration + tests).

---

**Q33NR awaits your task file for review.**
