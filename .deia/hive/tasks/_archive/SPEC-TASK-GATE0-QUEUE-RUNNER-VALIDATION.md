# SPEC: Add Gate 0 Programmatic Validation to Queue Runner

## Priority
P0 — process integrity fix

## Model
sonnet

## Objective

Add a **programmatic Gate 0 validation step** to the queue runner that checks spec quality BEFORE dispatching to the regent bot. This prevents incoherent specs (e.g., "fix this source code bug but DON'T TOUCH SOURCE CODE") from reaching bees.

Currently the queue runner dispatches specs directly to regent bots with zero validation. The Q33NR review step exists only as a behavioral prompt instruction to the regent bot, which means it gets skipped or rubber-stamped. This spec adds a real code-level gate.

## Context

- **PROCESS-0013** (`.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md`) defines a full Gate 0 + 3-phase IR fidelity pipeline. This spec implements the **minimum viable Gate 0** only — the coverage/coherence check.
- The queue runner lives at `.deia/hive/scripts/queue/run_queue.py`
- Spec processing happens in `.deia/hive/scripts/queue/spec_processor.py`
- Dispatch happens in `.deia/hive/scripts/queue/dispatch_handler.py`
- The regent bot prompt is at `.deia/config/regent-bot-prompt.md`

## What Gate 0 Must Check

The gate runs AFTER a spec is loaded but BEFORE `process_spec()` calls `handler.call_dispatch()`. It is a **code function**, not a prompt instruction.

### Required Checks (all must pass):

1. **Deliverables vs Acceptance Criteria coherence**: If the spec says "fix X" in acceptance criteria, the deliverables must not say "DO NOT modify X". Flag contradictions.
2. **File paths exist**: Every file path referenced in "Files to Read First" or "Files to Modify" must exist on disk. Flag missing files.
3. **Scope sanity**: If the spec references a source file bug, it must allow modification of that source file. A spec that identifies a bug location but forbids editing that location is incoherent.
4. **Priority is present**: Spec must have a P0/P1/P2/P3 priority. Missing priority = reject.
5. **Acceptance criteria present**: Spec must have at least one acceptance criterion. No criteria = reject.

### What Gate 0 Does NOT Do (yet):

- IR fidelity round-trip (Phase 1/2 — future work)
- LLM-based requirement extraction (future work)
- Embedding similarity checks (future work)
- Traceability graph generation (future work)

## Deliverables

- [ ] New file: `.deia/hive/scripts/queue/gate0.py` — the Gate 0 validation module
  - `validate_spec(spec: SpecFile, repo_root: Path) -> Gate0Result`
  - `Gate0Result` dataclass with: `passed: bool`, `checks: list[CheckResult]`, `summary: str`
  - `CheckResult` dataclass with: `name: str`, `passed: bool`, `message: str`
  - Each check is a separate function (testable independently)
- [ ] Integration in `spec_processor.py`: Call `validate_spec()` before `handler.call_dispatch()`. If Gate 0 fails, return `SpecResult(status="GATE0_FAIL", ...)` — do NOT dispatch.
- [ ] New status handling in `run_queue.py`: When result is `GATE0_FAIL`, move spec to `_needs_review/` with a log message showing which checks failed.
- [ ] Tests: `tests/queue/test_gate0.py`
  - Test each check independently
  - Test a valid spec passes all checks
  - Test an incoherent spec (contradictory deliverables/criteria) fails
  - Test a spec with missing file paths fails
  - Test a spec with no acceptance criteria fails
  - Test a spec with no priority fails
  - Minimum 12 tests

## Files to Read First

- `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` (the full process reference)
- `.deia/hive/scripts/queue/spec_processor.py` (where to integrate)
- `.deia/hive/scripts/queue/spec_parser.py` (SpecFile dataclass)
- `.deia/hive/scripts/queue/run_queue.py` (status handling)

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (N/A for this task)
- No stubs — every function fully implemented
- TDD: tests first
- Gate 0 must be FAST — no LLM calls, no network calls, no subprocess calls. Pure Python string parsing and file system checks.
- Gate 0 must not break existing specs that ARE coherent. Only reject clearly incoherent ones.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-GATE0-QUEUE-RUNNER-VALIDATION-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
