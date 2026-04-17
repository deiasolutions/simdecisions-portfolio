# TASK-BREADTH-001 — Platform Breadth Survey
## What Exists, What Is Adjacent, What Is Possible

**Priority:** P1
**Model:** Opus
**Type:** Research, ideation, and gap mapping — no code changes
**Date:** 2026-04-06

---

## Objective

Map the full surface area of the platform from a capability and opportunity perspective.
Three goals:

1. Find capabilities that exist in code but have no product surface — buried treasure
2. Find combinations of existing capabilities that would unlock something new with minimal work
3. Surface genuinely new territory that the platform's architecture makes possible but that
   has not been discussed or specced

This is not a bug hunt. This is an opportunity hunt.

---

## Part 1 — Buried Treasure Survey

Read the following directories and files. For each module, answer: does this capability have
any UI surface, any API route, any EGG that exposes it to a user? If not, it is buried.

### Directories to survey

- `efemera/src/efemera/surrogates/` — full directory, every file
- `efemera/src/efemera/optimization/` — full directory
- `efemera/src/efemera/tabletop/` — full directory
- `efemera/src/efemera/dialects/` — full directory
- `efemera/src/efemera/builds/` — full directory
- `efemera/src/efemera/entities/` — full directory (Four-Vector profiles)
- `efemera/src/efemera/pheromones/` — full directory
- `efemera/src/efemera/oracle/` — full directory (Oracle Tier Spectrum)
- `efemera/src/efemera/skills/` — full directory (Agent Skills governance)
- `hivenode/routes/` — every route file, list all endpoints
- `engine/` — full directory

### For each module report

| Module | What it does (1 sentence) | Lines | Tests passing | API route? | UI surface? | EGG? | Verdict |
|--------|--------------------------|-------|---------------|------------|-------------|------|---------|
| ... | ... | ... | ... | yes/no | yes/no | yes/no | EXPOSED / BURIED / PARTIAL |

BURIED = real capability, no user-facing surface at all
PARTIAL = some exposure but significant capability hidden
EXPOSED = user can actually reach and use this today

---

## Part 2 — Combination Opportunities

Given what you find in Part 1, identify combinations of existing buried or partial capabilities
that would unlock something meaningful with the least new code. Think in terms of:

- What does A produce that B could consume, if they were connected?
- What API already exists that a new EGG could expose with no backend work?
- What two buried modules, wired together, would produce a demo-worthy capability?

Report format: at least 10 combinations. For each:

**Combination:** Module A + Module B (+ Module C if needed)
**What it unlocks:** One sentence on the user-visible capability
**Missing piece:** The specific connection that doesn't exist today
**Effort estimate:** S (< 100 lines) / M (100-500 lines) / L (500+ lines)
**Demo value:** Low / Medium / High / Jaw-drop

---

## Part 3 — New Territory: What The Architecture Makes Possible

This is the hardest part. Based on what you see in the codebase — the actual primitives,
data structures, protocols, and patterns — what could be built that has not been discussed
at all? Not features. Capabilities that emerge from the combination of what exists.

Think about:

- What does the Event Ledger make possible that no one has named yet?
- What does seeded reproducibility + Alterverse enable beyond what's been specced?
- What does the Four-Vector entity profile enable if applied to humans, not just agents?
- What does the pheromone signal layer enable beyond task coordination?
- What does the dialect compiler architecture enable if you added a new dialect?
- What does hash-chaining the ledger enable beyond tamper-evidence?
- What does the tabletop engine enable for training, onboarding, or certification?
- What does the surrogate pipeline enable if the surrogate is the product, not the simulation?

Report: at least 12 genuinely new ideas. For each:

**Idea name:** Short memorable name
**What it is:** 2-3 sentences max
**What makes it possible:** Specific existing modules it builds on
**Why it hasn't been built:** Honest assessment — missing piece, not yet seen, too ambitious?
**Excitement level:** Useful / Interesting / Genuinely novel / Category-defining

---

## Part 4 — The Three Platforms Nobody Has Built

Step back further. Given the full picture of what exists:

