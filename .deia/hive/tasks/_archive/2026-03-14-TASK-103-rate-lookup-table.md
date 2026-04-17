# TASK-085: Cost Storage Format + Model Rate Lookup Table

## Objective
Create a model rate lookup table in SQLite, add columns to events table for per-million-token costs and model metadata, implement cost computation function, and create GET /ledger/cost endpoint for aggregated cost reporting.

## Context
Current implementation stores total cost_usd but doesn't track:
- Which model was used for each event
- Per-million-token rates at event time
- When rates were last updated

This task adds:
1. New table: `model_rates` (model_name, cost_per_mtok_input, cost_per_mtok_output, rate_effective_date)
2. New columns in `events`: cost_per_mtok_input, cost_per_mtok_output, model_name, rate_effective_date
3. Cost computation function using rate table
4. GET /ledger/cost endpoint for aggregated reporting
5. Staleness warning when rates > 30 days old

Files currently tracking costs:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py` — hardcoded COST_PER_TOKEN dict, needs to read from model_rates table
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\schema.py` — creates events table, needs migration for new columns + model_rates table
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — writes events, needs to accept new cost params
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\llm\test_cost.py` — existing tests, will need updates

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\schema.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\llm\test_cost.py`

## Deliverables
- [ ] New `model_rates` table in schema.py with columns: model_name (TEXT PRIMARY KEY), cost_per_mtok_input (REAL), cost_per_mtok_output (REAL), rate_effective_date (TIMESTAMP)
- [ ] Migration in schema.py to add 4 new columns to events table: cost_per_mtok_input, cost_per_mtok_output, model_name, rate_effective_date
- [ ] Seed data in schema.py: populate model_rates with claude-haiku-4-5, claude-sonnet-4-5, claude-sonnet-4-6, claude-opus-4-6, gpt-4o, gpt-4o-mini
- [ ] Update writer.py write_event() to accept new parameters: cost_per_mtok_input, cost_per_mtok_output, model_name, rate_effective_date
- [ ] Update cost.py to read from model_rates table instead of hardcoded dict
- [ ] Add staleness_check() function in cost.py: returns True + warning if rate_effective_date > 30 days old
- [ ] New module: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\cost_reporter.py` with get_cost_summary() function
- [ ] New route: GET /ledger/cost in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\ledger.py` (create if doesn't exist)
- [ ] GET /ledger/cost returns: tokens_up (int), tokens_down (int), cost_up_usd (float), cost_down_usd (float), by_model (dict[str, dict])
- [ ] All costs stored in scientific notation (REAL type handles this natively)
- [ ] Update emit_llm_event() to populate new fields from model_rates table

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - model_rates table seeded on fresh database
  - model_rates table preserved on existing database
  - get_cost_summary() handles zero events
  - get_cost_summary() handles missing model_name (old events)
  - staleness_check() warns when rate_effective_date > 30 days
  - GET /ledger/cost returns 200 with correct schema
  - GET /ledger/cost aggregates by model correctly
  - emit_llm_event() looks up rates from model_rates table
  - Unknown model falls back to default rates
  - Scientific notation precision preserved (test with very small values like 0.25e-6)

## Constraints
- No file over 500 lines
- No stubs
- Do NOT modify existing events — only add new columns (nullable, no defaults)
- Three currencies always tracked: CLOCK, COIN (USD), CARBON
- Rate lookup must be fast: use PRAGMA query for model_rates, cache in memory if needed
- Scientific notation storage: SQLite REAL type handles this natively, no special formatting needed
- Backward compatibility: existing events without model_name should not break queries

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-085-RESPONSE.md`

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
