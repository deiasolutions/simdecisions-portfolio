# DISPATCH AUTHORIZATION: TASK-158

**From:** Q33NR
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-15

---

## Status

TASK-158 has been reviewed and APPROVED.

**You are authorized to dispatch the bee.**

---

## Task File

`.deia/hive/tasks/2026-03-15-TASK-158-fix-shell-chrome-css-violations.md`

---

## Dispatch Instructions

**Model:** haiku (simple find-replace task)
**Role:** bee
**Inject Boot:** yes

**Command:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-158-fix-shell-chrome-css-violations.md --model haiku --role bee --inject-boot
```

---

## After Bee Completes

1. Read the bee response file: `.deia/hive/responses/20260315-TASK-158-RESPONSE.md`
2. Verify all 8 sections present
3. Verify all 60 tests pass
4. Verify CSS compliance check passes (no matches)
5. Write completion report to `.deia/hive/responses/20260315-DISPATCH-shell-chrome-css-fix-COMPLETION-REPORT.md`
6. Report to Q33NR

---

## Success Criteria

- [ ] All 4 rgba() calls replaced
- [ ] All 60 tests passing
- [ ] CSS compliance check: no matches
- [ ] Response file: all 8 sections

---

**Q33N: Execute dispatch and report results.**
