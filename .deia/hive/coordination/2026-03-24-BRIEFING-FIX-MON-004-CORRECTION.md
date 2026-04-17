# BRIEFING: MON-004 Task File Correction

**From:** Q33NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-24
**Priority:** P0

---

## Situation

The queue runner created a fix spec for MON-004, but this fix spec is malformed. The original MON-004 did NOT fail during bee execution — it failed during regent mechanical review because the task file violated Rule 8 (relative paths instead of absolute paths).

**Original failure:** Task file review rejection (not dispatched to bee)
**Fix spec created:** SPEC-fix-MON-004-code-egg
**Problem:** Fix spec has no concrete errors to fix (says "Dispatch reported failure" with no details)

---

## What Actually Happened

1. Queue runner processed `2026-03-24-SPEC-MON-004-code-egg.md`
2. Regent reviewed task file in `_stage/2026-03-24-TASK-MON-004-code-egg.md`
3. Regent found violations:
   - **ISSUE #1:** File paths are relative, not absolute (Rule 8 violation)
   - **ISSUE #2:** Task says "Add code subdomain" but it already exists in eggResolver.ts
4. Regent rejected the task file (cycle 1 of 2)
5. Queue runner interpreted this as a dispatch failure and created fix spec

---

## What Needs to Happen

**Option A: Correct the task file and re-run the original spec (RECOMMENDED)**

1. Fix `.deia/hive/queue/_stage/2026-03-24-TASK-MON-004-code-egg.md`:
   - Replace ALL relative paths with absolute Windows paths
   - Change "Add `code` subdomain" to "Verify `code` subdomain exists"
2. Resubmit to regent for cycle 2 review
3. If approved, dispatch BEE-HAIKU with corrected task file
4. Mark fix spec as INVALID (close without execution)

**Option B: Create new corrected task from scratch**

1. Read the original spec requirements
2. Write new task file with absolute paths
3. Submit for regent review
4. Dispatch when approved
5. Mark fix spec as INVALID

---

## Mechanical Review Issues (from regent response)

### Issue #1: Relative Paths (MUST FIX)

**Current (WRONG):**
```
src/eggs/code.egg.md
browser/src/eggs/__tests__/codeEgg.test.ts
```

**Required (CORRECT):**
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\code.egg.md
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\codeEgg.test.ts
```

### Issue #2: Subdomain Registration (CLARIFY)

**Current wording:**
> Add `code` subdomain to the EGG router

**Problem:** `eggResolver.ts` line 135 already contains `'code.shiftcenter.com': 'code'`

**Required wording:**
> Verify `code` subdomain exists in eggResolver.ts hardcoded fallback table (line 135)

---

## Recommendation

**Follow Option A.** The task file is 95% correct — only needs path corrections and one wording clarification. This is cycle 1 of 2, so we have one more correction cycle available.

After you correct the task file, I will review it again and approve for dispatch if corrections are correct.

---

## Files Involved

- Original spec: `.deia/hive/queue/_active/2026-03-24-SPEC-MON-004-code-egg.md`
- Task file to fix: `.deia/hive/queue/_stage/2026-03-24-TASK-MON-004-code-egg.md`
- Regent review: `.deia/hive/responses/20260324-REGENT-QUEUE-TEMP-2026-03-24-SPEC-MON-004-RESPONSE.md`
- Fix spec (INVALID): `TASK-BEE-R00.md` (the current prompt you're reading)

---

## Your Action

1. Read the task file at `_stage/2026-03-24-TASK-MON-004-code-egg.md`
2. Make the two corrections listed above
3. Write updated task file (same location, overwrite)
4. Report back to Q33NR with summary of changes
5. Wait for cycle 2 review
