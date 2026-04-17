# Briefing: Audit SPEC-PIPELINE-001 — What Was Built vs What Was Planned

## Objective
Audit SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md (in `docs/specs/`) to determine what was actually implemented vs what remains unbuilt. Also check if any unbuilt items were incorrectly marked as complete in the feature inventory.

## What To Do

### 1. Read the spec
Read `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` in full.

### 2. Check each planned feature against the codebase

**Wave 1:**
- W1-A: PipelineStore protocol (ABC) + FilesystemPipelineStore — search for `class PipelineStore`, `class FilesystemPipelineStore`
- W1-B: Validation ledger events — search for `emit_event`, `EventLedger`, `phase_validation`, `bee_execution` event schema

**Wave 2:**
- W2-A: Directory state machine transitions — does `run_queue.py` use `_active/` directory? Append manifests? Completion records? Failure logs? Crash recovery (scan `_active/` on startup for orphans)?
- W2-B: InMemoryPipelineStore — search for `class InMemoryPipelineStore`

**Wave 3:**
- W3-A: PHASE-IR flow encoding of the build pipeline as IR JSON
- W3-B: LLM triage functions — search for `triage_crash_recovery`, `triage_failure`, `validate_completion`

**Wave 4:**
- W4-A: DES runner for build pipeline — search for `/api/pipeline/simulate`

**Other features:**
- Fidelity gates (Gate 0, Phase 0, Phase 1, Phase 2) — are any wired?
- Queue directories: `_hold/`, `_active/`, `_done/`, `_failed/`, `_needs_review/`, `_dead/` — which exist as folders? Which does `run_queue.py` actually USE in code (file moves, routing logic)?
- Manifest appending on dispatch
- Completion Record appending on finish
- Failure Log appending on failure

### 3. Check feature inventory
Run `python _tools/inventory.py backlog list` and `python _tools/inventory.py feat list` to see if any pipeline items were marked as built or complete.

### 4. Write audit report

For each feature, classify as:
- **BUILT**: fully implemented and working
- **PARTIAL**: folder/stub exists but not fully wired
- **NOT BUILT**: doesn't exist at all
- **CLAIMED BUT NOT BUILT**: marked complete in inventory but not actually implemented

## Files to Read First
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`
- `.deia/hive/scripts/queue/run_queue.py`
- `.deia/hive/scripts/queue/spec_processor.py`

## Model: sonnet

## Response
Write response to: `.deia/hive/responses/20260318-PIPELINE-001-AUDIT.md`
