# TASK-SEC-7: Fix Frontend Tests - Vitest esbuild EPERM

## Objective
Fix Vitest esbuild spawn EPERM errors on Windows and record frontend test baseline.

## Context
On Windows, Vitest sometimes fails to spawn esbuild with EPERM (permission error). This is often due to corrupted node_modules or Windows file locking. The fix is to clean reinstall node_modules and explicitly run esbuild install script.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vitest.config.ts`

## Deliverables
- [ ] Run `cd browser && npx vitest run --reporter=verbose` and record current status
- [ ] If esbuild spawn fails:
  1. `cd browser && rm -rf node_modules && rm package-lock.json`
  2. `npm install`
  3. `node node_modules/esbuild/install.js`
- [ ] Run tests again: `npx vitest run --reporter=verbose`
- [ ] Record pass/fail/skip counts in response file
- [ ] If tests still fail, document the errors for Q88N review

## Test Requirements
- Run full frontend test suite
- Record baseline: pass/fail/skip counts
- Document any failures that are NOT related to esbuild spawn errors

## Constraints
- Do NOT modify test files or source code
- Only perform node_modules cleanup if esbuild spawn fails
- If failures persist after cleanup, document but do not attempt fixes

## Model
Haiku (simple cleanup task)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-SEC-7-RESPONSE.md`

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
