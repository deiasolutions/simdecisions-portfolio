# TASK-CANVAS-005C-5: Build Sweep Tab + Wire OptimizeMode into FlowDesigner

**Priority:** HIGH
**Model:** sonnet
**Role:** bee
**Date:** 2026-03-24
**Depends on:** CANVAS-005C-3 (API routes), CANVAS-005C-4 (SuggestionsTab)

## What

Build the Sweep tab for parameter sweep + Pareto frontier visualization, create the parent OptimizeMode component, and wire it into FlowDesigner.

## Part 1: Sweep Tab

### Target
`browser/src/apps/sim/components/flow-designer/modes/SweepTab.tsx`

### UI Components
1. **Parameter Config Panel** — Add/remove parameter rows. Each row:
   - Name (text input)
   - Path (text input — dot-path to flow parameter)
   - Min value (number)
   - Max value (number)
   - Step count (number, default 5)
2. **"Run Sweep" Button** — POST /api/des/sweep → shows progress spinner
3. **Pareto Scatter Chart** — SVG scatter plot (do NOT use Recharts — keep deps minimal):
   - X axis: first objective, Y axis: second objective
   - Non-dominated points highlighted (larger, different color using `var(--sd-purple)`)
   - Dominated points dimmed (using `var(--sd-text-dim)`)
   - Click point to select configuration
   - Knee point marked with special indicator
4. **Results Table** — Columns: parameter values, objective values (mean), CI low, CI high
   - Sortable by any column
   - Selected row highlighted
5. **"Apply Config" Button** — applies selected configuration to flow

### Bus Events
- `optimize:sweep-run` — when sweep starts
- `optimize:pareto-computed` — when Pareto frontier ready
- `optimize:config-selected` — when user selects a configuration from table/chart

## Part 2: Parent OptimizeMode Component

### Target
`browser/src/apps/sim/components/flow-designer/modes/OptimizeMode.tsx`

### Layout
- Tab bar at top: "Suggestions" | "Sweep"
- Tab content area below
- Renders `<SuggestionsTab>` or `<SweepTab>` based on active tab
- Passes flow, nodes, edges as props

### Target CSS
`browser/src/apps/sim/components/flow-designer/modes/OptimizeMode.css`

## Part 3: Wire into FlowDesigner

### Changes to FlowDesigner.tsx
- Import OptimizeMode
- Add "Optimize" to mode menu (if not already added)
- Render `<OptimizeMode>` when mode === "optimize"
- Check if "optimize" is already in FlowMode union type in types.ts (added by CANVAS-005 attempt)

### Changes to types.ts (if needed)
- Add `"optimize"` to FlowMode union type (if not already present)

## Tests (TDD)

Create `browser/src/apps/sim/components/flow-designer/modes/__tests__/SweepTab.test.tsx`:

1. `test_parameter_config_renders` — add parameter row renders inputs
2. `test_add_parameter` — click "Add" creates new parameter row
3. `test_remove_parameter` — click "Remove" deletes parameter row
4. `test_run_sweep_button` — button fires API call
5. `test_results_table_renders` — results table shows after sweep
6. `test_results_table_sortable` — click column header sorts
7. `test_pareto_chart_renders` — SVG scatter plot renders
8. `test_pareto_non_dominated_highlighted` — non-dominated points visually distinct
9. `test_apply_config_fires_event` — Apply button fires bus event
10. `test_empty_parameters_error` — error message when no params defined
11. `test_sweep_loading_state` — spinner while sweep running
12. `test_sweep_error_display` — error message on API failure

Create `browser/src/apps/sim/components/flow-designer/modes/__tests__/OptimizeMode.test.tsx`:

1. `test_renders_tab_bar` — "Suggestions" and "Sweep" tabs visible
2. `test_default_tab_is_suggestions` — Suggestions tab active by default
3. `test_switch_to_sweep_tab` — clicking Sweep shows SweepTab
4. `test_mode_receives_flow_props` — flow/nodes/edges passed to active tab

## Rules

- CSS: `var(--sd-*)` only.
- Files: 500 lines max.
- TDD: tests first.
- No stubs.
- SVG for Pareto chart (no Recharts dependency).
- Read `.deia/BOOT.md` first.

## Files to Read First

1. `.deia/BOOT.md`
2. `browser/src/apps/sim/components/flow-designer/modes/ConfigureMode.tsx` — mode component pattern
3. `browser/src/apps/sim/components/flow-designer/modes/SuggestionsTab.tsx` — from 005C-4
4. `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` — where to wire mode
5. `browser/src/apps/sim/components/flow-designer/types.ts` — FlowMode type
