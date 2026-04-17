# Q33N Coordination Report: Cost Storage Format + Model Rate Lookup Table

**Date:** 2026-03-16
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Re:** BRIEFING-cost-storage-rate-lookup

---

## Summary

Briefing analyzed. Task files written. Ready for Q33NR review before dispatch.

**Briefing scope:**
- Three-currency cost storage (CLOCK, COIN, CARBON) for Event Ledger
- Centralized YAML config for model rates (eliminate hardcoded duplication)
- Fix CLI token capture bug (currently returns 0 tokens)
- Auto-attach cost to Event Ledger for every CLI dispatch
- Heartbeat metadata population for build monitor display

**Task breakdown:** 5 tasks, sequential dependencies

---

## Task Files Created

### TASK-191: Model Rate YAML Config + Loader Module
**Path:** `.deia/hive/tasks/2026-03-16-TASK-191-model-rate-yaml-config.md`
**Model:** Haiku
**Estimated complexity:** Small (~60 min)

**Deliverables:**
- `hivenode/config/model_rates.yml` (5 models + default + carbon rate)
- `hivenode/config/rate_loader.py` (4 functions: load_model_rates, get_rate, compute_coin, compute_carbon)
- `hivenode/config/__init__.py` (exports)
- 8 tests (rate lookup, cost computation, carbon estimation)

**Why Haiku:** Pure data structure + simple functions. No complex logic.

**Dependencies:** None (foundation task)

---

### TASK-192: Fix CLI Token Capture from JSON Output
**Path:** `.deia/hive/tasks/2026-03-16-TASK-192-cli-token-capture-fix.md`
**Model:** Sonnet
**Estimated complexity:** Medium (~90 min)

**Deliverables:**
- Add debug logging to `claude_cli_subprocess.py` (4 locations)
- Verify ProcessResult.usage is passed correctly
- Migrate _estimate_cost() to use rate_loader.compute_coin()
- Migrate _estimate_carbon() to use rate_loader.compute_carbon()
- Remove hardcoded PRICING constant
- 5 tests (JSON parsing, token extraction, usage dict validation)

**Why Sonnet:** Debugging existing code + migration logic requires deeper analysis.

**Dependencies:** TASK-191 (needs rate_loader module)

---

### TASK-193: Migrate hivenode/llm/cost.py to Use rate_loader
**Path:** `.deia/hive/tasks/2026-03-16-TASK-193-migrate-llm-cost-rate-loader.md`
**Model:** Haiku
**Estimated complexity:** Small (~45 min)

**Deliverables:**
- Remove COST_PER_TOKEN constant
- Update calculate_cost() to use rate_loader.compute_coin()
- Update calculate_carbon() to use rate_loader.compute_carbon()
- Preserve emit_llm_event() interface (no breaking changes)
- 5 tests (cost computation, carbon estimation, consistency with rate_loader)

**Why Haiku:** Simple function replacement. No complex logic.

**Dependencies:** TASK-191 (needs rate_loader module)

---

### TASK-194: Event Ledger Auto-Attach for CLI Dispatches
**Path:** `.deia/hive/tasks/2026-03-16-TASK-194-event-ledger-auto-attach.md`
**Model:** Sonnet
**Estimated complexity:** Medium (~90 min)

**Deliverables:**
- Add ledger_writer parameter to ClaudeCodeProcess.__init__()
- Auto-write Event Ledger entry after ProcessResult creation
- Update dispatch.py to create LedgerWriter and pass to ClaudeCodeProcess
- Close ledger_writer in finally block
- 4 tests (ledger entry creation, cost fields, payload_json, no-crash on None)
- 1 integration test (e2e dispatch writes ledger)

**Why Sonnet:** Integrates multiple subsystems (CLI adapter, dispatch script, Event Ledger). Requires careful error handling.

**Dependencies:** TASK-192 (needs working token capture for usage data)

---

### TASK-195: Heartbeat Metadata Verification + Build Monitor Display
**Path:** `.deia/hive/tasks/2026-03-16-TASK-195-heartbeat-metadata-verify.md`
**Model:** Haiku
**Estimated complexity:** Small (~60 min)

