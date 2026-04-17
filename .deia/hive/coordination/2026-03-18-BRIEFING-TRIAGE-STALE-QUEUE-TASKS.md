# BRIEFING: Triage Stale Queue Tasks

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P0 — blocking all queue work

## Objective

12 queue tasks show as "active" but have been running for over an hour with no bee processes behind them (a crash killed hivenode earlier). Determine which are dead orphans vs actually completed, clean up the queue state, and report findings.

## Context

After a system crash, hivenode restarted but the queue runner still shows 12 tasks as active/running. No `node.exe` bee processes exist (only Vite). These are ghost entries.

## Active Tasks to Triage

1. `2026-03-18-BRIEFING-BUG-043-e2e-server-startup` (dispatched, sonnet, queen)
2. `QUEUE-TEMP-2026-03-18-SPEC-TASK-FIX-HOT-RELOAD-TESTS` (running, sonnet)
3. `QUEUE-TEMP-2026-03-18-SPEC-TASK-BUG043-e2e-server-startup-timeout` (running, sonnet)
4. `QUEUE-TEMP-2026-03-18-SPEC-TASK-FIX-MOVEAPP-TESTS` (running, sonnet)
5. `QUEUE-TEMP-2026-03-18-SPEC-TASK-FIX-SIM-EGG-TESTS` (running, sonnet)
6. `2026-03-18-BRIEFING-FIX-SIM-EGG-TESTS` (dispatched, sonnet, queen)
7. `2026-03-18-DISPATCH-INSTRUCTION-BUG-044` (running, sonnet)
8. `2026-03-18-TASK-FIX-KANBAN-TEST` (running, haiku)
9. `2026-03-18-TASK-FIX-HAIKU-PRICING` (running, haiku)
10. `2026-03-18-BRIEFING-FULL-TEST-SWEEP` (running, sonnet)

## What Q33N Must Do

1. **Check `.deia/hive/responses/`** for any response files matching these tasks. If a response exists, the bee completed before crashing.
2. **Check `.deia/hive/queue/_done/`** for any matching spec files that were already moved.
3. **For each task, determine status:** COMPLETED (response exists), DEAD (no response, no bee process), or UNKNOWN.
4. **Clear the stale active entries** from the queue runner state. The state file is at `.deia/hive/queue/monitor-state.json` — remove entries for dead tasks so the queue runner can accept new work.
5. **For tasks that were DEAD (no response):** check if the original spec still exists in `.deia/hive/queue/` so it can be re-queued.
6. **Write a triage report** to `.deia/hive/responses/20260318-TRIAGE-STALE-QUEUE-REPORT.md` listing each task, its status, and recommended action (re-queue, mark done, or drop).

## Files to Read First

- `.deia/hive/queue/monitor-state.json`
- `.deia/hive/responses/` (scan for 20260318-* files)
- `.deia/hive/queue/` (active specs)
- `.deia/hive/queue/_done/` (completed specs)

## Constraints

- Do NOT delete spec files. Only update monitor-state.json to clear stale active entries.
- After triage: dispatch bees to fix any tasks that were DEAD (no response file). Re-queue the original specs or write new task files as needed.
- Q33NR has pre-approved bee dispatch for all fix work identified in this triage.
- Report back to Q33NR with findings + dispatch confirmations.
