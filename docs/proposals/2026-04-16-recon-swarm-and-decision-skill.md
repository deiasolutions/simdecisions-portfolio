# Proposal: Recon-Then-Swarm Context Pattern + Data-Driven Bee Selection Skill

**Date:** 2026-04-16
**Author:** Q33NR (regent session)
**Status:** DRAFT — requesting second opinion from Mr. AI
**Audience:** Q88N (Dave) + Mr. AI

---

## TL;DR

Two intertwined ideas for the DEIA factory. We want a second opinion before committing:

1. **Recon-then-swarm:** Instead of every bee re-reading the full source slice, a single **Recon Bee** (cheap-long-context or strong-synthesis model — chosen per task) reads the codebase once and emits a **Briefing Digest**. Downstream swarm bees reference the digest plus their own narrow files. The digest compresses N bees worth of duplicated cold-reads into one.
2. **Decision skill:** Model selection (haiku / sonnet / opus / gemini / gpt) is governed by a **skill** (natural-language policy) backed by a deterministic helper (`_tools/pick_bee.py`) that computes token estimates, historical performance, and cost projections. **Business rules live in the skill, not in code.**

These are complementary: "should this be recon+swarm?" is itself a decision the skill makes.

---

## Context

**Current state of the factory (post-flatten, 2026-04-16):**

- ~976 spec tasks run this month, almost entirely Sonnet ($7.1k base / $357 at 20x plan).
- Haiku: 9 tasks ($7.45). Gemini: 1 test. Opus: zero factory runs (though live Q33NR/human sessions use Opus 4.6).
- Model assignment today is folk wisdom: "haiku for plumbing, sonnet for logic, opus for architecture."
- Every bee reads its own "Files to Read First" from cold. For waves of 3–5 bees on the same area, this is N× duplicate input-token spend.
- We already capture (in `/build/status`): model, cost_usd, duration_s, turns, input_tokens, output_tokens, status. We don't capture: archetype, outcome quality beyond "complete", estimated-context-at-dispatch, human verdict.

**Pain points this proposal addresses:**

- **Cost duplication.** A 200k-token context read 4 times by 4 bees costs ~4× what it should.
- **Inconsistent framing.** 4 bees reading the same files form 4 slightly different mental models. Subtle cross-cutting facts get inconsistent treatment.
- **Model-fit guesses.** "Sonnet for everything" is likely suboptimal. Some specs are haiku-cheap, some deserve opus, some are gemini-long-context plays. We are guessing.
- **Policy drift.** Any rules we bake into Python drift silently. Rules in a skill are human-readable, versioned in git, and editable without a code review cycle.

---

## Part 1: Recon-Then-Swarm

### Pattern

```
   +---------------------+
   |  Recon Bee          |   model: picked per task
   |  reads full slice   |   (e.g. gemini-2.5-pro for 500k-token sweeps,
   |  writes Digest      |    opus for subtle cross-cutting synthesis,
   +----------+----------+    sonnet-1M as the default workhorse)
              |
              v
   +---------------------+
   | Briefing Digest     |   .deia/hive/briefs/<AREA>-<DATE>.md
   | - facts             |
   | - interfaces        |
   | - invariants        |
   | - gotchas           |
   | - open questions    |
   +----------+----------+
              |
     +--------+--------+--------+--------+
     v        v        v        v        v
   Bee 1    Bee 2    Bee 3    Bee 4    Bee 5      (swarm, each reads:
   reads    reads    reads    reads    reads         - the Digest
   Digest   Digest   Digest   Digest   Digest        - its own narrow files
```

### Digest contract

A digest is a small, opinionated document — **not** a dump of file contents. It answers:

- What modules exist in this area and what is each responsible for?
- What are the public interfaces and the data contracts between them?
- What invariants or constraints must new work preserve?
- What known gotchas, dead paths, or migration-in-flight states exist?
- What is explicitly out of scope for downstream bees?
- What questions could NOT be answered from the source (escalation hooks)?

Digest format is a short Markdown template (proposed `docs/templates/briefing-digest.md`). Max size target: 3–5k tokens. If the digest is longer than that, the recon pass under-synthesized.

### When to use it

- Multi-bee waves where ≥3 bees will read the same area
- Large context slices (estimated >100k tokens of files-to-read) even for single bees
- Cross-cutting refactors or architectural changes
- When the recon cost < cumulative per-bee cold-read cost

### When NOT to use it

- Single bee + narrow scope (<3 files, <30k tokens)
- High-churn area where the digest goes stale in hours (e.g. an active spec is actively rewriting the files)
- Emergency fixes (one bee, urgent, no time for two hops)

### Model choice for the Recon role

