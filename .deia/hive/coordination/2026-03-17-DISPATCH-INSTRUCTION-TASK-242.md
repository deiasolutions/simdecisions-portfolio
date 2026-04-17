# DISPATCH INSTRUCTION: TASK-242

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17 15:18

---

## Approval Status

✅ **APPROVED FOR DISPATCH**

Both task files reviewed and approved. All mechanical checks passed (see `2026-03-17-APPROVAL-TASK-242.md`).

---

## Answers to Q33N's Questions

### 1. Efemera auth
**Q:** Should efemera routes require authentication?

**A:** Yes, eventually. But for now, TASK-242-B correctly handles both cases. The test logs INFO if no auth (current state) and asserts 401/403 if auth is added later. This is the right approach. No changes needed.

### 2. Theme toggle location
**Q:** Where is the theme switcher exposed in production UI?

**A:** Unknown at this time. TASK-242-A test 5 correctly handles this with a graceful skip if `[aria-label="Toggle theme"]` is not found. The test will log "Theme toggle not found in production - skipping" and return early. This is acceptable. No changes needed.

### 3. Dispatch priority
**Q:** Should TASK-242 wait for TASK-241 completion, or run in parallel?

**A:** TASK-242 can run NOW. TASK-241 is about verifying production URLs work, but TASK-242 tests already handle unreachable URLs gracefully (pytest.skip, console.log). If production is down, tests will skip — which is fine. Dispatch both tasks immediately.

---

## Dispatch Instructions

### TASK-242-A: Expand Playwright Smoke Tests
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-242-A-playwright-smoke-expansion.md --model haiku --role bee --inject-boot
```

### TASK-242-B: Create Backend API Smoke Tests
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-242-B-backend-api-smoke.md --model haiku --role bee --inject-boot
```

**Dispatch mode:** PARALLEL (both tasks are independent)

**Slot usage:** 2 of 5 slots (assuming peak hours, max_parallel_bees=5)

---

## Monitoring Requirements

After dispatch, Q33N MUST:

1. **Poll `.deia/hive/responses/` every 60 seconds** for:
   - `20260317-TASK-242-A-RESPONSE.md`
   - `20260317-TASK-242-B-RESPONSE.md`

2. **Review each response inline immediately:**
   - Verify all 8 sections present
   - Check test pass/fail counts
   - Verify no stubs shipped
   - Check for regressions

3. **Backfill slots** when bees complete

4. **Report to Q33NR** when BOTH bees complete with:
   - Summary: tasks completed/failed
   - Test counts: Playwright (9 → 14), Backend (0 → 3)
   - Any issues or follow-ups

---

## Expected Outcomes

**TASK-242-A:**
- `browser/e2e/deploy-smoke.spec.ts` updated with 5 new tests
- Test count increases from 9 to 14
- File size: ~226 lines (under 500 limit)
- All tests pass or gracefully skip (FAB menu, theme toggle)

**TASK-242-B:**
- `tests/smoke/test_production_api.py` created with 3 tests
- File size: ~112 lines (under 150 target)
- All tests pass or skip if production unreachable

---

## Authorization

**Q33NR AUTHORIZES:** Dispatch both bees immediately in parallel.

**Q33N:** Execute dispatch commands above. Monitor responses. Report results.

---

**Q33NR (signing off)**
