# TASK-024: Quick Cleanups (Import Fix, Debug Logs, Dispatch Path)

## Objective
Three small fixes: fix morning_report test imports, remove debug console.logs from terminal, and expand dispatch.py path validation to accept coordination files.

## Context
These are leftover issues from last night's BUG-002 fix and build queue Phase 1 work. All three are mechanical cleanups.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_morning_report.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\morning_report.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py`

## Deliverables

### Fix 1: morning_report test import path
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\conftest.py` that adds the parent directory (the queue package dir) to `sys.path` so `from morning_report import ...` resolves from any working directory.
- [ ] Remove the duplicate `QueueEvent` dataclass definition from `test_morning_report.py` (lines 11-20). Import it from `morning_report` instead: `from morning_report import QueueEvent, generate_morning_report`. Move the import to the top of the file (module level), not inside each test method.
- [ ] All 9 morning_report tests pass when run from repo root: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest .deia/hive/scripts/queue/tests/test_morning_report.py -v`

### Fix 2: Remove debug console.logs from terminal
- [ ] In `useTerminal.ts`, delete the debug `console.log` block at lines 250-256 (the `[useTerminal] isChatMode check:` log). Do NOT remove the `console.warn` calls for envelope parse issues or the `console.log` for conversation creation — those are operational, not debug.
- [ ] In `TerminalOutput.tsx`, delete the debug `console.log` at lines 43-46 inside `entries.map()` (the `[TerminalOutput] rendering entry:` log that fires on EVERY render of EVERY entry).
- [ ] In `TerminalOutput.tsx`, delete the debug `console.log` at line 96 (the `[TerminalOutput] response entry, metricsOnly:` log).
- [ ] Run browser tests to verify no regressions: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run`

### Fix 3: dispatch.py path validation
- [ ] Modify `validate_task_file()` in `dispatch.py` to accept files in BOTH `.deia/hive/tasks/` AND `.deia/hive/coordination/`. The coordination path is needed when dispatching Q33N (queen) with a briefing file.
- [ ] The function signature should accept an optional `role` parameter. When `role == "queen"`, also accept `.deia/hive/coordination/`. When `role == "bee"`, only accept `.deia/hive/tasks/` (current behavior).
- [ ] Update the `dispatch_bee()` function to pass the `role` argument through to `validate_task_file()`.
- [ ] Write tests for the path validation in a new file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\tests\test_dispatch_validation.py`. Test cases:
  - bee role: accepts `.deia/hive/tasks/TASK-001.md`, rejects `.deia/hive/coordination/BRIEFING.md`
  - queen role: accepts both `.deia/hive/tasks/TASK-001.md` and `.deia/hive/coordination/BRIEFING.md`
  - rejects files outside both directories regardless of role
  - rejects non-.md files (except .ir.json)
  - rejects files that don't exist
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\tests\__init__.py`
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\tests\conftest.py` that adds the dispatch script directory to sys.path.

## Test Requirements
- [ ] All 9 morning_report tests pass from repo root
- [ ] All 94 queue tests pass (run from repo root)
- [ ] Browser tests: no new regressions (run `npx vitest run` from browser/)
- [ ] New dispatch validation tests pass

## Constraints
- No file over 500 lines
- No stubs
- Do not modify any logic in useTerminal.ts or TerminalOutput.tsx beyond removing the debug console.log lines
- Do not modify morning_report.py itself — only fix the test imports
- Keep dispatch.py's existing behavior for bee role unchanged

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-024-RESPONSE.md`

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
