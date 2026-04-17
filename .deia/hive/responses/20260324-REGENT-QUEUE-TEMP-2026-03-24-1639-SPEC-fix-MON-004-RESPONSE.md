# SPEC-fix-MON-004-code-egg: Fix failures from MON-004 -- INVALID

**Status:** INVALID (fix spec inappropriate, root cause is task file review failure)
**Reviewer:** Q33NR-bot (Regent)
**Date:** 2026-03-24

---

## Files Modified

None. This fix spec was not executed.

---

## What Was Done

**Analysis:** The fix spec requested fixing "errors reported after processing MON-004," but investigation revealed:

1. Original MON-004 never reached bee execution
2. It failed during regent mechanical review (cycle 1 of 2)
3. Failure reason: task file had relative paths instead of absolute paths (Rule 8 violation)
4. Queue runner interpreted review rejection as dispatch failure and auto-generated this fix spec

**Action taken:**

- Wrote briefing for Q33N: `.deia/hive/coordination/2026-03-24-BRIEFING-FIX-MON-004-CORRECTION.md`
- Briefing explains the real issue and provides corrected path requirements
- Recommended Option A: fix the existing task file and re-run cycle 2 review

**No code changes made.** This is a process/workflow issue, not a code bug.

---

## Test Results

N/A — no code was executed.

---

## Build Verification

N/A — no build changes.

---

## Acceptance Criteria

**Original criteria from fix spec:**

- [ ] All original acceptance criteria still pass — **INVALID CRITERION** (no original code to test)
- [ ] Reported errors are resolved — **COMPLETE** (root cause identified: task file paths)
- [ ] No new test regressions — **N/A** (no code changes)

**What actually needs to happen:**

1. Q33N corrects task file paths (see briefing)
2. Q33NR reviews corrected task (cycle 2 of 2)
3. If approved, Q33N dispatches BEE-HAIKU with corrected task
4. Bee writes code, runs tests, produces response

---

## Clock / Cost / Carbon

- **Clock:** 8 minutes (investigation + briefing + response)
- **Cost:** $0.12 USD (Sonnet, ~4K tokens in/out)
- **Carbon:** ~0.15g CO2e

---

## Issues / Follow-ups

### Root Cause: Queue Runner Misinterprets Review Rejections

The queue runner created a fix spec when the regent rejected a task file during mechanical review. This is incorrect behavior — review rejections should trigger correction cycles (up to 2), not fix specs.

**Fix specs should only be created when:**
- A bee completes execution but tests fail
- A bee completes execution but acceptance criteria are not met
- A bee produces broken code that breaks other tests

**Fix specs should NOT be created when:**
- Regent rejects task file during review (use correction cycles)
- Spec is blocked by dependencies (mark as blocked, not failed)
- Spec is malformed (reject at queue entry, not after processing)

**Recommendation:** Update queue runner logic to distinguish between:
1. Review rejection → correction cycle (max 2)
2. Bee execution failure → fix spec (max 2)
3. After 2 correction cycles → approve with ⚠️ APPROVED_WITH_WARNINGS

### Next Steps

1. **Q33N:** Read briefing `.deia/hive/coordination/2026-03-24-BRIEFING-FIX-MON-004-CORRECTION.md`
2. **Q33N:** Correct task file paths as specified
3. **Q33NR:** Review corrected task (cycle 2)
4. **Q33N:** Dispatch BEE-HAIKU when approved
5. **Q88N:** Consider updating queue runner to handle review rejections correctly

---

## Disposition

**INVALID** — This fix spec addresses a non-existent code failure. The real issue is task file formatting (absolute paths required). A briefing has been written for Q33N to correct the task file and proceed through the normal review cycle.

The original spec (MON-004) remains in queue and will be completed once the task file is corrected and approved.
