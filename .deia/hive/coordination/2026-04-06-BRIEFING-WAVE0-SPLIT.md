# BRIEFING: Split WAVE0 into Individual Specs

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Model:** sonnet
**Priority:** P0 — blocking tonight's build

---

## Objective

The file `.deia/hive/queue/backlog/TASK-WAVE0-DDD-IMPLEMENTATION.md` contains 4 tasks in a single compound file. The queue scanner only picks up individual `SPEC-*.md` files. Split this into 4 individual spec files and place them in `backlog/` with correct dependency metadata.

---

## Source

Read: `.deia/hive/queue/backlog/TASK-WAVE0-DDD-IMPLEMENTATION.md`

This contains:
- TASK-WAVE0-A: Directory Structure + Task Template Update (haiku, no deps)
- TASK-WAVE0-B: QA Bee Dispatch Logic + qa_review_log (sonnet, no deps)
- TASK-WAVE0-C: Scheduler State Machine Extension (sonnet, depends on A+B)
- TASK-WAVE0-D: BAT End-to-End Validation (sonnet, depends on C)

Also read the process spec for full context: `.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md`

---

## Work Required

### 1. Create 4 individual spec files in `.deia/hive/queue/backlog/`

Split the compound file into:
- `SPEC-WAVE0-A-ddd-directories.md`
- `SPEC-WAVE0-B-qa-dispatch-logic.md`
- `SPEC-WAVE0-C-scheduler-state-machine.md`
- `SPEC-WAVE0-D-bat-e2e-validation.md`

Each spec must follow the standard queue spec format with these sections:
- `## Priority` (P0 for all)
- `## Model Assignment` (haiku for A, sonnet for B/C/D)
- `## Depends On` (None for A/B, SPEC-WAVE0-A + SPEC-WAVE0-B for C, SPEC-WAVE0-C for D)
- `## Intent` (from the source task objective)
- `## Files to Read First` (relevant existing files the bee needs)
- `## Acceptance Criteria` (copy from source, must use `- [ ]` checkbox format)
- `## Constraints` (from source + standard: no file over 500 lines, no stubs, no git ops)
- `## Smoke Test` (how to verify the task completed)

### 2. Add "Files to Read First" paths

Each spec needs file paths the bee should read. Key references:
- A: `.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md`, `.deia/hive/scripts/dispatch/dispatch.py`
- B: `.deia/hive/scripts/queue/run_queue.py`, `.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md`
- C: `hivenode/scheduler/scheduler_daemon.py`, `hivenode/scheduler/dispatcher_daemon.py`
- D: All files created by A, B, C

### 3. Remove the compound file

After splitting, delete `TASK-WAVE0-DDD-IMPLEMENTATION.md` from backlog/ so it doesn't confuse anything.

---

## Deliverable

- 4 `SPEC-WAVE0-*.md` files in `.deia/hive/queue/backlog/`
- Compound file removed
- Response file confirming all 4 specs written with correct dependencies

---

## Constraints

- Do NOT dispatch any bees. Just write the spec files.
- Do NOT modify any code.
- Use `- [ ]` checkbox format for all acceptance criteria (Gate 0 requirement).
- Do NOT use backticks around file paths in "Files to Read First" sections (Gate 0 requirement).
- Do NOT append descriptions after file paths with ` — ` (Gate 0 requirement).
