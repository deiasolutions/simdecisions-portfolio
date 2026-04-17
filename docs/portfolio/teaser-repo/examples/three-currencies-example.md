# Three Currencies: CLOCK, COIN, CARBON

**System:** Multi-dimensional resource accounting for AI agent work
**Purpose:** Portfolio demonstration of CLOCK/COIN/CARBON tracking

---

## Why Three Currencies?

Most teams track cost (COIN) only. Some track time (CLOCK). Almost none track carbon (CARBON).

**Why three currencies matter:**

- **CLOCK:** Wall time is a constraint. If a build takes 4 hours, you can't ship 6 builds per day. Time is the ultimate non-renewable resource.
- **COIN:** USD is the budget constraint. Every LLM call, every compute hour, every storage byte costs money. Track it or run out.
- **CARBON:** CO2e is the externality. LLM inference generates ~0.1g CO2 per 1k tokens (Voyage embeddings, Anthropic Claude). Multiply by 100k tokens/day, 365 days/year — that's 3.65 kg CO2/year per agent. Scale to 100 agents: 365 kg CO2/year. Measure it or ignore the real cost.

---

## Response File Template (Mandatory 8 Sections)

Every bee response file includes Clock/Cost/Carbon:

```markdown
# TASK-001: Build Export Button Component -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-16

## Files Modified
- browser/src/components/buttons/ExportButton.tsx (created, 42 LOC)
- browser/src/components/buttons/ExportButton.test.tsx (created, 68 LOC)
- browser/src/components/toolbar/Toolbar.tsx (modified, +3 LOC)

## What Was Done
- Created ExportButton component with Lucide Download icon
- Added tests for rendering, click behavior, disabled state
- Integrated into Toolbar

## Test Results
- 4 tests run
- 4 tests pass
- 0 failures

## Build Verification
All tests pass. Build succeeds.

## Acceptance Criteria
- [x] ExportButton.tsx created
- [x] ExportButton.test.tsx created
- [x] Toolbar.tsx modified
- [x] Tests written first (TDD)
- [x] All tests pass

## Clock / Cost / Carbon
- **Clock:** 87s (1.5m)
- **Cost:** $0.0043
- **Carbon:** ~0.4g CO2

## Issues / Follow-ups
None. All requirements met.
```

---

## Phase Reports (Token Breakdown by Model)

**Phase 0 Coverage Report Example:**

```markdown
## Token Usage by Model

| Operation | Model | Input Tokens | Output Tokens | Total Tokens | Cost |
|-----------|-------|--------------|---------------|--------------|------|
| Extract requirements | Haiku | 1,200 | 450 | 1,650 | $0.0033 |
| Check coverage (10 reqs) | Haiku | 8,500 | 2,100 | 10,600 | $0.0212 |
| **TOTAL Phase 0** | - | **9,700** | **2,550** | **12,250** | **$0.0245** |

## Model Breakdown

| Model | Input | Output | Total | Cost |
|-------|-------|--------|-------|------|
| Haiku | 9,700 | 2,550 | 12,250 | $0.0245 |

## 3-Currency Analysis

| Currency | Value |
|----------|-------|
| Clock | 5s |
| Cost | $0.0245 |
| Carbon | ~0.5g CO2 |
```

---

## Completion Report (Full Build)

**TASK-001 Completion Report:**

```markdown
## Token Summary by Phase

| Phase | Input | Output | Total | Cost |
|-------|-------|--------|-------|------|
| Gate 0 | 3,200 | 1,050 | 4,250 | $0.0085 |
| Phase 0 | 9,700 | 2,550 | 12,250 | $0.0245 |
| Phase 1 | 5,200 | 1,800 | 7,000 | $0.0140 |
| Phase 2 | 6,500 | 2,200 | 8,700 | $0.0174 |
| Workers | 42,000 | 18,500 | 60,500 | $0.1210 |
| **TOTAL** | **66,600** | **26,100** | **92,700** | **$0.1854** |

## Token Summary by Model

| Model | Input | Output | Total | Cost | % of Total Cost |
|-------|-------|--------|-------|------|-----------------|
| Haiku | 51,400 | 21,300 | 72,700 | $0.1454 | 78% |
| Sonnet | 15,200 | 4,800 | 20,000 | $0.0346 | 19% |
| Voyage (embeddings) | - | - | - | $0.0054 | 3% |
| **TOTAL** | **66,600** | **26,100** | **92,700** | **$0.1854** | **100%** |

## 3-Currency Analysis

| Currency | Total |
|----------|-------|
| Clock | 187s (3.1m) |
| Cost | $0.1854 |
| Carbon | ~19g CO2 |
```

---

