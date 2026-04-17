# TASK-225: InMemoryPipelineStore (W2-B)

## Objective
Implement a dict-backed `InMemoryPipelineStore` that satisfies the same `PipelineStore` ABC. In-memory event list. Tests mirror filesystem tests but run in-memory.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). This is the DES runtime adapter. Same interface as `FilesystemPipelineStore`, but uses Python dicts instead of filesystem. Enables the DES engine to simulate the build pipeline without any I/O.

## Depends On
- TASK-222 (PipelineStore ABC must exist)

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 6.3

## Files to Read First
- `.deia/hive/scripts/queue/pipeline_store.py` — PipelineStore ABC (from TASK-222)
- `.deia/hive/scripts/queue/filesystem_store.py` — reference implementation (from TASK-222)
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 6.3

## Deliverables
- [ ] Create `.deia/hive/scripts/queue/inmemory_store.py`
  - `InMemoryPipelineStore(PipelineStore)`
  - Stages as dict of lists: hold, queue, active, done, failed, needs_review, dead
  - `self.events = []` — append-only event list
  - `move_spec` pops from source list, appends metadata, pushes to dest list
  - `list_specs` returns copy of stage list
  - `get_done_ids` returns set of IDs from done list
  - `deps_satisfied` checks done list
  - `get_orphans` returns active list
  - `emit_event` appends to events list
  - `append_section` modifies spec content string in place
- [ ] Create tests in `.deia/hive/scripts/queue/tests/test_inmemory_store.py`
  - Mirror the filesystem store tests from TASK-222
  - Test all PipelineStore methods work with in-memory state
  - Test events are recorded correctly
  - ~10 tests minimum

## Priority
P1

## Model
haiku
