# SPEC: BL-085 Cost Storage Format + Model Rate Lookup Table

## Priority
P2

## Objective
Store token costs in scientific notation for precision. Maintain a platform-level rate lookup table mapping model names to per-million-token costs. Full spec at `docs/specs/SPEC-COST-STORAGE-RATE-LOOKUP.docx`.

## Context
Schema additions to Event Ledger: `cost_per_mtok_input` (REAL), `cost_per_mtok_output` (REAL), `model_name` (TEXT), `rate_effective_date` (TIMESTAMP).

Rate lookup table in PostgreSQL alongside Event Ledger. Maps model_name to input/output rates.

Cost formula: `cost_usd = (tokens_input * cost_per_mtok_input / 1_000_000) + (tokens_output * cost_per_mtok_output / 1_000_000)`

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — Event Ledger writer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\models.py` — Event Ledger models
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py` — existing cost calculation

## Acceptance Criteria
- [ ] Rate lookup table: model_name, cost_per_mtok_input, cost_per_mtok_output, rate_effective_date
- [ ] Pre-populated rates for: claude-haiku-4-5, claude-sonnet-4-5, claude-sonnet-4-6, claude-opus-4-6, gpt-4o, gpt-4o-mini
- [ ] Scientific notation storage for precision at small values
- [ ] Cost computation function using rate table
- [ ] Staleness warning when rate_effective_date > 30 days old
- [ ] GET /ledger/cost endpoint reports tokens_up, tokens_down, cost_up_usd, cost_down_usd, by_model breakdown
- [ ] Schema migration adds columns to events table
- [ ] 8+ tests
- [ ] No file over 500 lines

## Model Assignment
haiku

## Constraints
- Do NOT modify existing Event Ledger events — only add new columns and a lookup table
- Three currencies always tracked: CLOCK, COIN, CARBON
