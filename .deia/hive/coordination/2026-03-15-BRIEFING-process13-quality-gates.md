# BRIEFING: Wire Process 13 Quality Gates into Dispatch Pipeline

**Date:** 2026-03-15
**From:** Q33NR
**To:** Q33N
**Model:** sonnet
**Priority:** P0.85

---

## Objective

Wire quality gates (spec validation → build → test → review) into the dispatch pipeline. The spec references "Process 13" but P-13 in PROCESS-LIBRARY-V2.md is about backlog addition. The quality gates described match P-04: Build Integrity — 3-Phase Validation.

Implement the following gates in spec_processor.py:
1. **Spec format validation** before dispatch
2. **Pre/post test comparison** (already partially implemented via `_capture_baseline` and `_run_verification`)
3. **Regression detection** that flags NEEDS_DAVE (already implemented)
4. **Build verification** (needs implementation)

---

## Context

### Current Implementation

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py`

**Already implemented:**
- Baseline test capture (`_capture_baseline`) before dispatch
- Post-bee verification (`_run_verification`) with regression detection
- Regression flagging sets `status="NEEDS_DAVE"` and `is_regression=True`
- Test suite runner in `test_runner.py` (imports: `run_full_test_suite`, `get_new_failures`)

**Missing:**
- Spec format validation gate (before dispatch)
- Build verification gate (before tests)
- Explicit review gate (currently implicit in Q33NR workflow)

### P-04: Build Integrity — 3-Phase Validation

From `.deia\processes\PROCESS-LIBRARY-V2.md`:

**Act 1 — Validate the Plan.** Before coding, verify: task file is complete, deliverables are concrete, file paths exist, no ambiguity.

**Act 2 — Execute with Self-Check.** TDD cycle: write test (red) → write code (green) → refactor.

**Act 3 — Validate Output.** All tests pass. Build passes. Response file has all 8 sections. Acceptance criteria checked. No stubs. No hardcoded colors. No files over 500 lines.

---

## Requirements

### 1. Spec Format Validation Gate

Add `validate_spec_format()` function that checks BEFORE dispatch:
- [ ] Required sections present: Priority, Objective, Acceptance Criteria, Constraints, Smoke Test
- [ ] Priority is valid (P0, P0.5, P0.85, P1, P2, P3)
- [ ] Model assignment is valid (haiku, sonnet, opus)
- [ ] At least one acceptance criterion
- [ ] At least one smoke test command
- [ ] Return tuple: `(is_valid: bool, error_msg: str)`

### 2. Build Verification Gate (Pre-Test)

The spec says "build then test" but the current implementation only runs tests. For Python/TypeScript projects, "build" typically means:
- Python: import validation, syntax check
- TypeScript: compilation check

Add `run_build_check()` that:
- [ ] Runs Python import checks on hivenode and engine
- [ ] Runs TypeScript type check on browser (`npm run type-check` or similar)
- [ ] Returns build status before test suite runs
- [ ] If build fails, skip tests and flag NEEDS_DAVE

### 3. Enhanced Test Comparison

Already implemented. No changes needed.

### 4. Review Gate

Already implicit (Q33NR reviews results). No code change needed. Document in response file.

---

## Files to Modify

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py`
   - Add `validate_spec_format()` function
   - Add `run_build_check()` function
   - Call validation gate in `process_spec()` before dispatch
   - Call build gate after baseline, before dispatch or after dispatch but before verification
   - Update error handling for new gates

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\test_runner.py` (if build logic needs to go there)
   - Or create new `build_checker.py` module if build logic is substantial

---

## Test Requirements

Write tests in `.deia\hive\scripts\queue\tests\`:
- [ ] Test spec validation with valid spec (passes)
- [ ] Test spec validation with missing sections (fails)
- [ ] Test spec validation with invalid priority (fails)
- [ ] Test spec validation with invalid model (fails)
- [ ] Test build check with valid repo (passes)
- [ ] Test build check with syntax error (fails)
- [ ] Integration test: spec_processor calls validation gate before dispatch
- [ ] Integration test: spec_processor calls build gate before tests

Minimum 8 tests covering all gates.

---

## Constraints

- No file over 500 lines (modularize if needed)
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only (not applicable for Python)
- Follow existing code patterns in spec_processor.py
- Use existing test infrastructure (pytest)

---

## Success Criteria

- [ ] Spec validation gate prevents invalid specs from dispatching
- [ ] Build verification gate runs before tests
- [ ] Regression detection continues working (already implemented)
- [ ] All new tests pass
- [ ] No regressions in existing queue tests
- [ ] Response file documents all 3 gates

---

## Open Questions for Q33N

1. **Build verification placement:** Should build check run BEFORE dispatch (validate spec can even be attempted) or AFTER dispatch (validate bee's output)? Spec says "spec validation then build then test" which suggests build happens AFTER spec validation but unclear if before or after bee dispatch.

2. **Build commands:** What commands should run for build verification? Need to verify:
   - Python: `python -m py_compile` on key modules?
   - TypeScript: `npm run type-check` or `npx tsc --noEmit`?
   - Or just rely on test suite imports to catch build errors?

3. **Graceful degradation:** If build check fails (e.g., npm not installed), should we skip and continue, or should we fail the spec?

---

## Recommendation

Start with **spec format validation** (high confidence, low risk). For build verification, recommend a lightweight approach:
- Python: Try importing key modules (hivenode, engine) in subprocess
- TypeScript: Optional type check if `package.json` has type-check script
- Graceful degradation if build tools not available

---

**Q33N: Please clarify the open questions, then write task files for implementation.**
