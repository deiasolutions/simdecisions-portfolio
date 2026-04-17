# DISPATCH INSTRUCTION: BUG-044

**From:** Q33NR (Regent)
**To:** Q33N (Coordinator)
**Date:** 2026-03-18
**Spec:** BUG-044

---

## APPROVED — Dispatch the bee

Task file has been reviewed and approved. Proceed with bee dispatch.

---

## Command to Run

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG-044-A-add-reliability-metadata.md --model haiku --role bee --inject-boot
```

---

## After Bee Completes

1. Read response file: `.deia\hive\responses\20260318-TASK-BUG-044-A-RESPONSE.md`
2. Verify all 8 sections present
3. Verify TestReliabilityMetadata tests pass
4. Report completion to Q33NR

---

**Execute now.**
