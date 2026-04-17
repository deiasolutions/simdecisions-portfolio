# DISPATCH INSTRUCTION: BUG-038

**From:** Q33NR (Queen Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18

---

## Instruction

Your task files for BUG-038 have been reviewed and APPROVED.

**You are authorized to dispatch all 3 bees sequentially.**

---

## Dispatch Sequence

### Step 1: Dispatch TASK-BUG-038-A
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-038-A-PALETTE-DRAG-METADATA.md \
  --model haiku --role bee --inject-boot
```

**WAIT FOR COMPLETION.** Read response file: `.deia/hive/responses/20260318-TASK-BUG-038-A-RESPONSE.md`

### Step 2: Dispatch TASK-BUG-038-B
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-038-B-CANVAS-DRAG-HANDLERS.md \
  --model haiku --role bee --inject-boot
```

**WAIT FOR COMPLETION.** Read response file: `.deia/hive/responses/20260318-TASK-BUG-038-B-RESPONSE.md`

### Step 3: Dispatch TASK-BUG-038-C
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-038-C-INTEGRATION-TEST.md \
  --model haiku --role bee --inject-boot
```

**WAIT FOR COMPLETION.** Read response file: `.deia/hive/responses/20260318-TASK-BUG-038-C-RESPONSE.md`

---

## After All 3 Complete

1. **Read all 3 response files**
2. **Verify:**
   - All response files have 8 sections
   - All tests pass (4+ in A, 8+ in B, 6+ in C)
   - No stubs shipped
   - No TypeScript errors
3. **Write completion report** to Q33NR
4. **Report file:** `.deia/hive/responses/20260318-Q33N-BUG-038-COMPLETION-REPORT.md`

---

## If Any Bee Fails

1. Read the failure message in the response file
2. Create a P0 fix task
3. Dispatch fix bee
4. Max 2 fix cycles per original task
5. If still failing after 2 cycles: flag NEEDS_DAVE

---

**Proceed, Q33N.**
