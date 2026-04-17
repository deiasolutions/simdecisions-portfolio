---
id: EXEC-03
priority: P0
model: sonnet
role: bee
depends_on:
  - EXEC-01
  - EXEC-02
---
# SPEC-EXEC-03: Queue Runner Integration with DES Build Integrity Flow

## Intent
Wire the queue runner's spec_processor to load and execute the build-integrity PRISM-IR flow in production mode before dispatching bees. Specs must pass all 4 gates (Gate 0 + Phases 0/1/2) before a bee is dispatched. Failed specs go to `_needs_review/`.

## Files to Read First
- `.deia/hive/scripts/queue/spec_processor.py` — current spec processing logic
- `.deia/hive/scripts/queue/run_queue.py` — queue runner main loop
- `.deia/hive/scripts/queue/spec_parser.py` — spec file parser
- `engine/des/engine.py` — SimulationEngine class
- `engine/des/executors.py` — ExecutorRegistry (from EXEC-01)
- `engine/des/adapters.py` — LLMAdapter, DeciderRouter (from EXEC-01)
- `.wiki/processes/build-integrity.prism.md` — the flow to execute (from EXEC-02)
- `hivenode/llm/router.py` — LLM routing (to create adapter for LLM executor)

## Acceptance Criteria
- [ ] `spec_processor.py` modified to:
  - [ ] Load `.wiki/processes/build-integrity.prism.md` on first call (cached)
  - [ ] Create SimulationEngine in production mode
  - [ ] Create executor registry with:
    - [ ] Python executor wired to real Python execution (via allowlist)
    - [ ] LLM executor wired to hivenode LLM router via `HivenodeLLMAdapter`
    - [ ] Decision executor wired to `DeciderRouter` with `FileChannel` default
  - [ ] Inject spec content as token properties:
    ```python
    token.properties = {
        # Raw text
        "spec_raw": full_markdown_text,
        "spec_path": "backlog/SPEC-FOO.md",
        
        # Parsed fields
        "spec_id": "SPEC-FOO",
        "intent": "...",
        "acceptance_criteria": [...],
        "constraints": [...],
        "files_to_read": [...],
        "priority": "P0",
        "model_assignment": "sonnet"
    }
    ```
  - [ ] Run the flow
  - [ ] If flow completes at `build_approved` end node → proceed with existing bee dispatch
  - [ ] If flow completes at escalation/rejected end node → move spec to `_needs_review/`
  - [ ] Gate/phase reports written to `.deia/hive/responses/` per PROCESS-0013 format
- [ ] New LLM adapter in `hivenode/llm/des_adapter.py`:
  - [ ] `HivenodeLLMAdapter` implements `LLMAdapter` protocol from EXEC-01
  - [ ] Wraps hivenode LLM router
  - [ ] Returns `LLMResponse` with token counts and cost
  - [ ] Injected into executor registry via ctx (not imported at module level)
- [ ] Configuration flag `REQUIRE_BUILD_INTEGRITY_FLOW`:
  - [ ] Default: `True` (hard error if flow file missing)
  - [ ] If `False` and flow missing: fall back to direct dispatch with warning log
  - [ ] Configurable via environment variable
- [ ] Tests in `tests/engine/des/test_queue_integration.py`:
  - [ ] Test spec_processor loads flow correctly
  - [ ] Test token properties include both raw and parsed fields
  - [ ] Test happy path: mock executors return passing results → bee dispatch called
  - [ ] Test gate failure: mock executor returns failing coverage → spec moved to `_needs_review/`
  - [ ] Test `REQUIRE_BUILD_INTEGRITY_FLOW=True`: missing flow → error (no dispatch)
  - [ ] Test `REQUIRE_BUILD_INTEGRITY_FLOW=False`: missing flow → warning + direct dispatch
  - [ ] Test gate reports written to responses/ in PROCESS-0013 format

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- **Default behavior:** `REQUIRE_BUILD_INTEGRITY_FLOW=True` — missing flow file is a hard error after EXEC-02 ships.
- The LLM adapter lives in `hivenode/llm/des_adapter.py`, NOT in `engine/`. It imports the protocol from engine but implements in hivenode.
- Gate/phase reports follow PROCESS-0013 format exactly (save to `.deia/hive/responses/YYYY-MM-DD-HHMM-{AGENT}-{TASK}-PHASE{N}-REPORT.md`)
- Decision escalation files go to `.deia/hive/queue/_needs_review/ESCALATION-{spec-id}.md`
- Cost tracking: each gate/phase LLM call tracked by model. Total cost logged in spec's final report per PROCESS-0013 token tracking format.
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
# Should see GATE0-REPORT, PHASE0-REPORT, PHASE1-REPORT, PHASE2-REPORT
```
