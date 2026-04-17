# SPEC: Fix CLI Token & Cost Tracking

**Priority:** P0
**Layer:** infrastructure
**Estimate:** M

## Problem

The CLI subprocess adapter (`hivenode/adapters/cli/claude_cli_subprocess.py`) is not capturing token usage or cost data from Claude Code dispatches. Every dispatch for the past 5 days reports `Cost (USD): $0` and `input_tokens: 0, output_tokens: 0`.

Root cause: Lines 349-363 try to parse Claude Code's output as raw JSON, but the parsing either fails silently or the keys don't match what Claude Code actually returns via `--output-format json`.

Result: Zero visibility into actual API spend. The build monitor shows $0.49 total across 83+ specs, which is wrong.

## Requirements

1. **Investigate** what Claude Code actually returns with `--output-format json` — capture a real response and inspect the JSON structure
2. **Fix** `claude_cli_subprocess.py` to reliably extract `input_tokens` and `output_tokens` from Claude Code's JSON output
3. **Calculate cost** from tokens using model rate cards — do NOT rely on Claude Code returning cost. Cost = f(model, tokens_up, tokens_down)
4. **Rate card** must use the ACTUAL model dispatched (haiku/sonnet/opus), not a hardcoded default
5. **Heartbeat** the token counts and calculated cost via `send_heartbeat()` so the build monitor displays real numbers
6. **Carbon** estimate from tokens using the existing `estimate_carbon()` pattern in base adapter

## Files to Read First

- `hivenode/adapters/cli/claude_cli_subprocess.py` (lines 347-363 — JSON parsing)
- `hivenode/adapters/anthropic.py` (estimate_cost — has rate card pattern)
- `.deia/hive/scripts/dispatch/dispatch.py` (lines 345-387 — telemetry extraction)
- `hivenode/rag/indexer/models.py` (CCCMetadata — token_estimate, model_for_cost fields)

## Key Constraint

- `model_for_cost` must come from the actual dispatch, never hardcoded
- Claude Code returns tokens, we calculate cost — not the other way around

## Acceptance Criteria

- [ ] Token counts (input + output) captured from every CLI dispatch
- [ ] Cost calculated from tokens × model rate card
- [ ] Build monitor shows real token counts and costs
- [ ] Rate card covers haiku, sonnet, opus at minimum
- [ ] No hardcoded model assumptions
