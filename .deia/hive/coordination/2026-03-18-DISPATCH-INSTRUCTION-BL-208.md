# DISPATCH INSTRUCTION: BL-208

**From:** Q33NR (Queen Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18

---

## Approval Status

✅ **APPROVED** — Task file passes all checklist items.

Approval documented in: `.deia/hive/coordination/2026-03-18-APPROVAL-TASK-BL-208.md`

---

## Dispatch Command

Execute this command to dispatch the bee:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BL-208-APP-DIRECTORY-SORT.md --model haiku --role bee --inject-boot
```

**Model:** Haiku (straightforward sort logic)
**Role:** bee
**Boot injection:** YES

---

## After Bee Completes

1. Read bee response file from `.deia/hive/responses/`
2. Verify all 8 sections present
3. Check test pass counts (expect 13 total: 10 existing + 3 new)
4. Verify no stubs shipped
5. Report to Q33NR with completion summary

---

## Expected Timeline

- **Estimated duration:** 1-2 hours (TDD + implementation + tests)
- **Max turns:** No limit (let bee run to natural completion)

---

**Q33N: Proceed with dispatch and report when bee completes.**
