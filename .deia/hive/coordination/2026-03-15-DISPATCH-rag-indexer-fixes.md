# DISPATCH INSTRUCTION: RAG Indexer Fixes

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-15
**Time:** 14:36

---

## Approval

I have reviewed your 3 task files (TASK-161, TASK-162, TASK-163). All passed mechanical review.

**✅ APPROVED FOR DISPATCH**

---

## Dispatch Instructions

Dispatch the 3 tasks in this order:

### Phase 1 (Sequential)
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-161-fix-rag-indexer-imports.md --model haiku --role bee --inject-boot --timeout 600
```

### Phase 2 (Parallel, after Phase 1 completes)
```bash
# TASK-162
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-162-verify-rag-indexer-e2e.md --model haiku --role bee --inject-boot --timeout 1200 &

# TASK-163
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-163-smoke-test-rag-routes.md --model haiku --role bee --inject-boot --timeout 1200 &
```

---

## After Bees Complete

1. Read all 3 response files from `.deia/hive/responses/`
2. Verify all 8 sections present in each response
3. Check test pass/fail counts
4. Write completion report
5. Report to Q33NR

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-1238-SPE
