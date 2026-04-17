# DISPATCH INSTRUCTION: BUG-015

**From:** Q88NR (Regent)
**Date:** 2026-03-17
**Status:** 🐝 BEE DISPATCHED (background)

---

## Task Details

**Task ID:** BUG-015
**Task File:** `.deia/hive/tasks/2026-03-17-TASK-BUG-015-drag-onto-occupied-pane.md`
**Model:** Haiku
**Role:** Bee (worker)
**Timeout:** 1800s (30 min)
**Background Task ID:** b7bd507

---

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-17-TASK-BUG-015-drag-onto-occupied-pane.md \
  --model haiku \
  --role bee \
  --inject-boot \
  --timeout 1800
```

**Status:** Running in background

---

## Expected Outputs

**Response File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-015-RESPONSE.md`

**Response File Sections (mandatory 8):**
1. Header (task ID, title, status, model, date)
2. Files Modified
3. What Was Done
4. Test Results
5. Build Verification
6. Acceptance Criteria
7. Clock / Cost / Carbon
8. Issues / Follow-ups

---

## Success Criteria

- [ ] Response file exists with all 8 sections
- [ ] Status: COMPLETE (not FAILED)
- [ ] All acceptance criteria marked [x]
- [ ] Test results show passing tests
- [ ] No stubs shipped
- [ ] No files over 500 lines

---

## Next Steps (Q88NR)

1. Wait for bee to complete (monitor background task b7bd507)
2. Read response file when complete
3. Verify smoke tests passed
4. Review deliverables against acceptance criteria
5. If success: proceed to next spec
6. If failure: create fix spec (max 2 fix cycles)

---

**Q88NR signature**
Bee dispatched. Awaiting completion.
