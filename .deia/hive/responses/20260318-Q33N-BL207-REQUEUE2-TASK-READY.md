# Q33N Response: BL-207 Re-Queue 2 Task File Ready

**To:** Q33NR (Queen Regent)
**From:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Status:** TASK FILE READY FOR REVIEW

---

## Task File Created

I have written ONE task file for BL-207 (EGG chrome opt-out):

**File:** `.deia/hive/tasks/2026-03-18-TASK-BL207-EGG-CHROME-OPT-OUT.md`

---

## What the Task File Contains

### 1. **Crystal-Clear Instructions**

The task file is EXPLICIT about what must be changed:
- "Change line 33 from `chrome: true,` to `chrome: eggNode.chrome !== false,`"
- "Change line 115 from `chrome: true,` to `chrome: node.chrome !== false,`"
- Shows BEFORE and AFTER code blocks

### 2. **Multiple Warnings**

I added FIVE explicit warnings that the bee MUST modify source code:
- "CRITICAL: You MUST Modify Source Code" section at the top
- "If you only write tests, you have FAILED."
- "If you only write a briefing, you have FAILED."
- "If you do not change lines 33 and 115, you have FAILED."
- "WARNING: What NOT To Do" section at the bottom

### 3. **Complete Deliverables**

- [ ] Line 33 changed
- [ ] Line 115 changed
- [ ] No other lines changed
- [ ] Tests written
- [ ] All existing tests pass
- [ ] New tests verify chrome field behavior
- [ ] Response file with all 8 sections

### 4. **Complete Test Requirements**

- [ ] Tests written FIRST (TDD)
- [ ] Test: chrome: false → chrome: false
- [ ] Test: chrome: true → chrome: true
- [ ] Test: chrome: undefined → chrome: true (default)
- [ ] All existing eggToShell tests pass
- [ ] New tests added to eggToShell.test.ts

### 5. **Complete Acceptance Criteria**

- [ ] `chrome: true` is NO LONGER hardcoded on line 33
- [ ] `chrome: true` is NO LONGER hardcoded on line 115
- [ ] EGG pane with `"chrome": false` produces shell node with `chrome: false`
- [ ] EGG pane without chrome field produces shell node with `chrome: true`
- [ ] EGG pane with `"chrome": true` produces shell node with `chrome: true`
- [ ] All eggToShell tests pass
- [ ] build-monitor.egg.md test case verified

### 6. **Smoke Test Commands**

```bash
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
cd browser && npx vitest run --reporter=verbose src/shell/
cd browser && npx vitest run
```

### 7. **Success Checklist**

Before writing the response file, the bee must verify:
- [ ] I changed line 33 in eggToShell.ts
- [ ] I changed line 115 in eggToShell.ts
- [ ] I wrote tests to verify the change
- [ ] All existing tests pass
- [ ] All new tests pass
- [ ] No stubs or TODOs in my code
- [ ] I wrote a response file with all 8 sections

---

## Why This Should Work

### Previous Failures

**Re-queue 1:** Bee wrote a "runtime verify briefing" instead of changing code.
**Root cause:** Task file was not explicit enough about requiring SOURCE CODE changes.

### This Time

**The task file is IMPOSSIBLE to misunderstand:**
- Uses ALL CAPS for critical warnings
- Shows exact BEFORE and AFTER code
- Explicitly states the exact lines to change (33 and 115)
- Explicitly warns FIVE TIMES that only writing tests = FAILURE
- Has a success checklist that forces the bee to verify it changed the source code

If the bee reads the task file, it CANNOT miss the requirement to change source code.

---

## Files Referenced

The task file tells the bee to read these files FIRST:

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` — THE FILE TO CHANGE
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — AppNode type
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` — EggLayoutNode type
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` — test case
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.test.ts` — existing tests

---

## Expected Deliverables

When the bee completes this task:

1. **Source code changed:**
   - Line 33: `chrome: eggNode.chrome !== false,`
   - Line 115: `chrome: node.chrome !== false,`

2. **Tests added to eggToShell.test.ts:**
   - Test: chrome: false → false
   - Test: chrome: true → true
   - Test: chrome: undefined → true

3. **All tests pass:**
   - Existing eggToShell tests: PASS
   - New chrome tests: PASS

4. **Response file written:**
   - `.deia/hive/responses/20260318-TASK-BL207-RESPONSE.md`
   - All 8 sections present

---

## Awaiting Q33NR Review

The task file is ready for your review.

**Next steps:**
1. You review the task file
2. If approved, you tell me to dispatch the bee
3. I dispatch: `python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BL207-EGG-CHROME-OPT-OUT.md --model sonnet --role bee --inject-boot`
4. Bee completes the work
5. I review the response file and report to you

---

**Q33N — Awaiting approval to dispatch**
