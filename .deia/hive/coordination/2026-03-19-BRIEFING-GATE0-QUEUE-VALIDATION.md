# Briefing: Gate 0 Programmatic Validation for Queue Runner

**Date:** 2026-03-19
**From:** Q88NR (Regent-Bot)
**To:** Q33N (Queen Coordinator)
**Priority:** P0 (process integrity fix)
**Model Assignment:** Sonnet (complex logic + TDD)

---

## Objective

Add a **programmatic Gate 0 validation step** to the queue runner that checks spec quality BEFORE dispatching to the regent bot. This prevents incoherent specs from reaching bees.

Currently the queue runner dispatches specs directly to regent bots with zero validation. This spec implements the **minimum viable Gate 0** from PROCESS-0013 — coverage and coherence checks only (no IR fidelity).

---

## Context

### The Problem
- Queue runner currently has NO spec validation before dispatch
- Incoherent specs (contradictory deliverables vs acceptance criteria) reach bees
- Q33NR review exists only as a prompt instruction (gets rubber-stamped)
- Need a real code-level gate

### The Solution
From **PROCESS-0013** (`.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md`):
- Gate 0: Coverage/coherence validation
- Phase 0: Requirement coverage (FUTURE)
- Phase 1: SPEC fidelity via IR (FUTURE)
- Phase 2: TASK fidelity via IR (FUTURE)

**This task implements Gate 0 ONLY** — the minimum checks before dispatch.

### Integration Point
- Queue runner: `.deia/hive/scripts/queue/run_queue.py`
- Spec processor: `.deia/hive/scripts/queue/spec_processor.py`
- Spec parser: `.deia/hive/scripts/queue/spec_parser.py`

Gate 0 runs in `process_spec()` BEFORE `handler.call_dispatch()`.

---

## What Gate 0 Must Check

Run AFTER spec load, BEFORE dispatch. This is a **code function**, not a prompt.

### Required Checks (all must pass):

1. **Deliverables vs Acceptance Criteria Coherence**
   - If spec says "fix X" in acceptance criteria, deliverables must not say "DO NOT modify X"
   - Flag contradictions

2. **File Paths Exist**
   - Every file path in "Files to Read First" or "Files to Modify" must exist on disk
   - Flag missing files

3. **Scope Sanity**
   - If spec references a source file bug, it must allow modification of that file
   - A spec that identifies a bug location but forbids editing = incoherent

4. **Priority Present**
   - Spec must have P0/P1/P2/P3 priority
   - Missing priority = reject

5. **Acceptance Criteria Present**
   - Spec must have at least one acceptance criterion
   - No criteria = reject

### What Gate 0 Does NOT Do
- IR fidelity round-trip (Phase 1/2 — future)
- LLM-based requirement extraction (future)
- Embedding similarity (future)
- Traceability graph (future)

---

## Deliverables

### New File: `.deia/hive/scripts/queue/gate0.py`
The Gate 0 validation module.

**Required Functions:**
```python
def validate_spec(spec: SpecFile, repo_root: Path) -> Gate0Result:
    """Run all Gate 0 checks on a spec."""

@dataclass
class Gate0Result:
    passed: bool
    checks: list[CheckResult]
    summary: str

@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
```

**Each check is a separate function** (testable independently):
- `check_priority(spec) -> CheckResult`
- `check_acceptance_criteria(spec) -> CheckResult`
- `check_file_paths_exist(spec, repo_root) -> CheckResult`
- `check_deliverables_coherence(spec) -> CheckResult`
- `check_scope_sanity(spec) -> CheckResult`

### Integration: `spec_processor.py`
Call `validate_spec()` BEFORE `handler.call_dispatch()`.

If Gate 0 fails:
- Return `SpecResult(status="GATE0_FAIL", ...)`
- Do NOT dispatch

### Status Handling: `run_queue.py`
When result is `GATE0_FAIL`:
- Move spec to `_needs_review/`
- Log message showing which checks failed

### Tests: `tests/queue/test_gate0.py`
Minimum 12 tests:
- Test each check independently (5 tests)
- Test valid spec passes all checks (1 test)
- Test incoherent spec (contradictory deliverables/criteria) fails (1 test)
- Test spec with missing file paths fails (1 test)
- Test spec with no acceptance criteria fails (1 test)
- Test spec with no priority fails (1 test)
- Test edge cases (2+ tests)

