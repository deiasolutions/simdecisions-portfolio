# DISPATCH INSTRUCTION: BL-208

**From:** Q88NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17

---

## Instruction

**APPROVED.** Dispatch bee for TASK-BL-208.

---

## Task File
`.deia/hive/tasks/2026-03-17-TASK-BL-208-app-directory-sort-order.md`

---

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-BL-208-app-directory-sort-order.md --model haiku --role bee --inject-boot
```

---

## After Dispatch

1. Monitor bee completion
2. Read bee response file when complete
3. Verify all 8 sections present
4. Verify test count (14-16 passing)
5. Verify no stubs shipped
6. Report results to Q88NR

---

**End of instruction.**
