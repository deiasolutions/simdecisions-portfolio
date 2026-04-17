# BRIEFING: Gate 0 Validation Implementation for Queue Runner

**Date:** 2026-03-19
**From:** Q33NR
**To:** Q33N
**Re:** SPEC-TASK-GATE0-QUEUE-RUNNER-VALIDATION

---

## Objective

Q33N, you are to write task files for implementing Gate 0 programmatic validation in the queue runner. This is a **Sonnet-level task** requiring careful integration with existing queue infrastructure.

## Context

The queue runner currently dispatches specs directly to regent bot with zero validation. This allows incoherent specs (contradictory deliverables vs acceptance criteria) to reach bees and waste cycles.

Gate 0 from PROCESS-0013 is the first validation layer (disambiguation). It runs BEFORE dispatch and catches:
- Missing priority
- Missing acceptance criteria
- Non-existent file paths
- Contradictory deliverables vs acceptance criteria
- Scope violations (spec identifies bug location but forbids editing)

This is **pure Python validation** — no LLM calls, no network, no subprocess. Must be FAST (< 1 second).

## Integration Point

Gate 0 runs in `spec_processor.py::process_spec()` function at line 125, AFTER spec load, BEFORE `handler.call_dispatch()`.

If Gate 0 fails:
- Return `SpecResult(status="GATE0_FAIL", ...)`
- Do NOT dispatch
- `run_queue.py` moves spec to `_needs_review/`

## Files to Read First

Q33N, read these files to understand the integration:

1. `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` (lines 38-208) — Gate 0 requirements
2. `.deia/hive/scripts/queue/spec_processor.py` (lines 85-321) — where Gate 0 integrates
3. `.deia/hive/scripts/queue/spec_parser.py` (lines 14-27) — SpecFile dataclass
4. `.deia/hive/scripts/queue/run_queue.py` (lines 530-791) — status handling

## What Gate 0 Must Check

From PROCESS-0013 lines 98-110:

1. **Priority Present** — spec must have P0/P1/P2/P3
2. **Acceptance Criteria Present** — spec must have at least one
3. **File Paths Exist** — every file in "Files to Read First" or "Files to Modify" must exist on disk
4. **Deliverables vs Acceptance Criteria Coherence** — if spec says "fix X" in acceptance criteria, deliverables must not say "DO NOT modify X"
5. **Scope Sanity** — if spec references a source file bug, it must allow modification of that file

## Deliverables Expected from You (Q33N)

Write ONE task file for the bee:

**File:** `.deia/hive/tasks/2026-03-19-TASK-GATE0-VALIDATION.md`

The task must include:

### 1. New Module: `.deia/hive/scripts/queue/gate0.py`

Required functions:
```python
def validate_spec(spec: SpecFile, repo_root: Path) -> Gate0Result
def check_priority(spec: SpecFile) -> CheckResult
def check_acceptance_criteria(spec: SpecFile) -> CheckResult
def check_file_paths_exist(spec: SpecFile, repo_root: Path) -> CheckResult
def check_deliverables_coherence(spec: SpecFile) -> CheckResult
def check_scope_sanity(spec: SpecFile) -> CheckResult
```

Dataclasses:
```python
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

### 2. Integration: `spec_processor.py`

At line 125 (before `handler.call_dispatch()`):
```python
# Run Gate 0 validation
gate0_result = validate_spec(spec, repo_root)
if not gate0_result.passed:
    return SpecResult(
        spec_id=spec_id,
        status="GATE0_FAIL",
        cost_usd=0.0,
        duration_ms=0,
        error_msg=gate0_result.summary
    )
```

### 3. Status Handling: `run_queue.py`

When `result.status == "GATE0_FAIL"`:
- Move spec to `_needs_review/`
- Log message showing which checks failed

### 4. Tests: `tests/queue/test_gate0.py`

Minimum 12 tests:
- Test each check independently (5 tests)
- Test valid spec passes all checks (1 test)
- Test incoherent spec fails (1 test)
- Test missing file paths fails (1 test)
- Test missing acceptance criteria fails (1 test)
- Test missing priority fails (1 test)
- Test edge cases (2+ tests)

### 5. Fixture Specs: `tests/queue/fixtures/`

Create test fixtures:
- `valid-spec.md` — passes all checks
- `missing-priority-spec.md` — no priority section
- `missing-criteria-spec.md` — no acceptance criteria
- `missing-files-spec.md` — references non-existent files
- `incoherent-spec.md` — contradictory deliverables vs acceptance criteria
- `scope-violation-spec.md` — identifies bug location but forbids editing

## Constraints

From BOOT.md Rule 4: No file over 500 lines. If `gate0.py` approaches 500 lines, modularize checks into separate files.

From BOOT.md Rule 5: TDD — tests written FIRST.

From BOOT.md Rule 6: NO STUBS — every function fully implemented.

From BOOT.md Rule 10: NO GIT OPERATIONS without Q88N approval.

## Test Requirements

The bee MUST:
1. Write tests FIRST (TDD)
2. Run tests: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/queue/test_gate0.py -v`
3. All tests must pass
4. No stubs, no TODOs, no empty functions

## Response File Requirements

The bee MUST write: `.deia/hive/responses/20260319-GATE0-QUEUE-RUNNER-VALIDATION-SONNET-RESPONSE.md`

All 8 sections required (per BOOT.md):
1. Header (task ID, title, status, model, date)
2. Files Modified (absolute paths)
3. What Was Done (bullet list)
4. Test Results (pass/fail counts)
5. Build Verification (test output summary)
6. Acceptance Criteria (copied from task, marked [x] or [ ])
7. Clock / Cost / Carbon (all three, never omit)
8. Issues / Follow-ups

## Acceptance Criteria for Task File

Q33N, your task file must specify:

- [ ] New file: `.deia/hive/scripts/queue/gate0.py` with all required functions
- [ ] Integration in `spec_processor.py` at line 125
- [ ] New status `GATE0_FAIL` handled in `run_queue.py`
- [ ] Test file `tests/queue/test_gate0.py` with minimum 12 tests
- [ ] All tests pass
- [ ] Gate 0 rejects incoherent specs
- [ ] Gate 0 rejects specs with missing file paths
- [ ] Gate 0 rejects specs with no acceptance criteria
- [ ] Gate 0 rejects specs with no priority
- [ ] Gate 0 passes valid, coherent specs
- [ ] Gate 0 runs in < 1 second (no subprocess, no network)
- [ ] Fixture specs in `tests/queue/fixtures/` for test cases

## Next Steps

Q33N:
1. Read the 4 files listed above
2. Write the task file: `.deia/hive/tasks/2026-03-19-TASK-GATE0-VALIDATION.md`
3. Return to me (Q33NR) for review
4. Do NOT dispatch the bee yet — I must approve the task file first

---

**Q33NR**
