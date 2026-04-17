# TASK-226 (STAGING): PHASE-IR Flow Encoding of Build Pipeline

## Status: STAGING — waiting for dependency verification

## Original Spec
Copied from `_done/2026-03-16-SPEC-TASK-226-phase-ir-pipeline-flow.md`

## Objective
Author the `.ir.json` that describes the full build pipeline as a PHASE-IR flow.

## Depends On
- TASK-224 (directory state machine)
- TASK-225 (InMemoryPipelineStore) — verified PRESENT

## Why Staged
TASK-226 depends on TASK-224 which is NOT yet verified. Also the pipeline IR and DES runner are lower priority than UI bugs. Stage until canvas and explorer bugs are cleared.

## Files
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`
- `engine/phase_ir/`
- `engine/phase_ir/schema.json`

## Model Assignment
sonnet

## Priority
P1
