# SPEC-EXEC-03: Queue Runner Integration with DES Build Integrity Flow

## Role Override
bee

## Priority
P0

## Model Assignment
sonnet

## Depends On
SPEC-EXEC-01
SPEC-EXEC-02

## Intent
Wire the queue runner's spec_processor to load and execute the build-integrity PHASE-IR flow in production mode before dispatching bees. Specs must pass all 4 gates (Gate 0 + Phases 0/1/2) before a bee is dispatched. Failed specs go to `_needs_review/`.

## Files to Read First
- `.deia/hive/scripts/queue/spec_processor.py` — current spec processing logic
- `.deia/hive/scripts/queue/run_queue.py` — queue runner main loop
- `.deia/hive/scripts/queue/spec_parser.py` — spec file parser
- `engine/des/engine.py` — SimulationEngine class
- `engine/des/executors.py` — ExecutorRegistry (from EXEC-01)
- `engine/flows/build-integrity.phase` — the flow to execute (from EXEC-02)
- `hivenode/llm/router.py` — LLM routing (to create adapter for llm executor)

## Acceptance Criteria
- [ ] `spec_processor.py` modified to:
  - [ ] Load `engine/flows/build-integrity.phase` on first call (cached)
  - [ ] Create SimulationEngine in production mode
  - [ ] Create executor registry with:
    - [ ] Python executor wired to real Python execution
    - [ ] LLM executor wired to hivenode LLM router (or a lightweight adapter)
    - [ ] Human executor wired to `_needs_review/` file-based I/O
  - [ ] Inject spec content as token properties
  - [ ] Run the flow
  - [ ] If flow completes at `build_approved` sink → proceed with existing bee dispatch
  - [ ] If flow completes at escalation/rejected sink → move spec to `_needs_review/`
  - [ ] Gate/phase reports written to `.deia/hive/responses/` as PHASE0-REPORT.md, etc.
- [ ] New LLM adapter in `engine/des/llm_adapter.py`:
  - [ ] Thin wrapper that accepts model config from node and calls hivenode LLM router
  - [ ] Injected into executor registry via ctx
  - [ ] Handles token tracking (input/output tokens, cost)
- [ ] Fallback: if engine/flows/build-integrity.phase not found, fall back to existing behavior (direct dispatch without gates) with a warning log
- [ ] Tests in `tests/engine/des/test_queue_integration.py`:
  - [ ] Test spec_processor loads flow correctly
  - [ ] Test happy path: mock executors return passing results → bee dispatch called
  - [ ] Test gate failure: mock executor returns failing coverage → spec moved to `_needs_review/`
  - [ ] Test fallback: missing flow file → direct dispatch with warning
  - [ ] Test gate reports written to responses/

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- Do NOT break the existing queue runner. The fallback to direct dispatch must work if the flow file is missing.
- The LLM adapter must NOT import from engine into hivenode or vice versa at module level. Use dependency injection.
- Gate/phase reports follow the format from PROCESS-0013 (save to `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE{N}-REPORT.md`)
- Human escalation files go to `.deia/hive/queue/_needs_review/ESCALATION-{spec-id}.md`
- Cost tracking: each gate/phase LLM call tracked. Total cost logged in spec's final report.
- No file over 500 lines.
- TDD: tests first.

## Smoke Test
```bash
# Create a test spec
cat > /tmp/test-spec.md << 'EOF'
# SPEC-TEST-EXEC: Test the execution pipeline

## Priority
P2

## Model Assignment
haiku

## Intent
Verify that 2 + 2 = 4.

## Acceptance Criteria
- [ ] Assert 2 + 2 == 4

## Constraints
- This is a test spec
EOF

# Copy to backlog (queue runner picks it up)
cp /tmp/test-spec.md .deia/hive/queue/backlog/SPEC-TEST-EXEC-pipeline-test.md

# Watch for gate reports in responses/
ls -la .deia/hive/responses/ | grep PHASE
# Should see PHASE0-REPORT, PHASE1-REPORT, etc.
```
