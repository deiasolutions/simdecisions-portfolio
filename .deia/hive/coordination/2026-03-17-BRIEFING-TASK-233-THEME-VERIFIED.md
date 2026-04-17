# BRIEFING: TASK-233 Theme Verified

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-17
**Spec Source:** `.deia/hive/queue/2026-03-16-SPEC-TASK-233-theme-verified.md`
**Priority:** P1
**Model:** Sonnet

---

## Objective

Audit and fix the theme system. All components must use CSS variables from `shell-themes.css`. No hardcoded colors allowed (Rule 3).

---

## What Q88N Wants

Wave 4 Product Polish — Task 4.5. The theme system defines 150+ variables across 5 themes, but:
1. Some components reference **undefined variables** (e.g., `--sd-blue`, `--sd-yellow`)
2. Some files contain **hardcoded hex/rgb colors** (violates Rule 3)
3. Theme switching may cause invisible text or broken contrast

This must be fixed before alpha launch.

---

## Context

### Current Theme System

- **Theme file:** `browser/src/shell/shell-themes.css` (671 lines)
- **5 themes:** default, depth, light, monochrome, high-contrast
- **150+ variables** already defined

### Problem Files (from spec)

1. **`browser/src/primitives/canvas/bpmn-styles.css`**
   - Contains hardcoded BPMN colors
   - Needs mapping to theme variables

2. **`browser/src/primitives/canvas/nodes/nodes.css`**
   - References undefined `--sd-blue`, `--sd-blue-dimmest`

3. **`browser/src/primitives/terminal/terminal-errors.css`**
   - References undefined `--sd-yellow`, `--sd-yellow-dimmest`

4. **`browser/src/shell/components/GovernanceApprovalModal.css`**
   - Has fallback colors for undefined vars: `--sd-accent-warning`, `--sd-accent-success`, `--sd-accent-success-hover`, `--sd-bg-tertiary`, `--sd-border-color`

### Missing Variables (must be added to ALL 5 themes)

- `--sd-blue`, `--sd-blue-dimmest`
- `--sd-yellow`, `--sd-yellow-dimmest`
- `--sd-accent-warning`, `--sd-accent-success`, `--sd-accent-success-hover`
- `--sd-bg-tertiary`, `--sd-border-color`

---

## Deliverables (from spec)

1. Add missing variables to ALL 5 themes in `shell-themes.css`
2. Replace hardcoded colors in `bpmn-styles.css` with theme variables
3. Remove fallback hex values from `GovernanceApprovalModal.css`
4. Grep entire `browser/src/` for remaining hardcoded colors and fix
5. Verify each theme renders correctly (no invisible text, missing borders, broken contrast)
6. Run: `cd browser && npx vitest run`

---

## Your Task (Q33N)

1. **Read the files listed in the spec** (shell-themes.css, bpmn-styles.css, nodes.css, terminal-errors.css, GovernanceApprovalModal.css)
2. **Write ONE task file** for a bee to execute this work
   - This is a pure CSS task — no TDD required (Rule 5 exception)
   - But DO require visual verification across all 5 themes
3. **Task file must include:**
   - Exact variable names to add to each theme
   - Color mappings for BPMN elements (start → green, end → red, tasks → blue, gateways → yellow)
   - Grep command to find remaining hardcoded colors
   - Visual verification checklist (switch themes, check for issues)
4. **Return the task file to me (Q33NR) for review** before dispatching

---

## Constraints

- **Rule 3:** NO HARDCODED COLORS. Only `var(--sd-*)`. No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. `shell-themes.css` is 671 lines — already over limit. If adding variables pushes it higher, flag it.
- **Rule 5:** TDD not required for pure CSS tasks.
- **Rule 6:** NO STUBS. Every variable must be defined in all 5 themes.

---

## Model Assignment

**Sonnet** — This requires careful mapping of semantic meaning (warning → yellow, success → green) and visual verification across 5 themes.

---

## Next Steps

1. Q33N writes task file
2. Q33N returns to Q33NR for review
3. Q33NR approves (or requests corrections)
4. Q33N dispatches bee (Sonnet)
5. Bee completes, writes response file
6. Q33N reviews response, reports to Q33NR
7. Q33NR reports to Q88N

---

**Do NOT dispatch bees yet. Return the task file to me first.**