| Profile | Best for recon when... |
|---------|------------------------|
| Gemini 2.5 Pro | Context >200k, straightforward extraction, cost-sensitive |
| Claude Sonnet (1M) | Default mid-size recon, balanced cost/quality |
| Claude Opus | Cross-file pattern recognition, subtle invariants, adversarial constraints |
| GPT-4o / o1 | Strict schema adherence in the digest output |
| Gemini Flash / Haiku | Bulk extraction only (indexes, dead-code sweeps) |

### Cost intuition (back-of-envelope)

Assume a wave of 4 bees on a 150k-token context area. Ballpark base-rate Sonnet-input ($3/Mtoken):

- **Today:** 4 × 150k × $3/M = **~$1.80** just to orient the bees, before any thinking.
- **With recon:** 1 × 150k × $3/M (recon read) + 4 × 5k × $3/M (digest read) = $0.45 + $0.06 = **~$0.51**.
- **Net:** ~$1.29 savings per 4-bee wave on the reading phase. If we run 20 such waves a month: **~$25/month**.

This is tiny. **The real win is consistency, not cost.** Every bee starts from the same synthesized view. Q33N reviewers see one source of truth. Regressions on cross-file invariants drop.

### Open questions for Mr. AI

1. **Staleness / invalidation.** What triggers a digest rebuild? Time-based? Git-diff-based? How do we detect that the digest has drifted from the code it described?
2. **Trust.** When a swarm bee discovers the digest is wrong or incomplete, what's the escalation? Dispatch a new recon? Write an errata addendum? Block and ask Q33N?
3. **Bias risk.** A bad digest contaminates the whole wave. How do we validate digest quality before swarming? A second quick verification pass by a different model?
4. **Vendor choice for recon.** Is Gemini 2.5 Pro's synthesis quality good enough for our domain (Python FastAPI + React/TS + DEIA conventions), or does Sonnet-1M justify its price premium? We do not have benchmark data.
5. **Scope of digest.** Should digests span "one spec area" (narrow) or "one subsystem" (persistent, reusable across waves)? Persistent digests amortize better but drift faster.
6. **Failure mode.** If Recon Bee produces an empty or garbage digest, what does the swarm do? Block the wave? Fall back to cold-read?

---

## Part 2: Data-Driven Bee Selection Skill

### Decision criteria (ranked by signal strength)

1. **Archetype** — research / audit / implement / hygiene / port / debug / design / bulk
2. **Token scope** — estimated input tokens from Files-to-Read-First bytes
3. **Spec quality signals** — IR density (already computed), AC count, retry count
4. **Historical performance** — per-archetype-per-model: mean cost, duration, success rate, turns
5. **Priority × budget** — P0 starts higher; P3 starts cheaper; daily spend envelope
6. **Vendor capability gaps** — vision input, CSS sensibility, tool-use reliability, schema strictness, long-context
7. **Diversity hedge** — keep ~5–10% of low-risk traffic on non-Anthropic vendors so adapters stay warm

### Data we have vs. need

**Have in `/build/status` completed[]:**
model, role, cost_usd, duration_s, turns, input_tokens, output_tokens, status, last_logged_message.

**Need to add:**
- `## Archetype` field in spec frontmatter (taxonomy: research | implement | hygiene | port | audit | debug | design | bulk)
- Estimated input tokens captured at dispatch time (computed from Files-to-Read-First sizes)
- Outcome quality label beyond "complete" — pass/partial/fail, sourced from bee response file + gate0 + queue-runner log
- Human verdict — 1-bit "kept" vs "rejected/redispatched" from Q33NR review
- Whether recon+swarm was used; digest path if so

### Skill + helper split — the core architectural decision

**Business rules live in the skill (natural language, editable by Q88N/Q33NR without a PR):**

- Archetype definitions + keyword patterns
- Thresholds (what counts as "long-context"? what IR-density bumps a tier?)
- Override conditions ("upgrade to opus on retry", "downgrade to haiku if AC count is all file-edits")
- When-to-recon rules
- Vendor capability table
- Diversity quota
- Daily/weekly budget caps

**Deterministic code holds mechanism (stable, tested, changes via PR):**

- Spec parsing (reuses `.deia/hive/scripts/queue/spec_parser.py`)
- Token estimation (bytes × char-to-token ratio)
- Historical stats lookup (query a pre-computed aggregate, not live)
- Gate0 validation (already exists)
- Nightly roll-up of completed tasks into per-archetype-per-model aggregates
- JSON contract between skill and helper

### Proposed file layout

```
.claude/skills/
  pick-bee.md                        # the skill — policy + procedure

_tools/
  pick_bee.py                        # deterministic helper invoked by the skill
  pick_bee_stats.py                  # nightly roll-up: /build/status -> aggregates JSON

.deia/stats/
  model_performance.json             # per-archetype-per-model aggregates, refreshed nightly

docs/templates/
  briefing-digest.md                 # digest format template
```

### Skill contract (what the slash-command does)

