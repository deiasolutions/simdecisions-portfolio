# DISPATCH INSTRUCTION: TASK-244

**From:** Q33NR (Queen Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Status:** APPROVED — Execute Dispatch

---

## Instruction

Your task file `2026-03-17-TASK-244-landing-page.md` has been reviewed and **APPROVED**.

Proceed with bee dispatch NOW.

---

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-244-landing-page.md --model sonnet --role bee --inject-boot --timeout 7200
```

**Parameters:**
- Task file: `2026-03-17-TASK-244-landing-page.md`
- Model: `sonnet` (front-end UI work)
- Role: `bee` (worker)
- Inject boot: YES (includes BOOT.md and HIVE.md)
- Timeout: 7200 seconds (2 hours — matches Wave 5 estimate)

---

## After Dispatch

1. Wait for bee to complete
2. Read response file: `.deia/hive/responses/20260317-TASK-244-RESPONSE.md`
3. Verify all 8 sections are present
4. Check test results (12+ tests should pass)
5. Check for stubs (should be NONE)
6. Check for regressions
7. Write completion report
8. Report to Q33NR

---

## Expected Artifacts from Bee

1. **New files:**
   - `browser/src/pages/LandingPage.tsx`
   - `browser/src/pages/LandingPage.css`
   - `browser/src/pages/__tests__/LandingPage.test.tsx`

2. **Modified files:**
   - `browser/src/App.tsx` (conditional landing page render)

3. **Response file:**
   - `.deia/hive/responses/20260317-TASK-244-RESPONSE.md` (all 8 sections)

4. **Test results:**
   - Minimum 12 tests passing
   - No hardcoded colors
   - All files under 500 lines
   - Responsive design verified

---

Q33N: Execute dispatch now. Report back when bee completes.
