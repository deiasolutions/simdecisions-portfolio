# DISPATCH INSTRUCTION: BUG-021 Verification

**From:** Q88NR-bot (Regent)
**To:** Worker Bee (haiku)
**Date:** 2026-03-17
**Task File:** `.deia/hive/tasks/2026-03-17-TASK-BUG-021-VERIFY.md`
**Priority:** P0

---

## Task Summary

Verify that BUG-021 (canvas minimap white visible zone, corner misalignment) is already fixed via manual testing and close the bug.

---

## Mechanical Review: APPROVED ✅

All checklist items passed:
- ✅ Deliverables match spec
- ✅ File paths absolute (Windows `C:\...` format)
- ✅ Test requirements present (minimap.styles.test.tsx)
- ✅ No code changes (verification only)
- ✅ Response template present (8 sections + BUG-021 status)

---

## Key Instructions for Bee

1. **Read the files** listed in "Files to Read First"
2. **Run the test file:**
   ```bash
   cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/minimap.styles.test.tsx
   ```
3. **Search git history** for BUG-021 fix:
   ```bash
   git log --all --grep="BUG-021" -- browser/src/primitives/canvas/canvas.css
   git log --all -p -- browser/src/primitives/canvas/canvas.css | grep -A 10 -B 10 "BUG-021"
   ```
4. **Manual verification** (if dev server running):
   - Open Canvas EGG in browser
   - Check minimap visible zone color (should be purple, NOT white)
   - Check corner alignment (should be clean)
5. **Write response file** to `.deia/hive/responses/20260317-TASK-BUG-021-VERIFY-RESPONSE.md`
   - Include all 8 mandatory sections
   - Add BUG-021 Status section with recommendation (CLOSE_BUG or RE-OPEN)

---

## Expected Outcome

**If already fixed (most likely):**
- Response file status: COMPLETE
- BUG-021 Status: VERIFIED_FIXED
- Recommendation: CLOSE_BUG
- Evidence: Test results + git commit showing fix

**If still broken (unlikely):**
- Response file status: FAILED
- BUG-021 Status: STILL_EXISTS
- Recommendation: RE-OPEN
- Evidence: Screenshots or detailed description of remaining issues

---

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-BUG-021-VERIFY.md --role bee --model haiku
```

---

**Regent Signature:** Q88NR-bot
**Timestamp:** 2026-03-17T23:27:00Z
