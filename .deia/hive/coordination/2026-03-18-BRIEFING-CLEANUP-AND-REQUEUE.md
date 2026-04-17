# BRIEFING: Clean Monitor State + Re-Queue Orphaned Tasks

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P0
**Pre-approved:** Bee dispatch for all fix work

## Context

Triage report is at `.deia/hive/responses/20260318-TRIAGE-STALE-QUEUE-REPORT.md`. Read it first.

## What Q33N Must Do

### Phase 1: Clean monitor-state.json

Remove ALL of these from the active tasks map in `.deia/hive/queue/monitor-state.json`:

**Confirmed completed — clear immediately:**
1. `QUEUE-TEMP-2026-03-18-SPEC-TASK-FIX-HOT-RELOAD-TESTS`
2. `QUEUE-TEMP-2026-03-18-SPEC-TASK-BUG042-bus-ledger-publisher-required`
3. `QUEUE-TEMP-2026-03-18-SPEC-TASK-BUG044-rag-reliability-metadata-missing`
4. `QUEUE-TEMP-2026-03-18-SPEC-TASK-FIX-PIPELINE-SIM-TESTS`
5. `QUEUE-TEMP-2026-03-18-SPEC-TASK-FIX-MOVEAPP-TESTS`
6. `2026-03-18-TASK-FIX-HAIKU-PRICING`
7. `2026-03-18-BRIEFING-FIX-SIM-EGG-TESTS`

**Orphaned — clear from monitor AND handle in Phase 2:**
8. `2026-03-18-SPEC-TASK-BUG043-e2e-server-startup-timeout`
9. `2026-03-18-SPEC-TASK-FIX-SIM-EGG-TESTS`
10. `2026-03-18-TASK-FIX-KANBAN-TEST`

**Also clear this session (will be done by then):**
11. `2026-03-18-BRIEFING-TRIAGE-STALE-QUEUE-TASKS`

### Phase 2: Re-queue orphaned specs and dispatch bees

For each orphaned task:

1. **BUG043-e2e-server-startup-timeout** — spec at `.deia/hive/queue/2026-03-18-SPEC-TASK-BUG043-e2e-server-startup-timeout.md`. Dispatch a bee to execute it.
2. **FIX-SIM-EGG-TESTS** — spec at `.deia/hive/queue/2026-03-18-SPEC-TASK-FIX-SIM-EGG-TESTS.md`. Dispatch a bee to execute it.
3. **FIX-KANBAN-TEST** — investigate first. If no response file exists anywhere, write a fresh task file and dispatch a bee.

Use `dispatch.py` directly for each. Haiku for simple fixes, sonnet for anything complex.

### Phase 3: Report

Write completion report to `.deia/hive/responses/20260318-CLEANUP-REQUEUE-REPORT.md` with:
- Monitor state changes made
- Bees dispatched (task IDs, models)
- Any issues found

## Constraints

- Do NOT dispatch bees yet. Write task files for the orphaned specs and return them to Q33NR for review FIRST. Follow the chain: Q33N writes tasks → Q33NR reviews → Q33NR approves → Q33N dispatches.
- Do NOT touch the tasks marked "keep active" in the triage report.
- Clean the monitor state BEFORE writing new task files (free the slots).
- Phase 1 (monitor cleanup) you can do immediately. Phase 2 (task files) requires Q33NR review before dispatch.