**Deliverables:**
- Verify heartbeat callback receives usage data from ProcessResult
- Update dispatch script to send heartbeat with tokens/cost
- Verify build monitor /status returns non-zero total_cost
- Ensure CCCMetadata.model_for_cost is populated (not empty)
- 3 tests (heartbeat metadata, cost accumulation, zero tokens handling)
- 1 integration test (e2e dispatch → build monitor shows cost)

**Why Haiku:** Mostly verification + small fixes. No complex implementation.

**Dependencies:** TASK-192 (needs working token capture), TASK-194 (needs ledger auto-attach)

---

## Dependency Graph

```
TASK-191 (rate_loader YAML + module)
  ├─→ TASK-192 (CLI token capture fix)
  │     ├─→ TASK-194 (Event Ledger auto-attach)
  │     └─→ TASK-195 (heartbeat metadata verify)
  └─→ TASK-193 (migrate llm/cost.py)
```

**Sequential dispatch order:**
1. TASK-191 (foundation)
2. TASK-192 + TASK-193 (parallel, both depend on 191)
3. TASK-194 (depends on 192)
4. TASK-195 (depends on 192, 194)

---

## Test Coverage

**Total minimum tests:** 25 (8 + 5 + 5 + 4 + 3)

**Test distribution:**
- Unit tests: 21 (rate_loader: 8, CLI token capture: 5, llm/cost migration: 5, ledger auto-attach: 3)
- Integration tests: 4 (ledger auto-attach: 2, heartbeat verify: 2)

**Critical integration tests:**
- `test_e2e_dispatch_ledger_auto_attach()` — Verify Event Ledger contains entry after real dispatch
- `test_e2e_dispatch_heartbeat_cost()` — Verify build monitor shows non-zero cost after real dispatch

---

## File Impact

**Files created:**
- `hivenode/config/model_rates.yml`
- `hivenode/config/rate_loader.py`
- `hivenode/config/__init__.py`
- `tests/hivenode/config/test_rate_loader.py`
- `tests/hivenode/adapters/cli/test_token_capture.py`
- `tests/hivenode/llm/test_cost_migration.py`
- `tests/hivenode/adapters/cli/test_ledger_auto_attach.py`
- `tests/hivenode/routes/test_heartbeat_metadata.py`

**Files modified:**
- `hivenode/adapters/cli/claude_cli_subprocess.py` (TASK-192, TASK-194)
- `hivenode/llm/cost.py` (TASK-193)
- `.deia/hive/scripts/dispatch/dispatch.py` (TASK-194, TASK-195)
- `hivenode/rag/indexer/models.py` (TASK-195, CCCMetadata.model_for_cost fix)

**Files deleted:**
- None

**Constants removed:**
- `PRICING` dict in `claude_cli_subprocess.py` (lines 49-56)
- `COST_PER_TOKEN` dict in `llm/cost.py` (lines 10-14)
- `DEFAULT_COST` in `llm/cost.py` (lines 16-17)
- `CARBON_PER_TOKEN` in `llm/cost.py` (lines 19-20)

---

## Critical Issues Identified

### 1. CLI Token Capture Bug (TASK-192)
**Current state:** Lines 366-421 in claude_cli_subprocess.py parse JSON, but ProcessResult.usage shows 0 tokens

**Root cause hypothesis:**
- JSON parsing may fail silently (try/except swallows errors)
- Extracted tokens are 0 because JSON structure doesn't match expectations
- usage dict is created but not passed to ProcessResult (line ~458)

**Fix:** Add debug logging at 4 checkpoints to identify where tokens are lost

### 2. Hardcoded Rates Duplication
**Current state:** PRICING dict (claude_cli_subprocess.py) and COST_PER_TOKEN dict (llm/cost.py) have same data but different formats

**Problem:** Drift risk — if rates change, must update 2 places

**Fix:** YAML config as single source of truth, both modules use rate_loader

### 3. CCCMetadata.model_for_cost Often Empty
**Current state:** CCCMetadata.model_for_cost is "" in many places (e.g., terminal chat, RAG indexer)

**Problem:** Can't compute accurate cost without model ID

**Fix:** TASK-195 ensures model_for_cost is populated from actual dispatch model ID

