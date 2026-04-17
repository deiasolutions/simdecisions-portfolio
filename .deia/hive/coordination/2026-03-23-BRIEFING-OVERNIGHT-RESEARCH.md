# Briefing: Overnight Research Dispatch
**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-23
**Model:** Sonnet

---

## Objective

Dispatch and monitor 10 research bees that audit the shiftcenter monorepo against old platform repos. Read-only research — no code changes, no commits.

## Plan

The full research plan is at: `C:\Users\davee\Downloads\OVERNIGHT-RESEARCH-PLAN.md`

Q88N's dispatch answers are at: `C:\Users\davee\Downloads\Q33NR-DISPATCH-ANSWERS.md`

Read both before proceeding.

## Task Files — Already Written

All 10 task files are in `.deia/hive/tasks/`:

| File | Bee | Wave |
|------|-----|------|
| TASK-BEE-R00.md | Environment baseline | 0 (solo, first) |
| TASK-BEE-R01.md | Shell + Layout + DnD | A |
| TASK-BEE-R02.md | Canvas + ReactFlow | A |
| TASK-BEE-R03.md | Terminal + Commands | A |
| TASK-BEE-R04.md | EGG System + App Registry | A |
| TASK-BEE-R05.md | Hivenode Backend | A |
| TASK-BEE-R06.md | Channels + Chat + Efemera | A |
| TASK-BEE-R07.md | CSS / Hardcoded Colors | B |
| TASK-BEE-R08.md | Dead Code + Architecture | B |
| TASK-BEE-R09.md | Bug/Backlog Triage | B |
| TASK-BEE-R10.md | Port Checklist Refresh | C (after R01-R06) |

Review them. If corrections are needed, fix them before dispatching.

## Dispatch Order

```
WAVE 0: Dispatch R00 alone. Wait for completion.
         If build is red → STOP. Report to Q33NR.
         If build is green → proceed.

WAVE A+B: Dispatch R01-R09 in parallel (9 bees).
          Q88N has approved exceeding the normal 5-bee limit for this batch.
          Wait for R01-R06 to complete.

WAVE C: Dispatch R10 after R01-R06 response files exist.
        R10 consumes their findings.
```

## Dispatch Command

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TASK-BEE-RXX.md --model sonnet --role bee --inject-boot
```

All bees use Sonnet. All bees get `--inject-boot`.

## Shared Log

Already initialized at: `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`

Every bee is instructed to append findings there in real-time.

## Response Files

Each bee writes its response to `.deia/hive/responses/2026-03-23-BEE-RXX-RESPONSE-*.md`

## Old Repos Location

All under `C:\Users\davee\OneDrive\Documents\GitHub\platform\`:
- `platform/efemera/src/efemera/` — DES, PHASE-IR, RAG, etc.
- `platform/simdecisions-2/src/components/` — Canvas, shell, flow designer
- `platform/` root — canonical/, services, KB

## What to Report Back

When all bees complete:
1. Which bees completed vs failed
2. Summary of critical findings from the shared log
3. Whether R10's port checklist refresh was produced
4. Any bees that need re-dispatch

## Constraints

- No code changes. Read-only research.
- No git writes.
- All bees are read-only. If a bee tries to modify code, that's a bug in the task file.
