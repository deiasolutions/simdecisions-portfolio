# BRIEFING: Q33N-002 — Batch 2 Task Files

**From:** Q33NR
**To:** Q33N-002
**Date:** 2026-03-19
**Priority:** P0

---

## Your Role

You are Q33N-002 (Queen Coordinator). Read `.deia/BOOT.md` and `.deia/HIVE.md` first. Your job: write task files for 3 items, then STOP.

## What You Must Produce

Write **3 task files** to `.deia/hive/tasks/`:

### Item 1: BL-121-C (Canvas-Properties Integration Tests)
- **Task file ALREADY EXISTS** at `.deia/hive/tasks/2026-03-19-TASK-BL121-C-integration-tests.md`
- **REVIEW IT** — verify it has all 8 sections, explicit file boundaries, TDD requirements
- If it's good, leave it. If it needs fixes, fix it in place.
- Model: haiku
- Risk: LOW

### Item 2: TASK-226 (Phase-IR Pipeline Flow)
- **Create new task file:** `.deia/hive/tasks/2026-03-19-TASK-226-PHASE-IR-PIPELINE-FLOW.md`
- **What it does:** Create a pipeline flow module that converts Phase-IR execution traces into pipeline stage metrics
- **Context:** Phase-IR already exists at `engine/phase_ir/` (248 tests, 15 endpoints). TASK-228 created `/api/pipeline/simulate` at `hivenode/routes/pipeline_sim.py`. This task bridges them — reading Phase-IR traces and computing flow metrics (stage durations, bottleneck identification, throughput).
- **Files to read first:**
  - `engine/phase_ir/__init__.py` (81 exports)
  - `hivenode/routes/pipeline_sim.py` (253 lines, the simulation endpoint)
  - `engine/phase_ir/schemas/pipeline.ir.json` (if exists)
- **Files bee may modify:** Max 3 files
  - `engine/phase_ir/pipeline_flow.py` (NEW)
  - `tests/engine/phase_ir/test_pipeline_flow.py` (NEW)
  - `engine/phase_ir/__init__.py` (add exports)
- **Files bee must NOT modify:** Everything else. No browser/. No hivenode/routes/.
- **Model:** sonnet
- **Minimum tests:** 8
- **Risk:** LOW (new file, no modifications to existing code)

### Item 3: TASK-227 (LLM Triage Functions)
- **Create new task file:** `.deia/hive/tasks/2026-03-19-TASK-227-LLM-TRIAGE-FUNCTIONS.md`
- **What it does:** Create triage utility functions that classify incoming prompts by intent (simulation, query, design, chat) and route them to the correct handler
- **Context:** Terminal sends prompts to hivenode. Currently there's no classification — everything goes to a single LLM call. This task creates a triage layer that examines the prompt and returns a classification with confidence score.
- **Files to read first:**
  - `hivenode/routes/shell.py` (shell command execution)
  - `hivenode/routes/des_routes.py` (DES endpoints)
  - `hivenode/routes/pipeline_sim.py` (pipeline simulation)
- **Files bee may modify:** Max 3 files
  - `hivenode/triage.py` (NEW)
  - `tests/hivenode/test_triage.py` (NEW)
  - (optionally register in `hivenode/routes/__init__.py` if adding an endpoint)
- **Files bee must NOT modify:** Everything else. No browser/. No engine/.
- **Model:** sonnet
- **Minimum tests:** 10
- **Risk:** LOW (new file, no modifications to existing code)

## Critical Rules for Every Task File

1. **Explicit "Files You May Modify" section** with absolute paths
2. **Explicit "Files You Must NOT Modify" section**
3. **TDD test requirements** with minimum test counts
4. **Build verification commands** with absolute paths
5. **8-section response template** requirement
6. **No stubs allowed** — every function complete
7. **Max 3 files per task**
8. **No browser/ modifications** (protecting recovery work)

## When Done

Write a completion report to `.deia/hive/responses/20260319-Q33N-002-BATCH-2-TASK-FILES.md` listing all 3 task files and their status.

Then STOP. Do NOT dispatch bees.
