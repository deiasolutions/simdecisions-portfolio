# TASK-227: LLM Triage Functions — 3 Integration Points (W3-B)

## Objective
Implement three LLM triage functions that add intelligence to the directory state machine: crash recovery triage, failure diagnosis, and completion validation.

## Context
Part of SPEC-PIPELINE-001 (Unified Build Pipeline). These functions use cheap Haiku calls to make smart routing decisions instead of blind retries. Each costs ~$0.01-0.03 per call.

## Depends On
- TASK-224 (directory state machine transitions must exist)

## Source Spec
`docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 5

## Files to Read First
- `docs/specs/SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md` — Section 5 (LLM Triage Layer)
- `.deia/hive/scripts/queue/run_queue.py` — where triage gets called
- `.deia/hive/scripts/queue/dispatch_handler.py` — bee dispatch/completion handling

## Deliverables
- [ ] Create `.deia/hive/scripts/queue/triage.py`
  - `triage_crash_recovery(spec, diff, tests) -> CrashVerdict`
    - Verdicts: COMPLETE_ENOUGH, PARTIAL_SAFE, REVERT
    - Input: spec content, git diff since session start, test output
    - Dispatches Haiku call with structured prompt
  - `triage_failure(spec, response, errors) -> FailureClassification`
    - Classifications: AMBIGUOUS_SPEC, CODING_ERROR, DEPENDENCY_ISSUE, ENVIRONMENT_ISSUE
    - Routes: ambiguous → _needs_review/, coding → generate fix spec, dependency → block, environment → _needs_review/
  - `validate_completion(spec, diff, tests) -> CompletionReview`
    - Phase 1: advisory only — log the review, don't gate on it
    - Flags missing acceptance criteria or suspicious changes
    - Holdout principle: reviewing LLM is NEVER the same model/session that did the work
- [ ] Wire triage functions into state machine transitions:
  - `triage_crash_recovery` called during orphan scan (from TASK-224)
  - `triage_failure` called when bee returns error/timeout
  - `validate_completion` called before moving to _done/ (advisory)
- [ ] Create tests in `.deia/hive/scripts/queue/tests/test_triage.py`
  - Test each triage function returns correct verdict type
  - Test routing logic for each verdict
  - Mock LLM calls (do not make real API calls in tests)
  - ~10 tests minimum

## Priority
P1

## Model
sonnet
