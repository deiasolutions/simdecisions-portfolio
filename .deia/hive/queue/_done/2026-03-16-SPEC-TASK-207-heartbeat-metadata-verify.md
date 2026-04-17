# TASK-207: Heartbeat Metadata Verification + Build Monitor Display

## Objective
Verify that heartbeats include model + tokens after CLI token capture fix, and confirm build monitor displays real cumulative cost.

## Context
**Current state:**
- HeartbeatPayload (build_monitor.py lines 37-47) already has fields: model, input_tokens, output_tokens, cost_usd
- BuildState (lines 63-108) already tracks total_cost, total_input_tokens, total_output_tokens
- BUT: heartbeats show 0 for all tokens because CLI adapter returns 0 (fixed by TASK-204)

**After TASK-204 completes:**
- ProcessResult.usage contains non-zero tokens
- Heartbeat callback should receive usage data
- Build monitor should display real cumulative cost

**This task:**
1. Verify heartbeat callback receives usage data from ProcessResult
2. Update dispatch script to send heartbeat with tokens/cost after dispatch completes
3. Verify build monitor /status endpoint returns non-zero total_cost
4. Add test to confirm heartbeat metadata includes model + tokens

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (lines 37-108, HeartbeatPayload, BuildState)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (heartbeat callback usage)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (heartbeat_callback calls)

## Deliverables

### 1. Verify Heartbeat Callback Receives Usage Data
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py`

**Check:**
- After ProcessResult is created (line ~458), if heartbeat_callback exists, it should be called with usage data
- Currently heartbeat_callback is called in send_task() at various points (e.g., "running", "complete")
- Ensure "complete" heartbeat includes: model, input_tokens, output_tokens, cost_usd

**Implementation:**
```python
# After ProcessResult is created
if self.heartbeat_callback and usage:
    self.heartbeat_callback(
        status="complete",
        message="Dispatch complete",
        model=usage.get("model"),
        input_tokens=usage.get("input_tokens"),
        output_tokens=usage.get("output_tokens"),
        cost_usd=usage.get("cost_usd"),
    )
```

### 2. Update Dispatch Script Heartbeat Handling
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py`

**Check:**
- Heartbeat callback function (if exists) should forward model + tokens to build monitor
- If no heartbeat callback exists, add one that sends POST to /build-monitor/heartbeat

**Implementation:**
```python
def send_heartbeat(status, message, model=None, input_tokens=None, output_tokens=None, cost_usd=None):
    payload = {
        "task_id": task_id,
        "status": status,
        "message": message,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd,
        "role": "B",  # Bee dispatch
    }
    try:
        httpx.post(f"{BUILD_MONITOR_URL}/build-monitor/heartbeat", json=payload, timeout=5)
    except Exception:
        pass  # Don't crash dispatch on heartbeat failure

process = ClaudeCodeProcess(
    work_dir=repo_root,
    ...
    heartbeat_callback=send_heartbeat,  # Pass callback
)
```

### 3. Verify Build Monitor /status Endpoint
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py`

**Check:** Lines 88-90 already load total_cost, total_input_tokens, total_output_tokens from state
**No changes needed** — just verify endpoint returns non-zero values after heartbeat with tokens

### 4. Add CCCMetadata.model_for_cost Population
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py`

**Check:** CCCMetadata (lines 46-54) has model_for_cost field
**Ensure:** When CCCMetadata is created (e.g., in RAG indexer or terminal chat), model_for_cost is populated from actual model ID (not empty string)

**Example fix in hivenode/llm/router.py or terminal route:**
```python
ccc = CCCMetadata(
    clock_ms=duration_ms,
    coin_usd=cost_usd,
    carbon_kg=carbon_kg,
    token_estimate=input_tokens + output_tokens,
    model_for_cost=model,  # MUST be actual model ID, not ""
)
```

## Test Requirements

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_heartbeat_metadata.py`

Minimum 3 tests (TDD — write tests first):

1. `test_heartbeat_includes_tokens()` — Mock dispatch completion heartbeat, verify HeartbeatPayload includes model, input_tokens, output_tokens, cost_usd
2. `test_build_monitor_accumulates_cost()` — Send 2 heartbeats with cost_usd=1.0 each, verify /status returns total_cost=2.0
3. `test_heartbeat_zero_tokens_handled()` — Heartbeat with 0 tokens should not crash, total_cost remains 0

**Integration test:**
4. `test_e2e_dispatch_heartbeat_cost()` — Run real dispatch, query build monitor /status, verify total_cost > 0 and total_input_tokens > 0

## Constraints
- No file over 500 lines
- No stubs — all functions fully implemented
- Heartbeat callback must not crash dispatch on failure (try/except)
- If tokens are 0, cost_usd should be 0.0 (not None)
- CCCMetadata.model_for_cost MUST be populated (not empty string)

## Acceptance Criteria
- [ ] Heartbeat callback in ClaudeCodeProcess calls with model, input_tokens, output_tokens, cost_usd
- [ ] Dispatch script heartbeat callback forwards tokens to build monitor
- [ ] Build monitor /status endpoint returns non-zero total_cost after dispatch
- [ ] CCCMetadata.model_for_cost populated with actual model ID (not empty)
- [ ] 3+ tests pass
- [ ] Integration test confirms real dispatch results in non-zero total_cost

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-207-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