## Budget Tracking

**Per Build (avg 10 requirements, 5 tasks):**

| Phase | Clock | Cost | Carbon |
|-------|-------|------|--------|
| Gate 0 | ~5s | $0.008 | ~0.5g |
| Phase 0 | ~5s | $0.024 | ~0.5g |
| Phase 1 | ~8s | $0.014 | ~0.8g |
| Phase 2 | ~10s | $0.018 | ~1.0g |
| Workers (5 bees) | ~120s | $0.120 | ~12g |
| **TOTAL** | **~148s** | **$0.184** | **~15g** |

**Scaled to 1,358 builds:**

| Currency | Per Build | 1,358 Builds | Annual (5000 builds) |
|----------|-----------|--------------|----------------------|
| **Clock** | 148s | 56 hours | 206 hours (8.6 days) |
| **Cost** | $0.18 | $250 | $920 |
| **Carbon** | 15g | 20 kg | 75 kg |

**Comparison:**

- **Manual code review:** 1-2 hours per build → 5000-10000 hours/year (2.5-5 FTE)
- **Automated validation:** 148s per build → 206 hours/year (0.1 FTE)
- **Productivity gain:** ~25x faster with systematic validation

---

## Carbon Emission Factors

**Config (carbon.yml excerpt):**

```yaml
models:
  haiku:
    input_co2_per_1k_tokens: 0.10  # grams
    output_co2_per_1k_tokens: 0.15  # grams (higher for generation)

  sonnet:
    input_co2_per_1k_tokens: 0.20  # grams (larger model)
    output_co2_per_1k_tokens: 0.30  # grams

  voyage:
    embedding_co2_per_1k_tokens: 0.05  # grams (embedding only)
```

**Calculation Example:**

```python
# Haiku: 51,400 input + 21,300 output tokens
haiku_carbon = (51.4 * 0.10) + (21.3 * 0.15)
             = 5.14 + 3.20
             = 8.34g CO2

# Sonnet: 15,200 input + 4,800 output tokens
sonnet_carbon = (15.2 * 0.20) + (4.8 * 0.30)
              = 3.04 + 1.44
              = 4.48g CO2

# Voyage: embeddings (assume 10k tokens equivalent)
voyage_carbon = 10 * 0.05
              = 0.50g CO2

# Total
total_carbon = 8.34 + 4.48 + 0.50
             = 13.32g CO2
```

---

## Why This Differentiates

**What every shop does:**

- Track USD cost (COIN)

**What most shops don't do:**

- Track wall time systematically (CLOCK)
- Track carbon emissions (CARBON)
- Break down cost by model and phase
- Calibrate estimates from actuals (see Estimation Calibration below)

**Benefit:**

- **Multi-constraint optimization:** "Can we reduce carbon by 20% without increasing cost >10%?" → Switch some Sonnet tasks to Haiku.
- **Budget enforcement:** "Stop when session cost hits $50" → Queue runner halts before overspend.
- **Time planning:** "We have 4 hours until deploy. Can we fit 15 specs?" → CLOCK budget says yes/no.
- **Carbon accounting:** "Our annual AI usage = 75kg CO2, equivalent to driving 185 miles in a car." → Measure externalities, not just direct costs.

---

## Estimation Calibration

**Problem:** Initial estimates are often wrong. Build tasks might take 35% longer than estimated, while spec tasks finish 8% faster.

**Solution:** Track actuals vs estimates across 3 currencies, compute calibration factors, apply to future estimates.

**Example:**

```python
# Initial estimate for TASK-001
est_clock = 60s
est_cost = $0.05
est_carbon = 5g

# Actual outcome
act_clock = 87s
act_cost = $0.0043
act_carbon = 0.4g

# Calibration factor
calibration_clock = act_clock / est_clock = 1.45  # 45% longer
calibration_cost = act_cost / est_cost = 0.086    # 91% cheaper (Haiku vs Sonnet assumption)
calibration_carbon = act_carbon / est_carbon = 0.08  # 92% less carbon
```

**Apply to next estimate:**

```python
# Next build task estimate (before calibration)
est_clock_raw = 80s
est_cost_raw = $0.06
est_carbon_raw = 6g

# After calibration
est_clock_calibrated = 80s * 1.45 = 116s
est_cost_calibrated = $0.06 * 0.086 = $0.0052
est_carbon_calibrated = 6g * 0.08 = 0.48g
```

**From 60+ calibrated tasks:**

- Week-over-week accuracy improves ~40%
- Budget forecasting error drops from ±50% to ±15%

---

**END OF THREE CURRENCIES EXAMPLE**

Full carbon accounting methodology and calibration database available in private repo on request.
