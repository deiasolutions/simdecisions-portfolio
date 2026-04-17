# BRIEFING: Fix CLI Token & Cost Tracking

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1430-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Priority:** P0

---

## Objective

Fix the CLI subprocess adapter to accurately capture token usage and cost data from Claude Code dispatches. Currently, every dispatch reports $0 cost and 0 tokens, which blocks visibility into actual API spend.

---

## Context from Q88N

The CLI subprocess adapter (`hivenode/adapters/cli/claude_cli_subprocess.py`) tries to parse Claude Code's `--output-format json` output but the parsing either fails silently or the keys don't match. Result: zero visibility into actual API spend for the past 5 days. The build monitor shows $0.49 total across 83+ specs, which is incorrect.

Root cause is lines 349-363 in `claude_cli_subprocess.py`.

---

## Requirements (from spec)

1. **Investigate** what Claude Code actually returns with `--output-format json` — capture a real response and inspect the JSON structure
2. **Fix** `claude_cli_subprocess.py` to reliably extract `input_tokens` and `output_tokens` from Claude Code's JSON output
3. **Calculate cost** from tokens using model rate cards — do NOT rely on Claude Code returning cost. Cost = f(model, tokens_up, tokens_down)
4. **Rate card** must use the ACTUAL model dispatched (haiku/sonnet/opus), not a hardcoded default
5. **Heartbeat** the token counts and calculated cost via `send_heartbeat()` so the build monitor displays real numbers
6. **Carbon** estimate from tokens using the existing `estimate_carbon()` pattern in base adapter

---

## Files to Review Before Writing Tasks

- `hivenode/adapters/cli/claude_cli_subprocess.py` (lines 347-363 — JSON parsing)
- `hivenode/adapters/anthropic.py` (estimate_cost — has rate card pattern)
- `.deia/hive/scripts/dispatch/dispatch.py` (lines 345-387 — telemetry extraction)
- `hivenode/rag/indexer/models.py` (CCCMetadata — token_estimate, model_for_cost fields)

---

## Key Constraints

- `model_for_cost` must come from the actual dispatch, never hardcoded
- Claude Code returns tokens, we calculate cost — not the other way around
- NO HARDCODED COLORS (Rule 3 — does not apply to backend code)
- No file over 500 lines (Rule 4)
- TDD: tests first (Rule 5)
- NO STUBS (Rule 6)

---

## Acceptance Criteria (copy to task files)

- [ ] Token counts (input + output) captured from every CLI dispatch
- [ ] Cost calculated from tokens × model rate card
- [ ] Build monitor shows real token counts and costs
- [ ] Rate card covers haiku, sonnet, opus at minimum
- [ ] No hardcoded model assumptions

---

## Suggested Model Assignment

**Sonnet** — requires investigation of Claude Code JSON output structure + implementation + test coverage.

---

## Next Steps

1. Read the four files listed above
2. Write task file(s) for a bee (or Q33N if explicitly approved by Q88N for this task)
3. Return task files to me (Q33NR) for review
4. After I approve, dispatch the bee(s)
5. Report results

---

**Q33NR awaiting your task files.**
