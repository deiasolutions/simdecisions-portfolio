# Q33N Coordination: Dispatch Bees for Build Queue Phase 1

**From:** Q33NR
**Role:** queen
**Date:** 2026-03-11

---

## Your Job

You are Q33N. Four task files are approved. Dispatch bees in two batches, review results, report back.

## Dispatch Strategy

### Batch 1 — Parallel (independent tasks)

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023A-QUEUE-CONFIG.md --model haiku --role bee --inject-boot

python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023B-REGENT-PROMPT.md --model haiku --role bee --inject-boot

python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023C-MORNING-REPORT.md --model sonnet --role bee --inject-boot
```

All three are independent. Dispatch in parallel.

### Batch 2 — Sequential (depends on Batch 1)

After Batch 1 completes and all three bees report clean:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-11-TASK-023D-QUEUE-RUNNER.md --model sonnet --role bee --inject-boot
```

TASK-023D imports from morning_report.py (TASK-023C) and reads queue.yml (TASK-023A). Must run after those land.

## After Each Batch

1. Read response files in `.deia/hive/responses/`
2. Verify: all 8 sections present, tests pass, no stubs
3. If a bee fails: dispatch a fix task (same model)
4. Log results

## After All Bees Complete

1. Run queue tests: `cd .deia/hive/scripts/queue && python -m pytest tests/ -v`
2. Report to Q33NR: pass/fail per task, test counts, any issues
3. Do NOT archive yet — Q33NR will instruct
