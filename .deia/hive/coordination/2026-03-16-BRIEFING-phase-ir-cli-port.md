# BRIEFING: Port PHASE-IR CLI toolchain + domain vocabularies

**Date:** 2026-03-16
**From:** Q88NR (Regent)
**To:** Q33N (Queen Coordinator)
**Priority:** P0.10
**Model Assignment:** Sonnet
**Spec ID:** QUEUE-TEMP-2026-03-15-0753-SPEC-w1-02-phase-ir-cli

---

## Objective

Port the PHASE-IR CLI toolchain from platform repo. This includes:
- 13 CLI subcommands for flow management, validation, compilation, and analysis
- Domain vocabulary YAML files

**Source:** `platform/efemera/src/efemera/phase_ir/cli.py` (578 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py`
**Vocab Source:** `platform/efemera/src/efemera/phase_ir/vocabularies/`
**Vocab Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\vocabularies\`

---

## Context

PHASE-IR core was ported in TASK-146 (248 tests passing). The CLI toolchain is the next piece. It provides command-line access to PHASE-IR's flow engine.

**Key dependencies already ported:**
- `engine/phase_ir/` (core modules)
- `engine/database.py` (SQLAlchemy Base)
- Routes registered in `hivenode/routes/__init__.py`

**What memory.md says:**
> PHASE-IR Port — COMPLETE (2026-03-14)
> - Ported from: `platform/efemera/src/efemera/phase_ir/` (16 files, ~5,100 lines)
> - Ported to: `engine/phase_ir/` (now ~6,400 lines total)
> - 13 source files ported + 1 schema JSON + 8 test files
> - 15 API endpoints under `/api/phase` + `/api/phase/traces`
> - 81 exports in `engine/phase_ir/__init__.py`
> - Tests: 248 passed across 8 test files

---

## Acceptance Criteria (from spec)

- [ ] CLI module ported with all 13 subcommands
- [ ] Domain vocabulary YAMLs copied
- [ ] `python -m engine.phase_ir --help` works
- [ ] Tests for CLI commands written and passing

---

## Constraints (from spec)

- Max 500 lines per file (hard limit: 1,000)
- TDD: tests first, then implementation
- No stubs or TODOs — full implementation or explicit "cannot finish" with reason
- CSS: `var(--sd-*)` only (N/A for this task)
- POST heartbeats to `http://localhost:8420/build/heartbeat` every 3 minutes:
  ```json
  {
    "task_id": "2026-03-15-0753-SPEC-w1-02-phase-ir-cli",
    "status": "running",
    "model": "sonnet",
    "message": "working"
  }
  ```

---

## Smoke Test (from spec)

- [ ] `python -m pytest tests/engine/phase_ir/test_cli.py -v`
- [ ] No new test failures

---

## Your Task, Q33N

1. **Read the source files** from platform repo:
   - `platform/efemera/src/efemera/phase_ir/cli.py` (main CLI module)
   - `platform/efemera/src/efemera/phase_ir/vocabularies/*.yml` (domain vocab files)

2. **Determine task breakdown:**
   - The source CLI is 578 lines. This needs modularization per Rule 4 (max 500).
   - Identify natural split points (e.g., subcommand groups).
   - Determine if vocabularies can be copied as-is or need adjustments.

3. **Write task files** for bees:
   - One task per module (if splitting CLI)
   - One task for vocabularies (copy + verify)
   - One task for tests

4. **Include in each task:**
   - Absolute file paths
   - Specific test requirements (how many tests, which scenarios)
   - All 8 sections of the response file template
   - Heartbeat requirement for long-running tasks

5. **Return task files to me (Q88NR) for review.**

Do NOT dispatch bees yet. I will review your task files first.

---

## Files to Check First

Before writing tasks, read these to understand the existing structure:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\flow.py` (flow engine)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\` (test patterns)
- `platform/efemera/src/efemera/phase_ir/cli.py` (source to port)

---

## Budget Note

This is a P0.10 spec. Session budget enforcement is active. Track costs accurately.

---

## End of Briefing

Q33N: Read the source, plan the task breakdown, write task files, and return them to me for review.
