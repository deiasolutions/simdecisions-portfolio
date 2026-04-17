# BRIEFING: Apps-Home Batch Dispatch

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-14
**Status:** APPROVED — DISPATCH IMMEDIATELY

---

## Objective

Dispatch the APPS-HOME batch. Task files are pre-written and Q88N-approved. You do NOT need to write task files — they already exist. Go straight to dispatch.

## Task Files (all in `.deia/hive/tasks/`)

| Task | File | Model | Role | Wave |
|------|------|-------|------|------|
| T1 | `2026-03-14-Q33N-CODE-TASK-T1.md` | sonnet | bee | 1 |
| T2 | `2026-03-14-Q33N-CODE-TASK-T2.md` | sonnet | bee | 1 |
| T3 | `2026-03-14-Q33N-CODE-TASK-T3.md` | sonnet | bee | 1 |
| T4 | `2026-03-14-Q33N-CODE-TASK-T4.md` | haiku | bee | 2 |
| T5 | `2026-03-14-Q33N-CODE-TASK-T5.md` | sonnet | bee | 3 |

## Wave Plan

```
Wave 1 (parallel): T1 + T2 + T3  — dispatch all three simultaneously
Wave 2 (sequential): T4           — dispatch AFTER Wave 1 completes
Wave 3 (sequential): T5           — dispatch AFTER T4 completes
```

## Your Process

1. **Read each task file** to confirm they're well-formed
2. **Dispatch Wave 1** — T1, T2, T3 in parallel:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-Q33N-CODE-TASK-T1.md --model sonnet --role bee --inject-boot
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-Q33N-CODE-TASK-T2.md --model sonnet --role bee --inject-boot
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-Q33N-CODE-TASK-T3.md --model sonnet --role bee --inject-boot
   ```
3. **Wait for all 3 to complete.** Check `.deia/hive/responses/` for response files.
4. **Review Wave 1 responses.** Verify all 8 sections present, tests pass, no stubs.
5. **Dispatch Wave 2** — T4 (haiku):
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-Q33N-CODE-TASK-T4.md --model haiku --role bee --inject-boot
   ```
6. **Wait and review T4 response.**
7. **Dispatch Wave 3** — T5 (sonnet):
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-Q33N-CODE-TASK-T5.md --model sonnet --role bee --inject-boot
   ```
8. **Wait and review T5 response.**
9. **Write completion report** to `.deia/hive/responses/` and archive completed tasks.

## Constraints

- Do NOT rewrite the task files — they are approved
- Do NOT create `_outbox/` directories
- Do NOT dispatch bees before confirming each wave's predecessor completed
- If a bee fails: dispatch a fix task, do NOT re-dispatch the original
- Max 3 bees in parallel (Wave 1 is exactly 3)

## What's Being Built

An EGG directory home page (`apps.shiftcenter.com`). 14-card grid UI with search, grouped into Core/Productivity/Platform sections. It's a new EGG (`apps-home`) with its own React component, registry service, adapter, and test suite.
