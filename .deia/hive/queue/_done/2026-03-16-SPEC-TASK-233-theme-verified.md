# TASK-233: Theme Verified — All CSS Variables Working (W4 — 4.5)

## Objective
Audit the theme system. Define missing CSS variables, replace hardcoded colors with theme variables, verify dark mode looks good across all components.

## Context
Wave 4 Product Polish. The theme system in `shell-themes.css` defines 150+ variables across 5 themes (default, depth, light, monochrome, high-contrast). However, some components reference undefined variables and some files contain hardcoded hex/rgb colors.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.5

## Files to Read First
- `browser/src/shell/shell-themes.css` — Theme variable definitions (671 lines)
- `browser/src/primitives/canvas/bpmn-styles.css` — Hardcoded BPMN colors
- `browser/src/primitives/canvas/nodes/nodes.css` — References undefined `--sd-blue`
- `browser/src/primitives/terminal/terminal-errors.css` — References undefined `--sd-yellow`
- `browser/src/shell/components/GovernanceApprovalModal.css` — Fallback colors for undefined vars

## Deliverables
- [ ] Add missing variables to ALL 5 themes in `shell-themes.css`:
  - `--sd-blue`, `--sd-blue-dimmest` (used by canvas nodes)
  - `--sd-yellow`, `--sd-yellow-dimmest` (used by terminal warnings)
  - `--sd-accent-warning`, `--sd-accent-success`, `--sd-accent-success-hover` (used by governance modal)
  - `--sd-bg-tertiary`, `--sd-border-color` (used by governance modal)
- [ ] Replace hardcoded colors in `bpmn-styles.css`:
  - Map BPMN colors to `--sd-*` variables (start events → green, end → red, tasks → blue, gateways → yellow)
  - Replace `rgba()` shadows with `var(--sd-shadow-*)` or theme-aware values
- [ ] Remove fallback hex values from `GovernanceApprovalModal.css` (they become unnecessary once vars are defined)
- [ ] Grep entire `browser/src/` for remaining hardcoded colors (hex `#xxx`, `rgb(`, named colors) and fix any in component CSS
- [ ] Verify each theme renders correctly: switch themes and check no invisible text, missing borders, or broken contrast
- [ ] Run: `cd browser && npx vitest run`

## Priority
P1

## Model
sonnet