---

## Constraints

- **No file over 500 lines** (Rule 4)
- **TDD** — tests first (Rule 5)
- **No stubs** — every function fully implemented (Rule 6)
- **Gate 0 must be FAST** — no LLM calls, no network, no subprocess. Pure Python string parsing + file system checks.
- **Gate 0 must not break existing coherent specs** — only reject clearly incoherent ones

---

## Files to Read First

Priority order for Q33N:

1. `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` — full process reference (Gate 0 section)
2. `.deia/hive/scripts/queue/spec_processor.py` — where to integrate
3. `.deia/hive/scripts/queue/spec_parser.py` — SpecFile dataclass
4. `.deia/hive/scripts/queue/run_queue.py` — status handling

---

## Acceptance Criteria

From original spec (Q88N's requirements):

- [ ] New file: `.deia/hive/scripts/queue/gate0.py` exists with all required functions
- [ ] `validate_spec()` function takes `SpecFile` and `Path`, returns `Gate0Result`
- [ ] All 5 checks implemented as separate functions
- [ ] Integration in `spec_processor.py`: calls `validate_spec()` before dispatch
- [ ] New status `GATE0_FAIL` handled in `run_queue.py`: moves to `_needs_review/`
- [ ] Test file `tests/queue/test_gate0.py` exists with minimum 12 tests
- [ ] All tests pass
- [ ] Gate 0 rejects incoherent specs (contradictory deliverables/criteria)
- [ ] Gate 0 rejects specs with missing file paths
- [ ] Gate 0 rejects specs with no acceptance criteria
- [ ] Gate 0 rejects specs with no priority
- [ ] Gate 0 passes valid, coherent specs

---

## Response Requirements — MANDATORY

When bees finish, each bee writes:
  `.deia/hive/responses/YYYYMMDD-GATE0-QUEUE-RUNNER-VALIDATION-<BEE-MODEL>-RESPONSE.md`

**All 8 sections required:**
1. Header (task ID, title, status, model, date)
2. Files Modified (absolute paths)
3. What Was Done (bullet list)
4. Test Results (pass/fail counts)
5. Build Verification (test output summary)
6. Acceptance Criteria (copied from task, marked [x] or [ ])
7. Clock / Cost / Carbon (all three, never omit)
8. Issues / Follow-ups

---

## Task Breakdown Recommendation

Suggest to Q33N to create **2 tasks**:

### TASK-GATE0-A: Core Gate 0 Module (TDD)
**Assignee:** Sonnet
**Complexity:** Medium

Deliverables:
- `.deia/hive/scripts/queue/gate0.py` with all functions
- `tests/queue/test_gate0.py` with 12+ tests
- All tests passing

Test scenarios:
- Valid spec passes all checks
- Missing priority → fails
- Missing acceptance criteria → fails
- Missing file paths → fails
- Contradictory deliverables/criteria → fails
- Source bug identified but modification forbidden → fails

### TASK-GATE0-B: Integration & Status Handling
**Assignee:** Haiku
**Complexity:** Simple
**Depends On:** TASK-GATE0-A

Deliverables:
- Integration in `spec_processor.py`: call `validate_spec()` before dispatch
- Status handling in `run_queue.py`: handle `GATE0_FAIL`, move to `_needs_review/`
- Integration tests: end-to-end with real spec files

---

## Notes for Q33N

1. **This is Gate 0 ONLY** — not the full 3-phase pipeline from PROCESS-0013. Phases 0/1/2 are future work.

2. **Pure Python checks** — no LLM calls, no embeddings, no IR encoding. Just string parsing and file system checks.

3. **Error handling** — wrap all file operations in try/except. If a check can't run (I/O error), mark it as FAILED with clear message.

4. **Performance** — Gate 0 must run in < 1 second for typical specs. No subprocess calls, no network calls.

5. **Test data** — create fixture specs in `tests/queue/fixtures/` for test cases (valid spec, incoherent spec, missing files spec, etc.)

6. **Dispatch order** — Task A first (core module + tests), then Task B (integration). Task B depends on Task A passing.

---

## Budget

- **Model:** Sonnet for Task A (complex logic + TDD), Haiku for Task B (simple integration)
- **Estimated cost:** $0.15 total (Task A ~$0.10, Task B ~$0.05)
- **Estimated time:** 15-20 minutes total

---

**END OF BRIEFING**