Invoked as `/pick-bee <spec-path>`. Procedure:

1. Read the spec file.
2. Call `_tools/pick_bee.py <spec-path>` which returns JSON.
3. JSON contains: archetype, estimated_input_tokens, ir_density, should_recon (bool), recommendation{model, confidence, reasoning, expected_cost_usd, expected_duration_s}, alternatives[], override_conditions[].
4. Present in a readable table.
5. Apply skill-level overrides from natural-language rules (e.g. "if retry_count >= 1, upgrade one tier").
6. Ask Q33NR: accept / override / abort.

### Open questions for Mr. AI

1. **Skill vs code boundary.** Is our split clean? Are there business rules we've accidentally put on the code side, or mechanism we've leaked into the skill?
2. **Taxonomy.** Is 8 archetypes (research / implement / hygiene / port / audit / debug / design / bulk) the right granularity? Too coarse? Too fine?
3. **Cold-start problem.** With zero historical data, the skill falls back to priors. What priors? Just the folk-wisdom table? Or a published benchmark (SWE-bench, AIDER, LMSYS) mapped to our archetypes?
4. **Override friction.** Every dispatch asking "accept or override?" will become annoying. When should the skill auto-proceed vs. require confirmation? Threshold: confidence >= 0.8 auto-proceeds?
5. **Drift detection.** If a model's real cost/success starts diverging from its historical average (new model version, prompt injection issue), how does the skill notice and down-weight?
6. **Multi-objective trade-off.** We'd love cheapest-AND-best-AND-fastest, but those conflict. Who weights them? Skill asks Q33NR? Or Q88N sets a weekly "mode" (cost-saver, quality, speed)?
7. **Feedback loop latency.** Nightly roll-up is slow. A bad model choice runs many specs before the aggregate notices. Should we also have a real-time alert if N consecutive failures with model X?

---

## How the Two Ideas Connect

The skill's recommendation is not just "which model" — it's "which **strategy**":

- Strategy A: single bee, model X
- Strategy B: recon (model X) + swarm (model Y × N)
- Strategy C: split into smaller specs first (meta-spec)

The decision between A / B / C is itself a skill-level rule:

```
if estimated_tokens > 100k and planned_bee_count >= 3:
    prefer Strategy B (recon-then-swarm)
elif spec.ambiguity_score > threshold:
    prefer Strategy C (split first)
else:
    Strategy A
```

The recon model and swarm model are chosen separately — recon optimizes for context + synthesis, swarm optimizes for task-fit + cost.

---

## Proposed Sequencing

Three specs if we go forward, in order:

1. **SPEC-PICKBEE-001 (research, sonnet)** — Design the archetype taxonomy, outcome-label schema, digest template format, and the JSON contract between `pick_bee.py` and the skill. No code. Output is a design doc.
2. **SPEC-PICKBEE-002 (implementation, sonnet)** — Add `## Archetype` parsing to spec parser. Capture estimated-input-tokens at dispatch. Extract outcome labels from bee response files. Build `pick_bee_stats.py` nightly roll-up. Backfill from the existing ~976 completed tasks.
3. **SPEC-PICKBEE-003 (implementation, sonnet + haiku mix)** — Write `.claude/skills/pick-bee.md` and `_tools/pick_bee.py`. Ship with deterministic recommendation + natural-language override rules. Dogfood on the next 10 specs. Compare predicted vs actual cost/duration/success.

Recon-then-swarm is a separate sequence:

4. **SPEC-RECON-001 (research, sonnet)** — Design the Briefing Digest format, staleness/invalidation rules, validation pass, fallback paths. Output is a design doc + the digest template.
5. **SPEC-RECON-002 (implementation, sonnet)** — Wire the recon step into dispatch flow (`run_queue.py`). A spec can declare `## Recon Required: true` or the pick-bee skill can inject it. Digest file conventions + path resolution from spec files.
6. **SPEC-RECON-003 (integration, sonnet)** — Merge the recon decision into the pick-bee skill so Strategy A/B/C picking is unified.

Total: 6 specs. Low risk individually. We can stop at any checkpoint.

---

## The Meta-Point for Mr. AI

The fundamental bet here is that **factory economics improve dramatically when we stop treating every bee as stateless and independent**. A shared digest + a policy-driven picker turns the swarm from a flat pool into a tiered pipeline: scouts read widely, workers act narrowly, decisions are auditable.

The risk is complexity. Every abstraction we add (digest format, archetype taxonomy, stats pipeline) is one more thing that can break or go stale. We want Mr. AI's read on:

- Is this over-engineered for current scale (~1k specs/month, one human sovereign)?
- Are there simpler heuristics that get 80% of the value?
- Is there a known prior-art pattern from multi-agent systems literature we should borrow instead of inventing?
- What's the failure mode we're not seeing?

---

**End of proposal.**