If you were going to identify three distinct products — not features, full products — that could
be spun out of this codebase and marketed independently, what would they be?

For each:
- Product name and one-line description
- Which existing modules form its core
- Who buys it and why
- What is missing to make it shippable as a standalone product
- How long until it could be demonstrated to a prospect (in tasks, not hours)

These should be products that don't exist in the market today, or exist badly, and that the
platform's architecture gives a genuine unfair advantage on.

---

## Part 5 — Integration Health Map

Survey the major seams between platform components. For each seam, report whether data flows
correctly across it, what the protocol is, and whether there are known failure modes.

### Seams to check

| Seam | From | To | Protocol | Health |
|------|------|----|----------|--------|
| Simulation → Ledger | DES engine | Event Ledger | ledger_adapter | ? |
| Ledger → Surrogate | Event Ledger | Training pipeline | ? | ? |
| PHASE-IR → All four modes | IR spec | DES/Production/Tabletop/Optimization | ? | ? |
| Dialect → PHASE-IR | BPMN/SBML/L-sys | IR | Compiler | ? |
| GateEnforcer → Agent skills | ethics.yml | Skills wrapper | ? | ? |
| Pheromone → Task routing | Signal layer | Queue runner | ? | ? |
| Four-Vector → Task assignment | Entity profiles | Oracle routing | ? | ? |
| Efemera → ShiftCenter | WebSocket relay | EGG shell | ? | ? |
| hivenode → Cloud storage | Local adapter | Cloud adapter | HTTP/JWT | ? |
| Heartbeat → Build monitor | Bee telemetry | Monitor state | POST /build/heartbeat | ? |

For each seam: **HEALTHY** / **DEGRADED** / **BROKEN** / **NOT WIRED**

For any seam that is not HEALTHY: what is the specific failure point?

---

## Part 6 — The Honest Inventory

One final synthesis. Given everything found in Parts 1–5, produce a single honest inventory
table of the platform's actual state today:

| Capability Area | What works | What's buried | What's missing | Readiness |
|----------------|------------|---------------|----------------|-----------|
| Simulation (DES) | ... | ... | ... | 1-10 |
| Optimization | ... | ... | ... | 1-10 |
| Tabletop | ... | ... | ... | 1-10 |
| Surrogate pipeline | ... | ... | ... | 1-10 |
| Governance (TSaaS) | ... | ... | ... | 1-10 |
| Dialect compilers | ... | ... | ... | 1-10 |
| Four-Vector profiles | ... | ... | ... | 1-10 |
| Pheromone signals | ... | ... | ... | 1-10 |
| Event Ledger | ... | ... | ... | 1-10 |
| ShiftCenter shell | ... | ... | ... | 1-10 |
| EGG system | ... | ... | ... | 1-10 |
| Efemera comms | ... | ... | ... | 1-10 |
| Mobile | ... | ... | ... | 1-10 |
| Notification layer | ... | ... | ... | 1-10 |
| Sync / volumes | ... | ... | ... | 1-10 |

Readiness scale:
- 1-3: Specced or partially coded, not usable
- 4-6: Built and tested, not exposed or integrated
- 7-8: Exposed and usable, gaps exist
- 9-10: Production-ready, integrated, demonstrable

---

## Constraints

- No code changes
- No fixes
- No new specs unless Part 3 ideas warrant a one-paragraph sketch
- Read widely, report honestly
- If a directory doesn't exist at the expected path, say so — don't assume

## Acceptance Criteria

- [ ] Part 1: Every module in every listed directory has a row in the buried treasure table
- [ ] Part 2: At least 10 combination opportunities identified with effort and demo value rated
- [ ] Part 3: At least 12 genuinely new ideas, not previously discussed in project docs
- [ ] Part 4: Exactly 3 standalone product proposals with buyer, missing piece, and timeline
- [ ] Part 5: All 10 seams have a health verdict
- [ ] Part 6: Full inventory table complete with readiness scores

## Deliverable

8-section response file on completion. Parts 1–6 as subsections within section 3.
No fabrication — if something is not found in code, say not found.
New ideas in Part 3 must be grounded in actual modules that exist, not wishful thinking.
