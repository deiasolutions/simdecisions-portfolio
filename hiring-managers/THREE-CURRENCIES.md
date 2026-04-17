# Three Currencies: CLOCK, COIN, CARBON

Every task in SimDecisions is tracked in three currencies.

---

## Why Three?

| Currency | Measures | Why It Matters |
|----------|----------|----------------|
| **CLOCK** | Wall time (seconds) | Time is the ultimate non-renewable resource |
| **COIN** | Cost (USD) | LLM calls cost money — track or overspend |
| **CARBON** | Emissions (g CO2e) | Environmental accountability at scale |

Most teams track cost only. Some track time. Almost none track carbon.

---

## How It Works

Every task response file includes:

```
## Clock / Cost / Carbon
- **Clock:** 8 minutes (sandbox creation + analysis)
- **Cost:** ~$0.15 USD
- **Carbon:** ~0.05g CO2e
```

---

## Implementation

| Component | Location |
|-----------|----------|
| Carbon config | `.deia/config/carbon.yml` — model-specific energy rates, daily/weekly/monthly CO2 budgets |
| Cost calculation | `hivenode/hive_mcp/tools/telemetry.py` — `cost_summary()` function |
| Event logging | `hivenode/ledger/benchmark_events.py` — `BenchmarkTaskCompleteEvent` dataclass with `clock_seconds`, `coin_usd`, `carbon_kg` |

---

## Current Tracking

| Metric | Status | Method |
|--------|--------|--------|
| CLOCK | Active | Wall time from task start to completion |
| COIN | Active | Token count times model pricing |
| CARBON | Active | Tokens as proxy with model-specific rates from `carbon.yml` |

---

## Carbon Tracking Note

**Tokens in/out are tracked as a proxy for carbon emissions.**

Why proxy? **Anthropic, OpenAI, and Google do not currently publish per-model carbon footprint data.** Until vendors provide this:
- We track token counts per model
- We apply estimated g CO2e per 1k tokens (configured in `carbon.yml`)
- We flag this as approximate in reports

When vendor data becomes available, we'll switch to direct measurement.

---

## Why This Differentiates

Every shop tracks cost. Not every shop tracks time and carbon together.

This demonstrates systems thinking — optimizing across multiple constraints, not just minimizing one variable.
