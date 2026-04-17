# TASK-CANVAS-005: Port Optimize Mode -- **FAILED (SPEC CLARIFICATION REQUIRED)**

**Status:** FAILED (task spec inaccurate, user input needed)
**Model:** Sonnet
**Date:** 2026-03-23

## Files Modified
(none — no code written pending spec clarification)

## What Was Done
1. Read old platform OptimizeView (`simdecisions-2/src/components/mode-views/OptimizeView.tsx`, 479 lines)
2. Read backend optimization modules:
   - `efemera/src/efemera/optimization/pareto.py` (967 lines) — Pareto frontier solver
   - `efemera/src/efemera/des/sweep.py` (543 lines) — parameter sweep & sensitivity analysis
   - `simdecisions-2/src/services/optimization/types.ts` (84 lines) — frontend optimization types
3. Analyzed `hivenode/routes/des_routes.py` (277 lines) — existing DES backend API
4. Read comparison report line 43 — "Parameter sweep controls, Pareto frontier viz, optimization engine"

## Critical Finding: TASK SPEC IS INACCURATE

The task brief states:
> "OptimizeMode allows users to: 1. Define parameter ranges for sweep (e.g., arrival rate 1-10, service time 5-15) 2. Run multi-variate optimization (explore parameter space) 3. Visualize Pareto frontier (trade-off curves) 4. Select optimal configurations"

**REALITY:** The old platform's `OptimizeView` does **NOT** do parameter sweeps or Pareto frontiers. It does **AI-driven suggestion-based optimization**:

### What OptimizeView Actually Does (Old Platform)
- **Purpose:** Analyze execution ledger data and suggest improvements to existing flows
- **UI Components:**
  1. Constraints panel (max clock/cost/carbon, min quality)
  2. "Analyze" button (runs OptimizationEngine on ledger data)
  3. Suggestion cards (e.g., "Reduce tier 4 → tier 2", "Replace LLM with auto", "Add retry logic")
  4. Impact display (clock: -3.2s, cost: -$0.50, carbon: -12gCO2e, confidence: 85%)
  5. Entity profiles table (reliability, autonomy, quality scores per operator)
  6. Apply/Dismiss buttons per suggestion
- **Backend:** Client-side `OptimizationEngine` class (`services/optimization/optimizer.ts`) — NO backend API
- **Data Source:** `useExecutionStore().ledgerEntries` (execution history from previous runs)
- **Suggestion Types:** `replace_operator`, `reduce_tier`, `parallelize`, `remove`, `add_retry`, `merge`, `reorder`, `cache`
- **NO parameter sweeps, NO Pareto frontier viz**

### What Exists in Backend (NEVER WIRED TO UI)
The old platform backend **DOES** have full parameter sweep + Pareto infrastructure:

#### `efemera/optimization/pareto.py` (967 lines)
- `ParetoSolution`, `ParetoFrontier`, `DominanceChecker`, `ParetoSolver`
- Multi-objective optimization via weighted-sum method
- Frontier selection helpers: `select_by_weights()`, `select_where()`, `get_knee_point()`
- Frontier analysis: `spread()`, `hypervolume()`, `spacing()`, `trade_off_ratio()`
- Frontier viz: `to_table_text()`, `to_trade_off_text()`

#### `efemera/des/sweep.py` (543 lines)
- `SweepParameter`, `SweepConfig`, `SweepPoint`, `SweepResults`
- Full factorial parameter sweep: `parameter_sweep(flow, config)`
- Sensitivity analysis: `sensitivity_analysis()` (OAT elasticity + correlation)
- Metric extraction: `throughput`, `cycle_time`, `completions`, `utilization`
- CI computation per sweep point

#### Frontend Types (`types.ts`)
- `ParetoPoint` type exists (line 48-56) with `clock`, `cost`, `carbon`, `quality`, `isDominated`
- `OptimizationResult.paretoFrontier: ParetoPoint[]` (line 78)
- **BUT:** Old `OptimizationEngine` never computes a Pareto frontier — it just generates `Suggestion[]`

### The Discrepancy
- **Comparison report (line 43)** claims OptimizeView has "parameter sweep controls, Pareto frontier viz"
- **Actual old code:** OptimizeView = suggestion-based only, NO sweep UI, NO Pareto viz
- **Backend capability:** sweep + Pareto code exists, but was NEVER exposed to the UI

## User Decision Required

**Q88NR must clarify which OptimizeMode to build:**

### Option A: Port Old OptimizeView As-Is (Suggestion-Based)
**What:** AI-driven suggestions panel that analyzes execution ledger and recommends node changes
**Scope:**
- Port `OptimizationEngine` from `simdecisions-2/src/services/optimization/optimizer.ts` (~400 lines)
- Port `OptimizeView` UI (constraints, suggestions, entity profiles)
- NO backend API needed (client-side analysis only)
- NO parameter sweeps, NO Pareto charts
**Effort:** Medium (2-3 sessions)
**Value:** Incremental improvement suggestions based on historical execution data

