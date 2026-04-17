# TASK-222: PipelineStore Protocol + FilesystemPipelineStore (W1-A)

## Objective
Extract filesystem operations from `run_queue.py` behind a `PipelineStore` ABC. Implement `FilesystemPipelineStore`. Refactor `run_queue.py` to use it. All existing queue runner tests still pass. Pure refactor, zero new behavior.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). This is the foundational abstraction that enables dual-runtime (filesystem for production, in-memory for DES simulation). The same pipeline code runs against either adapter.

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Sections 6.1 and 6.2

## Files to Read First
- `.deia/hive/scripts/queue/run_queue.py` — current queue runner, extract filesystem ops from here
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 6 (PipelineStore Protocol)

## Deliverables
- [ ] Create `.deia/hive/scripts/queue/pipeline_store.py`
  - `SpecFile` dataclass: id, filename, priority, depends_on, hold_until, added_at, content, manifest
  - `PipelineStore` ABC with methods: list_specs, move_spec, append_section, get_done_ids, deps_satisfied, emit_event, get_orphans
- [ ] Create `.deia/hive/scripts/queue/filesystem_store.py`
  - `FilesystemPipelineStore(PipelineStore)` backed by pathlib
  - Stage mapping: hold, queue, active, done, failed, needs_review, dead
  - `move_spec` moves file between stage directories + emits transition event
  - `append_section` appends markdown section to spec file
  - `get_done_ids` returns set of spec IDs from `_done/`
  - `deps_satisfied` checks all deps are in `_done/`
  - `get_orphans` returns specs in `_active/`
- [ ] Refactor `run_queue.py` to use `FilesystemPipelineStore` instead of raw pathlib calls
  - All existing queue runner tests must still pass
  - No new behavior, pure refactor
- [ ] Create tests in `.deia/hive/scripts/queue/tests/test_pipeline_store.py`
  - Test SpecFile creation
  - Test list_specs returns correct specs per stage
  - Test move_spec moves files between directories
  - Test deps_satisfied checks _done/ correctly
  - Test get_orphans finds specs in _active/
  - ~10 tests minimum

## Priority
P1

## Model
haiku
