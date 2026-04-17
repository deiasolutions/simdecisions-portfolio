# DIRECTIVE: Dispatch TASK-184 and TASK-185 (Sequential)

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Status:** APPROVED — EXECUTE DISPATCH

---

## Instructions

You have approval to dispatch bees for TASK-184 and TASK-185.

**Sequential dispatch required** (TASK-185 depends on TASK-184):

1. Dispatch TASK-184 (haiku)
2. Wait for TASK-184 completion
3. Read TASK-184 response file
4. If TASK-184 COMPLETE → dispatch TASK-185 (haiku)
5. If TASK-184 FAILED → report to Q33NR, do not proceed to TASK-185

---

## Dispatch Commands

```bash
# TASK-184 first
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-184-oauth-url-token-extraction.md --model haiku --role bee --inject-boot

# TASK-185 second (only after TASK-184 completes successfully)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-185-auth-adapter-storage-wiring.md --model haiku --role bee --inject-boot
```

---

## After Completion

1. Read both response files
2. Verify all 8 sections present
3. Check test results (15 new tests expected)
4. Run smoke test: `cd browser && npx vitest run src/primitives/auth/__tests__/`
5. Write completion report to Q33NR

---

**Execute now.**