---

## Smoke Test Plan

After all tasks complete:

1. **Start hivenode:**
   ```bash
   python -m hivenode.main
   ```

2. **Dispatch a bee via CLI:**
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/TEST-TASK.md --model sonnet --role bee --inject-boot
   ```

3. **Check Event Ledger:**
   ```sql
   SELECT event_type, cost_usd, cost_carbon, cost_tokens_up, cost_tokens_down
   FROM events
   WHERE event_type='CLI_DISPATCH'
   ORDER BY id DESC LIMIT 1;
   ```
   **Expected:** cost_usd > 0, cost_carbon > 0, cost_tokens_up > 0, cost_tokens_down > 0

4. **Check build monitor:**
   ```bash
   curl http://localhost:8000/build-monitor/status
   ```
   **Expected:** `"total_cost": 0.085` (not 0.00), `"total_input_tokens": 12450` (not 0)

5. **Check heartbeat log:**
   Review build monitor log for heartbeat entries
   **Expected:** `model: "claude-sonnet-4-5-20250929"`, `input_tokens: 12450`, `output_tokens: 3200`

---

## Acceptance Criteria (All Tasks Combined)

- [ ] YAML config created at `hivenode/config/model_rates.yml` (5 models + default + carbon)
- [ ] rate_loader module implements 4 functions (no stubs)
- [ ] CLI token capture extracts non-zero tokens from JSON output
- [ ] Debug logging added to identify token extraction failures
- [ ] PRICING constant removed from claude_cli_subprocess.py
- [ ] COST_PER_TOKEN constant removed from llm/cost.py
- [ ] Event Ledger auto-attach writes CLI_DISPATCH entry with cost fields
- [ ] Dispatch script creates LedgerWriter and passes to ClaudeCodeProcess
- [ ] Heartbeat callback sends model + tokens to build monitor
- [ ] Build monitor /status returns non-zero total_cost after dispatch
- [ ] CCCMetadata.model_for_cost populated with actual model ID
- [ ] 25+ tests pass across 5 test files
- [ ] Smoke test confirms Event Ledger + build monitor show real costs

---

## Recommendations for Q33NR

### Dispatch Order
**Sequential with dependencies:**
1. Dispatch TASK-191 (Haiku)
2. Wait for 191 completion, then dispatch TASK-192 (Sonnet) + TASK-193 (Haiku) in parallel
3. Wait for 192 completion, then dispatch TASK-194 (Sonnet)
4. Wait for 194 completion, then dispatch TASK-195 (Haiku)

**Total estimated time:** ~5.5 hours (191: 1h, 192: 1.5h, 193: 0.75h, 194: 1.5h, 195: 1h)

### Risk Mitigation
- **TASK-192 is CRITICAL** — if token capture remains broken, all downstream tasks fail
- Add smoke test after TASK-192 to verify tokens are non-zero before proceeding
- If TASK-192 uncovers deeper JSON parsing issues, may need emergency fix task

### Post-Completion Verification
- Run full hivenode test suite: `cd hivenode && python -m pytest tests/ -v`
- Run dispatch integration test with real bee
- Query Event Ledger to confirm CLI_DISPATCH entries exist
- Check build monitor UI to confirm cost display

---

## Q33N Status

**Task files:** 5 written, ready for review
**Dependencies:** Mapped, sequential dispatch order defined
**Tests:** 25 minimum across 5 test files
**Acceptance criteria:** 13 checkboxes defined
**Smoke test:** 5-step plan ready

**Awaiting Q33NR review before dispatch.**

---

## Files Attached

1. `.deia/hive/tasks/2026-03-16-TASK-191-model-rate-yaml-config.md`
2. `.deia/hive/tasks/2026-03-16-TASK-192-cli-token-capture-fix.md`
3. `.deia/hive/tasks/2026-03-16-TASK-193-migrate-llm-cost-rate-loader.md`
4. `.deia/hive/tasks/2026-03-16-TASK-194-event-ledger-auto-attach.md`
5. `.deia/hive/tasks/2026-03-16-TASK-195-heartbeat-metadata-verify.md`

**Next step:** Q33NR reviews task files, requests corrections if needed, or approves dispatch.
