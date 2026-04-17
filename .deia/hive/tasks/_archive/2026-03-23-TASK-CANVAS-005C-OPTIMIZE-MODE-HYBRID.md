# TASK-CANVAS-005C: Build Hybrid Optimize Mode (Suggestions + Sweep/Pareto)

**Priority:** HIGH
**Model:** sonnet
**Role:** bee
**Date:** 2026-03-23

## Context

This task builds the full Optimize Mode for the canvas flow designer. The mode has TWO tabs:
1. **Suggestions Tab** — AI-driven analysis of execution ledger data → actionable suggestions
2. **Sweep Tab** — Parameter sweep + Pareto frontier visualization

The old platform had suggestion-based optimization in `OptimizeView.tsx`. The backend has full sweep + Pareto infrastructure in `sweep.py` and `pareto.py` that was never wired to UI. We're building both.

## Part 1: Backend — Port Sweep + Pareto Modules

### 1A. Port sweep.py to engine/des/sweep.py
- Source: `platform/efemera/src/efemera/des/sweep.py` (543 lines)
- Target: `engine/des/sweep.py`
- Classes: `SweepParameter`, `SweepConfig`, `SweepPoint`, `SweepResults`
- Functions: `parameter_sweep(flow, config)`, `sensitivity_analysis()`
- Metric extraction: throughput, cycle_time, completions, utilization
- CI computation per sweep point

### 1B. Port pareto.py to engine/optimization/pareto.py
- Source: `platform/efemera/src/efemera/optimization/pareto.py` (967 lines)
- Target: `engine/optimization/pareto.py`
- Classes: `ParetoSolution`, `ParetoFrontier`, `DominanceChecker`, `ParetoSolver`
- Methods: `select_by_weights()`, `select_where()`, `get_knee_point()`
- Analysis: `spread()`, `hypervolume()`, `spacing()`, `trade_off_ratio()`

### 1C. Add API Routes
Add to `hivenode/routes/des_routes.py` (or new `hivenode/routes/optimize_routes.py`):

```
POST /api/des/sweep       — Run parameter sweep
  Body: { flow: Flow, config: SweepConfig }
  Returns: SweepResults

POST /api/des/pareto      — Compute Pareto frontier from sweep results
  Body: { points: SweepPoint[], objectives: string[] }
  Returns: ParetoFrontier

POST /api/des/optimize     — Run AI suggestion analysis on execution ledger
  Body: { flow: Flow, ledger: LedgerEntry[], constraints: OptConstraints }
  Returns: { suggestions: Suggestion[] }
```

Register routes in `hivenode/routes/__init__.py`.

## Part 2: Frontend — OptimizeMode Component

### 2A. Port OptimizationEngine (Client-side Suggestion Logic)
- Source: `platform/simdecisions-2/src/services/optimization/optimizer.ts` (~400 lines)
- Target: `browser/src/apps/sim/components/flow-designer/modes/OptimizationEngine.ts`
- Suggestion types: replace_operator, reduce_tier, parallelize, remove, add_retry, merge, reorder, cache
- Each suggestion has: type, description, targetNode, impact (clock, cost, carbon, quality, confidence)
- Engine analyzes ledger entries and generates suggestions

### 2B. Create OptimizeMode.tsx
- Path: `browser/src/apps/sim/components/flow-designer/modes/OptimizeMode.tsx`
- Two-tab layout:
  - **Tab 1: "Suggestions"** — Constraints panel + suggestion cards + entity profiles table
  - **Tab 2: "Sweep"** — Parameter range config + Pareto chart + results table

#### Suggestions Tab UI:
- Constraints panel: max clock, max cost, max carbon, min quality (number inputs)
- "Analyze" button → runs OptimizationEngine on ledger data
- Suggestion cards: icon by type, description, impact display (clock: -3.2s, cost: -$0.50, etc.)
- Apply/Dismiss buttons per suggestion
- Entity profiles table: reliability, autonomy, quality per operator

#### Sweep Tab UI:
- Parameter config panel: name, path, min, max, step (add/remove parameters)
- "Run Sweep" button → POST /api/des/sweep
- Pareto scatter chart (use Recharts or SVG): X/Y axis objectives, non-dominated highlighted
- Results table: sweep points with CIs, sortable columns
- "Apply Config" button → applies selected optimal config to flow

### 2C. Wire into FlowDesigner
- Add "Optimize" to mode menu in FlowDesigner.tsx (alongside Design, Configure, Simulate, etc.)
- Import and render OptimizeMode when mode === "optimize"
- Bus events: `optimize:suggestion-apply`, `optimize:config-selected`, `optimize:sweep-run`

### 2D. Update canvas.egg.md
- Add optimize mode pane definitions if needed

## Part 3: Tests (TDD)

Write tests FIRST for each component:

### Backend Tests:
- [ ] Sweep: parameter_sweep with 2 params × 3 values = 6 points
- [ ] Sweep: sensitivity_analysis returns elasticity values
- [ ] Pareto: 2-objective frontier correctly identifies dominated points
- [ ] Pareto: knee point selection works
- [ ] API: POST /api/des/sweep returns SweepResults
- [ ] API: POST /api/des/pareto returns ParetoFrontier
- [ ] API: POST /api/des/optimize returns suggestions

### Frontend Tests:
- [ ] OptimizationEngine generates suggestions from mock ledger
- [ ] Suggestions tab renders constraint inputs
- [ ] Suggestions tab displays suggestion cards with impacts
- [ ] Apply suggestion fires bus event
- [ ] Sweep tab renders parameter config inputs
- [ ] Sweep tab displays results table after sweep completes
- [ ] Pareto chart highlights non-dominated points
- [ ] Mode switching to/from optimize works
- [ ] Edge: empty ledger → "No data" message
- [ ] Edge: no parameters defined → error message
- [ ] Edge: sweep timeout → error display

## Rules

- All CSS: `var(--sd-*)` only. No hex, no rgb(), no named colors.
- Files: 500 lines max.
- TDD: tests first.
- No stubs.
- Follow the pane adapter pattern from CANVAS-000 if adding shell panes.

## Files to Read First

1. `.deia/BOOT.md` — hard rules
2. `browser/src/apps/sim/components/flow-designer/modes/ConfigureMode.tsx` — pattern for mode components (Wave 2 delivery)
3. `hivenode/routes/des_routes.py` — existing DES API routes
4. `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` — mode switching logic
5. `platform/simdecisions-2/src/services/optimization/optimizer.ts` — old OptimizationEngine
6. `platform/efemera/src/efemera/des/sweep.py` — sweep module to port
7. `platform/efemera/src/efemera/optimization/pareto.py` — pareto module to port
8. `platform/simdecisions-2/src/components/mode-views/OptimizeView.tsx` — old UI reference

## Response Template

Use the standard 8-section DEIA response template from BOOT.md.