### Option B: Build True Parameter Sweep + Pareto Mode (New Capability)
**What:** Define parameter ranges, run multi-variate sweeps, visualize Pareto frontier
**Scope:**
- NEW backend API routes: `POST /api/des/sweep`, `POST /api/des/pareto`
- Port `sweep.py` + `pareto.py` modules to shiftcenter `engine/` (1,500+ lines backend)
- NEW frontend pane adapters:
  - Parameter sweep config panel (define ranges, factorial vs OAT)
  - Pareto frontier chart (Recharts scatter plot, trade-off curves)
  - Results table (sweep points, CIs, best configs)
- Update `canvas.egg.md` layout for optimize mode panes
**Effort:** Large (5-7 sessions)
**Value:** True multi-objective optimization — explore parameter space, find Pareto-optimal configs

### Option C: Hybrid (Both Features)
**What:** Combine suggestion-based analysis + parameter sweep + Pareto
**Scope:** All of Option A + Option B
**Effort:** Very Large (8-10 sessions)
**Layout:** Optimize mode with TWO tabs: "Suggestions" (ledger analysis) + "Sweep" (parameter exploration)

## Recommendation
**Option B (True Parameter Sweep + Pareto)** is the better long-term investment:
1. **Unique capability:** Suggestion-based optimization is nice-to-have, but parameter sweep + Pareto is a DIFFERENTIATOR. Allows users to systematically explore "what if" scenarios.
2. **Backend exists:** All hard work (sweep.py, pareto.py) is already done. We just need to wire it up.
3. **Aligns with task brief:** Task description explicitly calls for "parameter sweep controls, Pareto frontier viz".
4. **Future-proof:** Once sweep + Pareto infra is ported, we can layer suggestions on top later (Option C becomes easy).

If Q88NR agrees with Option B, next steps:
1. Port `engine/des/sweep.py` + `engine/optimization/pareto.py` to shiftcenter `engine/` (backend modules)
2. Add `POST /api/des/sweep` and `POST /api/des/pareto` to `hivenode/routes/des_routes.py`
3. Create frontend pane adapters: `optimizeParamsPaneAdapter.tsx`, `optimizeResultsPaneAdapter.tsx`
4. Update `canvas.egg.md` with optimize mode layout (params pane left, results pane right)
5. Build Pareto chart component (Recharts scatter plot with frontier highlighting)
6. Wire bus events: `optimize:sweep-run`, `optimize:pareto-computed`, `optimize:config-selected`

## Blockers
- **USER INPUT REQUIRED:** Q88NR must choose Option A, B, or C before work can proceed
- Task spec must be updated to clarify which OptimizeMode variant to build

## Test Plan (Pending Spec Clarification)
### If Option A (Suggestion-Based):
- [ ] OptimizationEngine analyzes ledger → generates suggestions
- [ ] Suggestion cards display impact (clock/cost/carbon)
- [ ] Apply suggestion → updates node in IR
- [ ] Entity profiles table populated from ledger
- [ ] Constraints filter suggestions

### If Option B (Parameter Sweep + Pareto):
- [ ] Sweep config UI: define parameters (name, path, values)
- [ ] POST /api/des/sweep → runs full factorial → returns SweepResults
- [ ] POST /api/des/pareto → computes frontier → returns ParetoFrontier
- [ ] Pareto chart: scatter plot, non-dominated solutions highlighted
- [ ] Results table: sweep points with CIs
- [ ] Select config → applies to flow
- [ ] Edge cases:
  - [ ] Parameter ranges with min > max — validation error
  - [ ] Optimization with 0 parameters — error message "No parameters defined"
  - [ ] Optimization run fails (backend timeout) — show error in UI
  - [ ] Pareto frontier with single objective — degenerates to sorted list (handle gracefully)
  - [ ] Large parameter space (100+ combinations) — show progress bar

## Next Steps
1. Q88NR reviews this response
2. Q88NR selects Option A, B, or C
3. If Option B: Create new task file `TASK-CANVAS-005B-PARETO-SWEEP.md` with updated scope
4. If Option A: Create new task file `TASK-CANVAS-005A-SUGGESTION-OPTIMIZER.md` with updated scope
5. Requeue with clarified spec

## Lessons Learned
- **ALWAYS read old implementation before trusting comparison report** — report line 43 was inaccurate
- **Backend capabilities ≠ UI capabilities** — sweep/Pareto code existed but was never exposed
- When porting "missing" features, verify what was actually missing vs what was just buried in backend
