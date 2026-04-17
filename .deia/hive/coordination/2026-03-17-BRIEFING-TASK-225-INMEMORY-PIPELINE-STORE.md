# Briefing: TASK-225 InMemoryPipelineStore Implementation

**To:** Q33N (Queen Coordinator)
**From:** Q88NR-bot (Regent)
**Date:** 2026-03-17
**Source Spec:** `2026-03-16-SPEC-TASK-225-inmemory-pipeline-store.md`
**Priority:** P1
**Model Assignment:** haiku

---

## Objective

Implement an in-memory version of `PipelineStore` ABC for DES runtime simulation. This enables the DES engine to simulate the build pipeline without filesystem I/O.

---

## Context

Part of SPEC-PIPELINE-001 (Unified Build Pipeline). We need two implementations of the same `PipelineStore` ABC:
1. **FilesystemPipelineStore** — Production mode (COMPLETE in TASK-222)
2. **InMemoryPipelineStore** — DES simulation mode (THIS TASK)

The DES (Discrete Event Simulation) engine needs to simulate queue operations without touching the filesystem. The in-memory store uses Python dicts and lists instead of directories and files.

---

## Dependencies

- **TASK-222** (PipelineStore ABC + FilesystemPipelineStore) — ✅ COMPLETE
  - Located: `.deia/hive/scripts/queue/pipeline_store.py`
  - Located: `.deia/hive/scripts/queue/filesystem_store.py`
  - Tests: `.deia/hive/scripts/queue/tests/test_pipeline_store.py`

---

## Files to Read First

Before writing the task file, read these files to understand the interface and reference implementation:

1. `.deia/hive/scripts/queue/pipeline_store.py` — The `PipelineStore` ABC and `SpecFile` dataclass
2. `.deia/hive/scripts/queue/filesystem_store.py` — Reference implementation (use as a pattern for in-memory version)
3. `.deia/hive/scripts/queue/tests/test_pipeline_store.py` — Existing filesystem tests (mirror these for in-memory tests)
4. `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 6.3 (context on DES integration)

---

## Deliverables Required

**Your task file MUST include these deliverables:**

1. **Implementation file:** `.deia/hive/scripts/queue/inmemory_store.py`
   - Class `InMemoryPipelineStore(PipelineStore)` implementing all abstract methods
   - Use Python dicts and lists (no filesystem operations)
   - Stages as dict of lists: `{"hold": [], "queue": [], "active": [], ...}`
   - Events list: `self.events = []` (append-only log)
   - Full implementation of: `list_specs`, `move_spec`, `get_done_ids`, `deps_satisfied`, `get_orphans`, `emit_event`, `append_section`

2. **Test file:** `.deia/hive/scripts/queue/tests/test_inmemory_store.py`
   - **Mirror the filesystem store tests** from `test_pipeline_store.py`
   - Test all PipelineStore methods work correctly with in-memory state
   - Test event recording
   - Test spec content modification
   - **Minimum 10 tests**

---

## Constraints

- **TDD:** Tests first, then implementation
- **No file over 500 lines** (modularize if needed)
- **No stubs:** Every method fully implemented
- **No filesystem operations:** Pure in-memory (dicts, lists, strings only)
- **Model:** haiku (fast, low-cost for straightforward implementation)

---

## Test Requirements

The bee MUST:
- Write tests FIRST (TDD)
- Mirror the structure of filesystem store tests
- Verify all abstract methods work correctly
- Test edge cases (empty stages, missing specs, dependency checking)
- Run pytest and verify all tests pass
- Include test count in response file

---

## Acceptance Criteria from Spec

- [ ] `InMemoryPipelineStore` class exists and inherits from `PipelineStore`
- [ ] All abstract methods implemented (no `NotImplementedError`)
- [ ] Stages stored as dict of lists (7 stages: hold, queue, active, done, failed, needs_review, dead)
- [ ] Events stored as append-only list
- [ ] Spec content stored and modifiable (append_section works)
- [ ] Tests mirror filesystem store tests (≥10 tests)
- [ ] All tests pass
- [ ] No filesystem operations in implementation

---

## Review Checklist for You (Q33N)

Before returning the task file to me, verify:

- [ ] File paths are absolute (Windows format: `C:\Users\davee\OneDrive\...`)
- [ ] Deliverables match the spec (implementation file + test file)
- [ ] Test requirements clearly specified (TDD, mirror filesystem tests, ≥10 tests)
- [ ] No hardcoded colors (N/A for this task — no CSS)
- [ ] No files over 500 lines
- [ ] Response file template included in task file
- [ ] Model assignment: haiku

---

## Next Steps

1. Read the files listed above
2. Write a single task file for this work (bee-sized unit)
3. Return the task file to me (Q88NR) for review
4. **Do NOT dispatch yet** — wait for my approval

---

**End of Briefing**
