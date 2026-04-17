# BRIEFING: IR Density Measurement for Hive Specs and Tasks

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Priority:** P1

## Context

We have a spec on file — `SPEC-IR-DENSITY-001` — that defines IR Density as "IR primitives generated per tokens consumed" for PHASE-IR conversations. The concept is sound but has never been operationalized. Meanwhile, we're generating 60+ spec files and task files through the hive pipeline, and we have no way to measure how much actionable instruction each one contains relative to its size.

We also have:
- **Gate 0** (`gate0.py`) — validates spec format (priority, acceptance criteria, file paths, scope) but doesn't score density
- **Fidelity scoring** (`ledger_events.py`) — records 0.0–1.0 fidelity per phase, but doesn't measure what *makes* a spec produce high fidelity
- **Estimation calibration ledger** (EST-01 through EST-04, in pipeline) — tracks Clock/Cost/Carbon per task, will soon have actuals vs estimates

The missing piece: **what structural properties of a spec predict build success, cost efficiency, and fidelity?** That's what IR density measurement would answer.

## What IR Density Means in the Hive

Adapted from SPEC-IR-DENSITY-001 for our build pipeline:

**IR Density** = actionable instruction tokens / total spec tokens

A "high density" spec packs more executable instructions (acceptance criteria, file paths, code snippets, smoke tests, CLI commands) per line. A "low density" spec has more narrative, context, repetition, and ambiguity.

### Proposed Sub-Metrics (4)

1. **Instruction Density** — `(acceptance_criteria_count + deliverable_count + smoke_test_count) / total_lines`
   - How many checkboxes, commands, and concrete deliverables per line of spec?
   - High = dense, actionable. Low = verbose, ambiguous.

2. **Reference Density** — `(file_path_refs + code_block_lines + schema_lines) / total_lines`
   - How much concrete code, schema, and file paths vs prose?
   - Bees work faster when they can copy-paste rather than interpret.

3. **Constraint Clarity** — `constraint_sections_present / expected_sections`
   - Does the spec have Priority, Depends On, Model Assignment, Acceptance Criteria, Smoke Test, Constraints, Response Requirements?
   - Missing sections = ambiguity = wasted tokens in the build.

4. **IR Cost Efficiency** — `fidelity_score / actual_cost_usd`
   - How much fidelity per dollar spent?
   - Computed post-build, using calibration ledger actuals.

### Composite Score

```
ir_density = (
    0.30 * instruction_density +
    0.25 * reference_density +
    0.25 * constraint_clarity +
    0.20 * ir_cost_efficiency    # only when actuals available
)
```

Score range: 0.0 – 1.0. Weights are initial — calibrate from actuals.

## Data Sources

All exist today:
- **Spec files** in `backlog/`, `queue/`, `_active/`, `_done/` — parse sections, count checkboxes, code blocks, file paths
- **Gate 0 results** — `gate0.py` already validates structure, just doesn't score it
- **Fidelity scores** — `ledger_events.py` records per-phase fidelity
- **Calibration ledger** — `inv_estimates` will have actual_cost_usd, actual_hours per task (EST-02 populates this)
- **Response files** — Clock/Cost/Carbon sections, success/failure, healing attempts

## What We'd Build

### Phase 1: Static Spec Analyzer (no LLM calls)

A new CLI tool: `_tools/ir_density.py`

```bash
# Score a single spec
python _tools/ir_density.py score .deia/hive/queue/backlog/SPEC-MW-011-mobile-nav-hub.md
# Output: IR Density: 0.72 (instruction: 0.81, reference: 0.68, clarity: 0.86, efficiency: N/A)

# Score all specs in a directory
python _tools/ir_density.py batch .deia/hive/queue/backlog/
# Output: table of all specs, sorted by density, flagging low-density specs

# Compare density vs build outcomes (requires calibration ledger data)
python _tools/ir_density.py correlate
# Output: correlation between IR density and (cost delta %, fidelity, healing attempts)

# Gate 0 integration: add density check to validation pipeline
python _tools/ir_density.py gate-check SPEC-MW-011.md --min-density 0.5
# Output: PASS (0.72) or FAIL (0.38) — blocks dispatch if below threshold
```

### Phase 2: Predictive Model

Once we have enough data (30+ tasks with both IR density and actuals from calibration ledger):
- Correlate IR density with cost overruns
- Correlate IR density with fidelity scores
- Correlate IR density with healing attempts
- Train a simple regression: `predicted_cost = f(ir_density, task_type, model)`
- Feed predictions back into scheduler estimates

### Phase 3: Spec Improvement Recommendations

- Low instruction density → "Add more acceptance criteria"
- Low reference density → "Add code snippets and file paths"
- Low constraint clarity → "Missing Smoke Test section"
- Automated spec rewriting suggestions (LLM-assisted, Phase 3 only)

## Integration Points

1. **Gate 0** — Add IR density as a 6th check. Warn (not block) if density < 0.4, block if < 0.2.
2. **Calibration Ledger** — New column `ir_density` in `inv_estimates`. Recorded at dispatch time. Correlate with actuals.
3. **Scheduler** — Weight task priority by density: high-density specs dispatch first (less risk of healing loops).
4. **Build Monitor** — Show IR density in task status. Flag low-density active builds.
5. **Morning Report** — Include average IR density of dispatched specs. Track improvement over time.

## Files to Read First

- `docs/specs/PROMPT-BACKLOG-BATCH-INSERT.md` — ITEM 10: SPEC-IR-DENSITY-001 original definition
- `.deia/hive/scripts/queue/gate0.py` — Current Gate 0 validation (5 checks, no density)
- `.deia/hive/scripts/queue/ledger_events.py` — Fidelity event schema (add ir_density field)
- `.deia/hive/scripts/queue/spec_parser.py` — Parses spec files (sections, fields)
- `.deia/hive/scripts/queue/spec_validator.py` — Format validation (extend with density)
- `hivenode/inventory/store.py` — inv_estimates schema (add ir_density column)
- `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md` — Calibration ledger design

## Deliverables

This is a DESIGN + PLAN task. The Q33N should:

1. **Validate the 4 sub-metrics** — Are they measurable from existing spec files? Parse 5 real specs, compute each metric, verify they produce meaningful differentiation.
2. **Design the scoring algorithm** — Weights, normalization, edge cases (empty sections, very short specs).
3. **Design the CLI** — Commands, output formats, integration with gate0.
4. **Design the inv_estimates integration** — New column, when to record, how to correlate.
5. **Create task files** for bee dispatch (3-4 tasks):
   - Task 1: Static analyzer + CLI (`_tools/ir_density.py`) — score individual specs
   - Task 2: Batch scoring + Gate 0 integration — score all specs, add density check
   - Task 3: Calibration ledger integration — ir_density column, correlate with actuals
   - Task 4: Morning report integration + dashboard (optional, lower priority)

## Constraints

- No LLM calls in Phase 1 (pure static analysis)
- No file over 500 lines
- TDD where applicable
- Must work on existing spec format (not require spec rewrites)
- Must produce meaningful scores on our real specs (validate on 5+ existing specs before finalizing weights)
- CLI via `_tools/ir_density.py` (new file, match `inventory.py` pattern)

## Open Questions for Q33N

1. Should the composite score weight `ir_cost_efficiency` at all in Phase 1? (We won't have actuals until calibration ledger is populated.) Recommendation: set weight to 0 until data exists, redistribute to other 3.
2. Should Gate 0 density check block dispatch or just warn? Recommendation: warn initially, block after calibrating threshold from real data.
3. Should we score TASK files as well as SPEC files? They have the same sections. Recommendation: yes, both.
