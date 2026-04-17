# TASK-224: Directory State Machine Transitions (W2-A)

## Objective
Implement the full directory state machine: `_active/` pickup with manifest, `_done/`/`_failed/` routing, crash recovery (orphan scan on startup), failure log appending, completion record appending. All through `PipelineStore` interface.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). This task implements Sections 4.2–4.7 of the spec. The queue runner currently moves specs directly between `queue/` and `_done/`. This task adds the intermediate states (`_active/`, `_failed/`, `_needs_review/`) and the manifest/completion record pattern.

## Depends On
- TASK-222 (PipelineStore protocol must exist)

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Sections 4.2 through 4.7

## Files to Read First
- `.deia/hive/scripts/queue/pipeline_store.py` — PipelineStore ABC (from TASK-222)
- `.deia/hive/scripts/queue/filesystem_store.py` — FilesystemPipelineStore (from TASK-222)
- `.deia/hive/scripts/queue/run_queue.py` — refactored queue runner (from TASK-222)
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 4

## Deliverables
- [ ] Create `_active/`, `_failed/`, `_needs_review/`, `_dead/` directories if they don't exist
- [ ] Implement pickup logic in `run_queue.py`:
  - Move spec from `queue/` to `_active/` via PipelineStore
  - Append `## Execution Manifest` section (bee_id, model, session_id, started_at, pid)
- [ ] Implement completion routing:
  - CLEAN result → append `## Completion Record`, move to `_done/`
  - Error/timeout → append `## Failure Log` entry, move to `_failed/`
  - Regression detected → move to `_needs_review/`
- [ ] Implement crash recovery on startup:
  - Scan `_active/` for orphans via `get_orphans()`
  - If retries remain → move back to `queue/`
  - If max retries exhausted → move to `_needs_review/`
- [ ] Create tests in `.deia/hive/scripts/queue/tests/test_state_machine.py`
  - Test pickup moves to _active/ with manifest
  - Test clean completion moves to _done/ with record
  - Test failure moves to _failed/ with log
  - Test crash recovery moves orphans back to queue
  - Test crash recovery escalates after max retries
  - ~15 tests minimum

## Priority
P1

## Model
sonnet
