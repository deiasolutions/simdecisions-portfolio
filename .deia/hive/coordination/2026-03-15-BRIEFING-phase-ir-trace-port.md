# BRIEFING: Port PHASE-IR trace system from platform

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-15
**Spec ID:** QUEUE-TEMP-2026-03-15-0822-SPEC-w1-03-phase-ir-trace
**Priority:** P0.15
**Model Assignment:** haiku

---

## Objective

Port the PHASE-IR trace system from the platform repo to shiftcenter. This includes:
- Trace module with 25 event types
- JSONL export and import functionality
- Trace API routes
- Comprehensive tests

This continues the PHASE-IR port that began with the core engine port (PHASE-IR Port — COMPLETE per MEMORY.md).

---

## Context from Q88N

This is part of Wave 1 ports. The PHASE-IR core engine was already ported successfully to `engine/phase_ir/` with 248 passing tests. Now we need the trace system, which provides event logging and replay capabilities for simulations.

**Source:** `platform/efemera/src/efemera/phase_ir/trace.py` (~420 lines)
**Targets:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\trace.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\phase_ir_trace.py`

**Pattern to follow:** The existing `engine/phase_ir/store.py` pattern already in the repo.

---

## Key Requirements

1. **25 event types** — The trace system must support all 25 event types from platform
2. **JSONL export/import** — Must be able to export traces to JSONL format and re-import them
3. **API routes** — Routes must be registered under `/api/phase/traces` (parallel to existing `/api/phase` routes)
4. **TDD** — Tests first, then implementation
5. **No stubs** — Every function fully implemented
6. **Modularization** — No file over 500 lines (hard limit: 1,000)

---

## Acceptance Criteria (from spec)

- [ ] Trace module with 25 event types
- [ ] JSONL export and import working
- [ ] Trace API routes registered
- [ ] Tests written and passing

---

## Smoke Test

```bash
python -m pytest tests/engine/phase_ir/ -v
```

No new test failures.

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only (not applicable here, but rule still applies)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-15-0822-SPEC-w1-03-phase-ir-trace", "status": "running", "model": "haiku", "message": "working"}
  ```

---

## Files to Reference

**Platform source (READ ONLY — do NOT modify platform):**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\trace.py`

**Existing shiftcenter patterns:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\store.py` (follow this pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (route registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\` (test patterns)

---

## Task Breakdown Guidance

Suggested breakdown (you may adjust based on actual dependencies):

1. **Port trace.py module** — Core trace system with 25 event types, JSONL export/import
2. **Add trace routes** — API endpoints under `/api/phase/traces`
3. **Register routes** — Update `hivenode/routes/__init__.py`
4. **Tests** — Comprehensive test coverage (TDD)

Keep tasks bee-sized. If trace.py would exceed 500 lines, split into multiple modules.

---

## Known Patterns (from MEMORY.md)

- When a dependency is missing, PORT IT — don't rewrite dependent code
- Follow existing PHASE-IR patterns in `engine/phase_ir/`
- Tests go in `tests/engine/phase_ir/`
- Routes register in `hivenode/routes/__init__.py`
- Exports go in `engine/phase_ir/__init__.py`

---

## What Q33N Should Deliver

1. Task files written to `.deia/hive/tasks/`
2. Each task file includes:
   - Objective (one sentence)
   - Context (what the bee needs to know)
   - Files to Read First (absolute paths)
   - Deliverables (concrete, checkable)
   - Test Requirements (specific scenarios)
   - Constraints (500 lines, no stubs, etc.)
   - Response Requirements (8-section template)
3. Summary of task files for Q33NR review
4. WAIT for Q33NR approval before dispatching bees

---

## Response Format

After creating task files, report to Q33NR with:

```markdown
# Q33N RESPONSE: PHASE-IR Trace Port Task Breakdown

## Task Files Created

1. `.deia/hive/tasks/2026-03-15-TASK-XXX-phase-ir-trace-module.md`
   - Deliverables: [list]
   - Tests: [count/description]
   - Model: haiku

2. `.deia/hive/tasks/2026-03-15-TASK-YYY-phase-ir-trace-routes.md`
   - Deliverables: [list]
   - Tests: [count/description]
   - Model: haiku

[etc.]

## Dependencies

- Task XXX must complete before YYY (or "all tasks independent")

## Dispatch Plan

- [Sequential/Parallel] dispatch
- [Number] bees total
- Estimated completion: [time estimate if applicable]

## Ready for Review

Awaiting Q33NR approval to dispatch.
```

---

**Q33N: Read this briefing, read the platform source, write task files, return for review. Do NOT dispatch yet.**
