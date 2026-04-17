# TASK-CANVAS-005C-4: Port OptimizationEngine + Build Suggestions Tab

**Priority:** HIGH
**Model:** sonnet
**Role:** bee
**Date:** 2026-03-24
**Depends on:** CANVAS-005C-3 (API routes) should be complete, but this task is frontend-only and can proceed independently

## What

Port the OptimizationEngine from the old platform and build the Suggestions tab for OptimizeMode.

## Part 1: Port OptimizationEngine

### Source
`platform/simdecisions-2/src/services/optimization/optimizer.ts` (~451 lines)

### Target
`browser/src/apps/sim/components/flow-designer/modes/OptimizationEngine.ts`

### What to Port
- `OptimizationEngine` class: analyzes execution ledger entries and generates suggestions
- Suggestion types: `replace_operator`, `reduce_tier`, `parallelize`, `remove`, `add_retry`, `merge`, `reorder`, `cache`
- Each suggestion: `{ type, description, targetNodeId, impact: { clock, cost, carbon, quality, confidence } }`
- Constraint filtering: max clock, max cost, max carbon, min quality
- Entity profiling: reliability, autonomy, quality scores per operator node

If the source file is over 500 lines, modularize into 2 files (e.g., `OptimizationEngine.ts` + `suggestionGenerators.ts`).

## Part 2: Build Suggestions Tab UI

### Target
`browser/src/apps/sim/components/flow-designer/modes/SuggestionsTab.tsx`

### UI Components
1. **Constraints Panel** — 4 number inputs: max clock (s), max cost ($), max carbon (gCO2e), min quality (0-1)
2. **"Analyze" Button** — runs OptimizationEngine on ledger data
3. **Suggestion Cards** — Each card shows:
   - Icon by suggestion type
   - Description text
   - Impact display: clock: -3.2s, cost: -$0.50, carbon: -12gCO2e, quality: +0.05
   - Confidence percentage
   - "Apply" and "Dismiss" buttons
4. **Entity Profiles Table** — rows per operator node with reliability/autonomy/quality scores
5. **Empty State** — "No suggestions. Run a simulation first to generate execution data."

### Bus Events
- `optimize:suggestion-apply` — when user clicks Apply on a suggestion
- Receives `simulation:ledger-update` — to refresh analysis when new ledger data arrives

## Tests (TDD)

Create `browser/src/apps/sim/components/flow-designer/modes/__tests__/SuggestionsTab.test.tsx`:

1. `test_engine_generates_suggestions_from_ledger` — mock ledger → suggestions array
2. `test_engine_respects_constraints` — high cost constraint filters expensive suggestions
3. `test_engine_empty_ledger_returns_empty` — no ledger → no suggestions
4. `test_engine_entity_profiles` — generates profiles per operator
5. `test_suggestions_tab_renders_constraints` — 4 number inputs present
6. `test_suggestions_tab_analyze_button` — button click triggers analysis
7. `test_suggestions_tab_displays_cards` — suggestion cards render after analysis
8. `test_suggestion_card_impact_display` — clock/cost/carbon values shown
9. `test_suggestion_apply_fires_bus_event` — Apply button fires optimize:suggestion-apply
10. `test_suggestion_dismiss_removes_card` — Dismiss removes suggestion from list
11. `test_entity_profiles_table` — profiles table renders with correct columns
12. `test_empty_state_message` — shows "No suggestions" when no ledger data
13. `test_loading_state` — shows spinner while analyzing
14. `test_suggestion_confidence_display` — confidence percentage shown
15. `test_multiple_suggestions_sorted` — suggestions sorted by total impact

## Rules

- CSS: `var(--sd-*)` only. No hex/rgb/named colors.
- Files: 500 lines max.
- TDD: tests first.
- No stubs.
- Read `.deia/BOOT.md` first.

## Files to Read First

1. `.deia/BOOT.md`
2. `platform/simdecisions-2/src/services/optimization/optimizer.ts` — source
3. `platform/simdecisions-2/src/components/mode-views/OptimizeView.tsx` — old UI reference
4. `browser/src/apps/sim/components/flow-designer/modes/ConfigureMode.tsx` — pattern for mode tabs
