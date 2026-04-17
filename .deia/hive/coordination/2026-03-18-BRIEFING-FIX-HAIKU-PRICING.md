# Briefing: Fix Haiku Pricing Constant

## Objective
Fix the outdated Haiku pricing constant that causes `test_estimate_cost_haiku` to fail. Expected $0.0048, got $0.006.

## What's Broken
- Test: `tests/hivenode/test_claude_cli_token_tracking.py::TestCostCalculation::test_estimate_cost_haiku`
- Error: Haiku pricing mismatch — expected 0.0048, got 0.006
- Reference: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` section "Cost calculation (1)"

## What To Do
1. Find the Haiku pricing constant in the codebase (likely in a cost estimator or token tracking module)
2. Update it to match current Haiku 4.5 pricing
3. Run the failing test to confirm fix
4. Write a spec file and drop it in `.deia/hive/queue/` with priority P2, model haiku

## Model: haiku

## Response
Write response to: `.deia/hive/responses/20260318-FIX-HAIKU-PRICING.md`
