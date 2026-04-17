# Q33NR APPROVAL — Process 13 Quality Gates

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Re:** BRIEFING-process13-quality-gates

---

## Approval Status: ✅ APPROVED TO PROCEED

Your analysis is thorough and well-reasoned. All three clarifying questions have been answered. You are approved to write task files.

---

## Approved Decisions

### 1. Build Check Timing
**APPROVED: Option A (before dispatch)**

Run build verification AFTER spec format validation, BEFORE baseline capture, BEFORE dispatch.

Flow sequence:
```
spec file
  → validate_spec_format() [NEW]
  → run_build_check() [NEW]
  → _capture_baseline() [EXISTING]
  → dispatch.py (calls bee)
  → _run_verification() [EXISTING]
```

### 2. Build Commands
**APPROVED: Python + TypeScript with graceful degradation**

```bash
# Python (mandatory, fail if errors)
python -m py_compile hivenode/__init__.py
python -m py_compile engine/__init__.py

# TypeScript (optional, graceful skip if npm/script missing)
cd browser && npm run type-check
```

Failure handling:
- Python compile error → status=NEEDS_DAVE, error_msg includes syntax details
- npm missing or no type-check script → log warning, continue
- type-check fails → status=NEEDS_DAVE, error_msg includes type errors

### 3. Validation Strictness
**APPROVED: Lenient validation**

**FAIL conditions:**
- Priority not in [P0, P0.5, P0.85, P1, P2, P3]
- Model not in [haiku, sonnet, opus]
- Objective is empty or missing
- Acceptance Criteria section empty (no checkboxes)
- Smoke Test section empty (no commands)

**WARN conditions:**
- Constraints section missing (log to console, don't block)

**SKIP conditions:**
- Hold section present (queue runner already handles this)

---

## Task File Requirements

Write both task files now:

### TASK-165: Add Spec Format Validation Gate
- **Model:** haiku
- **Deliverables:**
  - New module: `.deia/hive/scripts/queue/spec_validator.py` (~150 lines)
  - Update: `.deia/hive/scripts/queue/spec_processor.py` (~5 lines to call validator)
  - New tests: `.deia/hive/scripts/queue/tests/test_spec_validator.py` (~200 lines)
- **Test requirements:** 8 tests minimum
  1. Valid spec (all sections present) → passes
  2. Missing objective → fails with clear error
  3. Invalid priority (P4) → fails
  4. Invalid model (gpt4) → fails
  5. Empty acceptance criteria → fails
  6. Empty smoke test → fails
  7. Missing constraints → warns, passes
  8. Integration: spec_processor calls validator before dispatch
- **Constraints:** No file over 500 lines, TDD, no stubs
- **Response requirements:** All 8 sections

### TASK-166: Add Build Verification Gate
- **Model:** haiku
- **Deliverables:**
  - New module: `.deia/hive/scripts/queue/build_checker.py` (~200 lines)
  - Update: `.deia/hive/scripts/queue/spec_processor.py` (~10 lines to call build check)
  - New tests: `.deia/hive/scripts/queue/tests/test_build_checker.py` (~250 lines)
- **Test requirements:** 8 tests minimum
  1. Python compile valid → passes
  2. Python syntax error → fails with error details
  3. TypeScript type-check valid → passes
  4. TypeScript type errors → fails with error details
  5. npm not installed → warns, continues (graceful degradation)
  6. type-check script missing → warns, continues
  7. Integration: spec_processor calls build check before baseline
  8. Integration: build failure skips dispatch, flags NEEDS_DAVE
- **Constraints:** No file over 500 lines, TDD, no stubs
- **Response requirements:** All 8 sections

---

## Mechanical Review Checklist (for when you return task files)

I will verify:
- [ ] Deliverables match spec acceptance criteria
- [ ] File paths are absolute
- [ ] Test requirements specify count and scenarios
- [ ] No file will exceed 500 lines (estimates provided)
- [ ] No stubs mentioned in deliverables
- [ ] Response file template included in each task
- [ ] CSS uses var(--sd-*) only (N/A for Python)
- [ ] Tasks can run in parallel (independent directories)

---

## Dispatch Plan (after task review approval)

Both tasks are independent (different modules, different test files). They can run in parallel:

```bash
# Parallel dispatch (2 bees)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-165-spec-format-validation.md --model haiku --role bee --inject-boot

python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-166-build-verification-gate.md --model haiku --role bee --inject-boot
```

Max parallel bees: 2 (within budget limit of 5).

---

## Action Items

**Q33N next steps:**
1. Write TASK-165 to `.deia/hive/tasks/2026-03-15-TASK-165-spec-format-validation.md`
2. Write TASK-166 to `.deia/hive/tasks/2026-03-15-TASK-166-build-verification-gate.md`
3. Return both task files to Q33NR for mechanical review
4. Wait for Q33NR approval before dispatching bees

**Q33NR next steps:**
1. Review both task files against checklist
2. Approve OR request corrections (max 2 cycles)
3. Approve dispatch
4. Wait for bee responses
5. Review results, report to Q88N

---

**Status:** APPROVED — Q33N, proceed to write task files.

**Clock:** 20 minutes total (Q33N analysis + Q33NR decisions + approval)
**Cost:** $0.00
**Carbon:** ~0g
