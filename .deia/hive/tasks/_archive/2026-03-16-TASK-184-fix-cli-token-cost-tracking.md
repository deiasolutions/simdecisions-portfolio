# TASK-184: Fix CLI Token & Cost Tracking

## Objective

Fix `claude_cli_subprocess.py` to capture token usage from Claude Code's JSON output, calculate cost using model-specific rate cards, and populate telemetry so the build monitor shows accurate API spend.

## Context

Currently, every Claude Code dispatch reports `$0 cost` and `0 tokens` because the JSON parsing at lines 347-363 in `claude_cli_subprocess.py` doesn't correctly extract token data from Claude Code's `--output-format json` output. The code tries to read keys like `cost_usd` and `total_cost_usd`, but we need to:

1. Determine what Claude Code actually returns in its JSON output
2. Extract `input_tokens` and `output_tokens` from that structure
3. Calculate cost ourselves using the rate card pattern from `anthropic.py`
4. Pass this data via the `usage` dict in `ProcessResult` so it flows to `dispatch.py`

The `model` is already passed to `ClaudeCodeProcess.__init__()` and stored as `self.model`, so we can use it for rate card lookups.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (lines 90-170, 347-411 — init + JSON parsing)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\anthropic.py` (lines 13-78 — PRICING rate card + estimate_cost)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\base.py` (lines 49-65 — estimate_carbon pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (lines 345-387 — how usage dict is consumed)

## Deliverables

### Phase 1: Investigation (REQUIRED FIRST)
- [ ] Run a test dispatch with `claude code --output-format json` and capture the raw JSON output
- [ ] Document the actual JSON structure returned by Claude Code (what keys exist, where tokens are)
- [ ] Verify whether Claude Code returns token counts at all with `--output-format json`

### Phase 2: Implementation
- [ ] Update JSON parsing in `send_task()` to extract `input_tokens` and `output_tokens` from the correct keys in Claude Code's response
- [ ] Add a rate card (PRICING dict) to `ClaudeCodeProcess` matching the pattern in `anthropic.py` with rates for:
  - `claude-opus-4-6`
  - `claude-sonnet-4-5-20250929`
  - `claude-haiku-4-5-20251001`
  - `default` fallback
- [ ] Implement `_estimate_cost(input_tokens: int, output_tokens: int) -> float` method in `ClaudeCodeProcess` using the rate card and `self.model`
- [ ] Implement `_estimate_carbon(input_tokens: int, output_tokens: int) -> float` method using the base adapter pattern (5g CO2 per 1000 tokens)
- [ ] Populate the `usage` dict in `ProcessResult` with:
  - `input_tokens`: int
  - `output_tokens`: int
  - `cost_usd`: float (calculated)
  - `carbon_kg`: float (calculated, in kg not grams)
  - `model`: str (the actual model used)
- [ ] If Claude Code doesn't return token counts in JSON, log a warning and set tokens to 0 (do NOT fail)

### Phase 3: Tests
- [ ] Write test file: `tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py`
- [ ] Test: Mock Claude Code JSON response with token counts → verify cost calculation
- [ ] Test: Mock response with haiku model → verify haiku rate card used
- [ ] Test: Mock response with sonnet model → verify sonnet rate card used
- [ ] Test: Mock response with opus model → verify opus rate card used
- [ ] Test: Mock response with unknown model → verify default rate card used
- [ ] Test: Mock response with no tokens → verify graceful fallback (0 tokens, $0 cost)
- [ ] Test: Verify carbon calculation (1000 input + 1000 output = ~10g CO2 = 0.01 kg)
- [ ] All tests must pass

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass: `cd hivenode && python -m pytest tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py -v`
- [ ] Minimum 8 tests (as listed in deliverables)
- [ ] Edge cases covered: missing tokens, unknown model, malformed JSON

## Constraints

- No file over 500 lines (current file is ~500, may need to modularize if we exceed)
- No hardcoded model — always use `self.model`
- No stubs — full implementation required
- If Claude Code doesn't return tokens, gracefully default to 0 (don't crash)
- Use the exact rate card values from `anthropic.py` for consistency

## Acceptance Criteria

- [ ] Token counts (input + output) captured from every CLI dispatch
- [ ] Cost calculated from tokens × model rate card (NOT from Claude Code's cost field)
- [ ] Carbon calculated from tokens using base adapter pattern
- [ ] `usage` dict contains: `input_tokens`, `output_tokens`, `cost_usd`, `carbon_kg`, `model`
- [ ] Rate card covers haiku, sonnet, opus at minimum + default fallback
- [ ] No hardcoded model assumptions — uses `self.model`
- [ ] Tests pass with 100% coverage of new code paths
- [ ] Graceful fallback if Claude Code JSON doesn't contain tokens

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-184-RESPONSE.md`

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

## Notes

- The investigation phase (Phase 1) is CRITICAL. Do not guess the JSON structure — run a real test and document what you find.
- If Claude Code doesn't return tokens via `--output-format json`, document this clearly and we'll need to parse from text output instead.
- The `model` parameter passed to `ClaudeCodeProcess.__init__()` is a short name like "sonnet", "haiku", "opus" — you may need to map these to full model IDs for the rate card lookup.
