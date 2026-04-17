# Carbon Methodology — DEIA Energy Accounting

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\carbon.yml`
**Additional Source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\grace.yml`
**ADR:** ADR-015 (Carbon Accounting)
**Last Updated:** 2026-03-17

---

## Overview

DEIA tracks the **carbon footprint** of AI model usage. Every API call to Claude, GPT, Gemini, or Llama generates CO2 emissions (from electricity consumed by the model's inference hardware). DEIA measures these emissions in **grams of CO2 equivalent (CO2e)** and enforces budget limits.

This document explains:
- How energy consumption is estimated per model
- How carbon emissions are calculated from energy + regional intensity
- How budgets are enforced (daily, weekly, monthly)
- How grace periods work when budgets are exceeded

---

## Why Track Carbon?

AI models consume **significant energy**. A single GPT-4 API call can consume as much electricity as leaving a lightbulb on for an hour. At scale, this adds up:

- **Environmental impact:** Every kWh of electricity generates CO2 (depending on the regional power grid)
- **Cost impact:** Energy costs money. Tracking carbon is a proxy for tracking cost.
- **Ethical responsibility:** DEIA's governance model includes **environmental accountability**. If we enforce ethics rules for data privacy and security, we should also enforce limits on environmental impact.

---

## Methodology Overview

DEIA calculates carbon emissions in three steps:

1. **Estimate energy consumption** — Based on model type and token count (input + output)
2. **Apply regional carbon intensity** — Convert kWh to CO2e based on the regional power grid
3. **Check against budgets** — Enforce daily, weekly, and monthly limits

Formula:

```
Energy (kWh) = (input_tokens / 1000) * input_kwh_per_1k + (output_tokens / 1000) * output_kwh_per_1k
Carbon (g CO2e) = Energy (kWh) * regional_intensity (g/kWh)
```

---

## Model Energy Estimates

**Source:** `carbon.yml` → `model_energy`

DEIA includes energy estimates for 8 major LLM models. These are **approximations** based on published research and vendor disclosures. Actual energy consumption varies based on hardware, batch size, and model version.

### Claude Models

| Model | Input kWh per 1k tokens | Output kWh per 1k tokens | Notes |
|-------|------------------------|-------------------------|-------|
| **claude-opus-4** | 0.0080 | 0.0120 | Largest Claude model; highest energy consumption |
| **claude-sonnet-4** | 0.0030 | 0.0045 | Mid-tier Claude model; balanced performance/energy |
| **claude-haiku-4** | 0.0008 | 0.0012 | Smallest Claude model; lowest energy consumption |

**Why output uses more energy:**
Generating output tokens is more computationally expensive than processing input tokens. Output generation requires iterative forward passes through the model, while input processing is a single pass.

**Example:** 10k input + 2k output with **claude-sonnet-4** = 0.039 kWh = 15.6 g CO2e (at US average 400 g/kWh)

### GPT Models

| Model | Input kWh per 1k tokens | Output kWh per 1k tokens | Notes |
|-------|------------------------|-------------------------|-------|
| **gpt-4o** | 0.0040 | 0.0060 | OpenAI's flagship model; high energy consumption |
| **gpt-4o-mini** | 0.0015 | 0.0022 | Smaller GPT variant; lower energy consumption |

**Example:** 5k input + 1k output with **gpt-4o** = 0.026 kWh = 9.88 g CO2e (at Texas 380 g/kWh)

### Gemini Models

| Model | Input kWh per 1k tokens | Output kWh per 1k tokens | Notes |
|-------|------------------------|-------------------------|-------|
| **gemini-pro** | 0.0035 | 0.0050 | Google's multimodal model; mid-tier energy |

**Example:** 8k input + 1.5k output with **gemini-pro** = 0.0355 kWh = 8.875 g CO2e (at EU 250 g/kWh)

### Llama Models

| Model | Input kWh per 1k tokens | Output kWh per 1k tokens | Notes |
|-------|------------------------|-------------------------|-------|
| **llama-70b** | 0.0025 | 0.0035 | Meta's 70-billion-parameter model; mid-tier energy |
| **llama-8b** | 0.0005 | 0.0008 | Smallest Llama model; very low energy consumption |

**Example:** 15k input + 3k output with **llama-70b** = 0.048 kWh = 11.04 g CO2e (at California 230 g/kWh)

---

## Regional Carbon Intensity

**Source:** `carbon.yml` → `region_intensity`

Carbon intensity measures **how much CO2 is emitted per kWh of electricity generated** in a specific region. Regions with more renewable energy (solar, wind, hydro) have lower carbon intensity. Regions relying on coal or natural gas have higher carbon intensity.

| Region | Carbon Intensity (g CO2e / kWh) | Notes |
|--------|--------------------------------|-------|
| **us_average** | 400 | US national average (mix of coal, gas, renewables) |
| **texas** | 380 | Texas grid (natural gas heavy) |
| **california** | 230 | California grid (high renewable penetration) |
| **eu_average** | 250 | EU average (moderate renewable mix) |
| **france** | 50 | France (nuclear + hydro; very low carbon) |

**Default region:** `us_average` (400 g/kWh)

**Why regional intensity matters:**
Running the same model in **France** (50 g/kWh) generates **8x less CO2** than running it in **Texas** (380 g/kWh). DEIA allows you to configure the region to match your actual infrastructure location.

**How to set region:**
Update `default_region` in `carbon.yml`:

```yaml
default_region: "california"
```

Or override per-request via API:

```python
response = agent.call(model="claude-sonnet-4", region="france")
```

---

## Carbon Budgets

**Source:** `carbon.yml` → `budgets`

DEIA enforces three levels of carbon budgets:

| Budget Type | Limit (g CO2e) | Reset Period | Notes |
|-------------|----------------|--------------|-------|
| **Daily** | 50,000 | 24 hours | ~128 Claude Sonnet calls (10k input + 2k output each) |
| **Weekly** | 250,000 | 7 days | ~641 Claude Sonnet calls |
| **Monthly** | 1,000,000 | 30 days | ~2,564 Claude Sonnet calls |

**Alert threshold:** `0.8` (80%)

When carbon consumption reaches **80% of any budget**, DEIA triggers an **alert** (logged to the event ledger, optionally sent to admins via email/Slack).

**Hard cap:** `false` (default)

When `hard_cap: false`, exceeding a budget triggers a **warning** but does not block further API calls. When `hard_cap: true`, exceeding a budget **blocks** all further API calls until the budget resets.

**Why default to soft cap:**
Hard caps can **break production systems** if a budget is misconfigured or if usage spikes unexpectedly. DEIA defaults to **monitoring and alerting** rather than hard blocking. You can enable hard caps in environments where budget enforcement is critical (e.g., research projects with fixed grants).

**Example scenario (soft cap):**
- Daily budget: 50,000 g CO2e
- Current usage: 42,000 g CO2e (84%)
- New request: 10,000 g CO2e (would bring total to 52,000 g)

With `hard_cap: false`:
1. Alert triggered: "Daily carbon budget exceeded (104%)"
2. Request **allowed** (total: 52,000 g)
3. Event logged to ledger

With `hard_cap: true`:
1. Request **blocked** (budget exceeded)
2. Gate disposition: `BLOCK`
3. Event logged to ledger
4. User notified: "Daily carbon budget exceeded. Retry after reset."

---

## Grace Periods for Budget Violations

**Source:** `grace.yml`

When a carbon budget is exceeded, DEIA can apply a **grace period** before allowing the next request. This prevents "spamming" the gate enforcer with repeated requests immediately after a budget violation.

### Grace Period by Violation Type

**Source:** `grace.yml` → `by_violation_type`

| Violation Type | Grace Period (seconds) | Notes |
|----------------|------------------------|-------|
| **forbidden_action** | 60 | Agent attempted a forbidden action (e.g., delete production data) |
| **forbidden_target** | 60 | Agent attempted to modify a forbidden target (e.g., event ledger) |
| **domain_violation** | 120 | Agent attempted to access a domain not in `allowed_domains` |
| **tier_exceeded** | 300 | Agent attempted an action beyond its autonomy tier |
| **missing_rationale** | 30 | Agent submitted a request without a required rationale |
| **escalation_bypassed** | 180 | Agent attempted to bypass an escalation trigger |

**How it works:**
When an agent violates a rule, the gate enforcer starts a cooldown timer. The agent **cannot retry the same action** until the grace period expires.

**Example:**
Agent attempts to delete production data. Gate enforcer blocks the request and starts a **60-second grace period**. Agent retries 10 seconds later. Gate enforcer rejects with: "Grace period active. Retry after 50s."

---

### Grace Period by Gate Disposition

**Source:** `grace.yml` → `by_gate_disposition`

| Gate Disposition | Grace Period (seconds) | Notes |
|------------------|------------------------|-------|
| **BLOCK** | 120 | Request was hard-blocked (forbidden action/target) |
| **HOLD** | 60 | Request was paused (missing rationale or pending review) |
| **ESCALATE** | 0 | Request escalated to human (no cooldown; human decides timing) |

**Why ESCALATE has zero grace period:**
When a request is escalated, the **human** controls the timing of the retry. There's no need for an automatic cooldown.

**Why BLOCK has longer grace period than HOLD:**
`BLOCK` indicates a **hard violation** (forbidden action/target). `HOLD` indicates a **soft violation** (missing info). Hard violations deserve longer cooldowns.

---

### No-Grace Gates

**Source:** `grace.yml` → `no_grace_gates`

Some gate dispositions **never apply grace periods**:

| Gate Disposition | Grace Period | Notes |
|------------------|--------------|-------|
| **REQUIRE_HUMAN** | None | Human approval required; no automatic retry |
| **security_critical** | None | Security violations escalate immediately; no cooldown |

**Why:**
These dispositions represent **critical scenarios** where automatic retries are inappropriate. Instead, a human must explicitly approve or deny the action.

---

## Calculation Method: Step-by-Step

**Inputs:**
- Model: `claude-sonnet-4`
- Input tokens: 10,000
- Output tokens: 2,000
- Region: `us_average`

**Step 1: Calculate energy consumption**

```
input_kwh_per_1k = 0.0030 (from carbon.yml)
output_kwh_per_1k = 0.0045 (from carbon.yml)

Energy = (10,000 / 1000) * 0.0030 + (2,000 / 1000) * 0.0045
       = (10 * 0.0030) + (2 * 0.0045)
       = 0.030 + 0.009
       = 0.039 kWh
```

**Step 2: Apply regional carbon intensity**

```
regional_intensity = 400 g/kWh (us_average)

Carbon = 0.039 kWh * 400 g/kWh
       = 15.6 g CO2e
```

**Step 3: Check against budgets**

```
Current daily usage: 48,000 g CO2e
New request: 15.6 g CO2e
Total after request: 48,015.6 g CO2e

Daily budget: 50,000 g CO2e
Threshold (80%): 40,000 g CO2e

Status: ✅ Within budget (96% utilized)
Alert: ⚠️ Yes (exceeded 80% threshold)
Action: Allow request, trigger alert
```

**Step 4: Log to event ledger**

```json
{
  "timestamp": "2026-03-17T14:32:15Z",
  "event_type": "api_call",
  "model": "claude-sonnet-4",
  "input_tokens": 10000,
  "output_tokens": 2000,
  "energy_kwh": 0.039,
  "carbon_g": 15.6,
  "region": "us_average",
  "daily_usage_g": 48015.6,
  "daily_budget_g": 50000,
  "alert": true,
  "alert_reason": "Daily carbon usage at 96% of budget"
}
```

---

## Real-World Example: Budget Exceeded

**Scenario:**
A research team is running automated experiments with `gpt-4o`. They've configured:

```yaml
budgets:
  daily_limit_g: 10000
  alert_threshold: 0.8
  hard_cap: true
```

**Current state:**
- Daily usage: 9,500 g CO2e (95% of budget)
- Remaining budget: 500 g CO2e

**New request:**
- Model: `gpt-4o`
- Input: 20,000 tokens
- Output: 5,000 tokens
- Region: `texas` (380 g/kWh)

**Calculation:**

```
Energy = (20 * 0.0040) + (5 * 0.0060)
       = 0.080 + 0.030
       = 0.110 kWh

Carbon = 0.110 kWh * 380 g/kWh
       = 41.8 g CO2e
```

**Budget check:**

```
Current usage: 9,500 g
New request: 41.8 g
Total: 9,541.8 g

Daily budget: 10,000 g
Hard cap: true

Status: ❌ Budget exceeded (9,541.8 > 10,000)
Action: BLOCK request
```

**Gate enforcer response:**

```json
{
  "disposition": "BLOCK",
  "reason": "Daily carbon budget exceeded",
  "current_usage_g": 9500,
  "request_carbon_g": 41.8,
  "daily_budget_g": 10000,
  "retry_after": "2026-03-18T00:00:00Z",
  "grace_period_seconds": 120
}
```

**What happens:**
1. Request is blocked
2. Event logged to ledger
3. Team is notified: "Daily carbon budget exceeded. Next reset: midnight UTC."
4. Grace period: 120 seconds (cannot retry for 2 minutes)
5. After midnight UTC, daily budget resets to 0 g, requests allowed again

---

## How to Optimize Carbon Usage

### 1. Use Smaller Models

**Example:**
Switching from `claude-opus-4` to `claude-haiku-4` reduces energy consumption by **~10x** per token.

**Trade-off:**
Smaller models have lower quality outputs. Use small models for simple tasks (classification, extraction) and large models for complex tasks (reasoning, writing).

---

### 2. Reduce Output Length

Output tokens consume **more energy** than input tokens. Limit output length when possible:

```python
response = agent.call(
    model="claude-sonnet-4",
    max_tokens=500,  # Instead of 2000
)
```

---

### 3. Cache Input Tokens

Many models support **prompt caching** (reusing previously processed input tokens). This reduces input token processing costs.

**Example (Claude):**

```python
response = client.messages.create(
    model="claude-sonnet-4",
    system=[
        {
            "type": "text",
            "text": "You are an expert in...",
            "cache_control": {"type": "ephemeral"}  # Cache this
        }
    ],
    messages=[...]
)
```

Cached tokens consume **~90% less energy** than uncached tokens.

---

### 4. Choose Low-Carbon Regions

If you control where your infrastructure runs, deploy to **low-carbon regions**:

| Region | Carbon Intensity (g/kWh) | CO2 Reduction vs US Average |
|--------|--------------------------|----------------------------|
| **France** | 50 | 87.5% lower |
| **California** | 230 | 42.5% lower |
| **EU Average** | 250 | 37.5% lower |

**Example:**
Running 10,000 API calls in **France** instead of **Texas** saves:

```
Texas: 10,000 calls * 15.6 g (per call) * (380/400) = 148,200 g CO2e
France: 10,000 calls * 15.6 g (per call) * (50/400) = 19,500 g CO2e

Savings: 128,700 g CO2e (86.8% reduction)
```

---

## Next Steps

- **Review ethics framework:** See [ethics.md](ethics.md) for forbidden actions and escalation triggers
- **Understand governance:** See [governance.md](governance.md) for how carbon limits are enforced via gates
- **Read the config files:**
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\carbon.yml`
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\grace.yml`

---

**Version:** 1.0.0
**Last Updated:** 2026-03-17
**Source:** ADR-015, `carbon.yml`, `grace.yml`
