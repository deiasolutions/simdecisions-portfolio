# SPEC: Cost Storage Format + Model Rate Lookup Table

## Priority
P1

## Objective
Define how three currencies (CLOCK, COIN, CARBON) are stored per operation, and add a model rate lookup table so COIN can be computed from token counts.

## Context
Files to read first:
- `docs/specs/SPEC-COST-STORAGE-RATE-LOOKUP.docx` (existing spec)
- `hivenode/ledger/writer.py` (Event Ledger)
- `hivenode/ledger/schemas.py` (event schemas)

## Acceptance Criteria

### Token & Model Capture (MANDATORY — nothing works without this)
- [ ] Every LLM call MUST capture and store: model used (actual model string, not a default), input_tokens (tokens up), output_tokens (tokens down)
- [ ] CLI dispatch adapter (`hivenode/adapters/cli/claude_cli_subprocess.py`) MUST extract input_tokens and output_tokens from Claude Code's JSON output — currently broken, returns 0 for everything
- [ ] Heartbeats MUST include model, input_tokens, output_tokens so build monitor can display them
- [ ] CCCMetadata.model_for_cost MUST come from the actual dispatch, NEVER hardcoded

### Cost Storage
- [ ] Cost stored as three fields on every Event Ledger entry: clock_ms (int), coin_usd (float, stored as scientific notation e.g. 3.0e-4), carbon_grams (float)
- [ ] Model rate lookup table in hivenode/config/model_rates.yml:
  ```yaml
  rates:
    claude-opus-4-6: { input_per_million: 15.00, output_per_million: 75.00 }
    claude-sonnet-4-6: { input_per_million: 3.00, output_per_million: 15.00 }
    claude-haiku-4-5: { input_per_million: 0.80, output_per_million: 4.00 }
    gpt-4o: { input_per_million: 2.50, output_per_million: 10.00 }
  ```
- [ ] compute_coin(model, input_tokens, output_tokens) -> float USD
- [ ] compute_carbon(model, input_tokens, output_tokens) -> float grams (estimate based on published data center PUE)
- [ ] LLM Router auto-attaches cost to every Event Ledger entry after an LLM call
- [ ] Build monitor shows cumulative cost from these real values (not hardcoded $0.00)
- [ ] 10+ tests (including token capture verification)

## Smoke Test
- [ ] Send a chat message -> Event Ledger entry has non-zero coin_usd and carbon_grams
- [ ] Build monitor header shows real cost for bee dispatches

## Model Assignment
sonnet
