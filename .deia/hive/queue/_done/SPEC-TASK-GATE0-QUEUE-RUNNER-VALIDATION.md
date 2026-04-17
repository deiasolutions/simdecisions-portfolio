# SPEC: Gate 0 Programmatic Validation for Queue Runner

## Priority
P0

## Objective

Add programmatic Gate 0 validation to the queue runner that checks spec quality BEFORE dispatching to regent bot. This prevents incoherent specs from reaching bees. This implements the **minimum viable Gate 0** from PROCESS-0013 — coverage and coherence checks only (no IR fidelity).

## Context

From briefing 2026-03-19-BRIEFING-GATE0-QUEUE-RUNNER-VALIDATION:
- Queue runner currently dispatches specs directly with zero validation
- Incoherent specs (contradictory deliverables vs acceptance criteria) reach bees
- Q33NR review exists only as prompt instruction (gets rubber-stamped)
- Need code-level gate to catch issues before dispatch

Gate 0 runs in `process_spec()` BEFORE `handler.call_dispatch()`.

From PROCESS-0013:
- Gate 0 is the first validation layer (disambiguation)
- Phase 0 (requirement coverage) is FUTURE work
- Phase 1/2 (IR fidelity) are FUTURE work
- This task implements ONLY Gate 0 checks

## Integration Point

- **Queue runner:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`
- **Spec processor:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py`
- **Spec parser:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py`

Gate 0 runs in `process_spec()` AFTER spec load, BEFORE `handler.call_dispatch()`.

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` (Gate 0 section, lines 38-208)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` (process_spec function, lines 85-321)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` (SpecFile dataclass, lines 14-27)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` (status handling, lines 530-791)

## Model Assignment

Sonnet

## What Gate 0 Must Check

Run AFTER spec load, BEFORE dispatch. Pure Python validation (no LLM calls, no network, no subprocess).

### Required Checks (all must pass)

1. **Priority Present**
   - Spec must have P0/P1/P2/P3 priority
   - Missing priority = FAIL

2. **Acceptance Criteria Present**
   - Spec must have at least one acceptance criterion
   - Empty acceptance criteria = FAIL

3. **File Paths Exist**
   - Every file path in "Files to Read First" or "Files to Modify" must exist on disk
   - Missing files = FAIL

4. **Deliverables vs Acceptance Criteria Coherence**
   - If spec says "fix X" in acceptance criteria, deliverables must not say "DO NOT modify X"
   - Flag contradictions = FAIL

5. **Scope Sanity**
   - If spec references a source file bug, it must allow modification of that file
   - A spec that identifies a bug location but forbids editing = FAIL

### What Gate 0 Does NOT Do

- IR fidelity round-trip (Phase 1/2 — future)
- LLM-based requirement extraction (Phase 0 — future)
- Embedding similarity (future)
- Traceability graph (future)

## Deliverables

### 1. New File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\gate0.py`

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

### 2. Integration: `spec_processor.py`

Call `validate_spec()` BEFORE `handler.call_dispatch()` in `process_spec()` function (around line 125).

If Gate 0 fails:
- Return `SpecResult(status="GATE0_FAIL", ...)`
- Do NOT dispatch

### 3. Status Handling: `run_queue.py`

When result is `GATE0_FAIL`:
- Move spec to `_needs_review/`
- Log message showing which checks failed

### 4. Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\test_gate0.py`

Minimum 12 tests:
- Test each check independently (5 tests)
- Test valid spec passes all checks (1 test)
- Test incoherent spec (contradictory deliverables/criteria) fails (1 test)
- Test spec with missing file paths fails (1 test)
- Test spec with no acceptance criteria fails (1 test)
- Test spec with no priority fails (1 test)
- Test edge cases (2+ tests)

## Constraints

- **No file over 500 lines** (Rule 4)
- **TDD** — tests first (Rule 5)
- **No stubs** — every function fully implemented (Rule 6)
- **Gate 0 must be FAST** — no LLM calls, no network, no subprocess. Pure Python string parsing + file system checks.
- **Gate 0 must not break existing coherent specs** — only reject clearly incoherent ones
- **Error handling** — wrap all file operations in try/except. If a check can't run (I/O error), mark it as FAILED with clear message.

## Acceptance Criteria

- [ ] New file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\gate0.py` exists with all required functions
- [ ] `validate_spec()` function takes `SpecFile` and `Path`, returns `Gate0Result`
- [ ] All 5 checks implemented as separate functions
- [ ] Integration in `spec_processor.py`: calls `validate_spec()` before dispatch
- [ ] New status `GATE0_FAIL` handled in `run_queue.py`: moves to `_needs_review/`
- [ ] Test file `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\test_gate0.py` exists with minimum 12 tests
- [ ] All tests pass
- [ ] Gate 0 rejects incoherent specs (contradictory deliverables/criteria)
- [ ] Gate 0 rejects specs with missing file paths
- [ ] Gate 0 rejects specs with no acceptance criteria
- [ ] Gate 0 rejects specs with no priority
- [ ] Gate 0 passes valid, coherent specs
- [ ] Gate 0 runs in < 1 second for typical specs (no subprocess, no network)

## Smoke Test

After implementation:
- [ ] Run queue tests: `python -m pytest tests\queue\test_gate0.py -v`
- [ ] All tests pass
- [ ] Create fixture spec with missing priority → Gate 0 rejects it
- [ ] Create fixture spec with contradictory deliverables/criteria → Gate 0 rejects it
- [ ] Create valid spec → Gate 0 passes it

## Test Data Requirements

Create fixture specs in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\queue\fixtures\` for test cases:
- `valid-spec.md` — passes all checks
- `missing-priority-spec.md` — no priority section
- `missing-criteria-spec.md` — no acceptance criteria
- `missing-files-spec.md` — references non-existent files
- `incoherent-spec.md` — contradictory deliverables vs acceptance criteria
- `scope-violation-spec.md` — identifies bug location but forbids editing

## Response Requirements — MANDATORY

When done, write: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-GATE0-QUEUE-RUNNER-VALIDATION-SONNET-RESPONSE.md`

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

**END OF SPEC**
