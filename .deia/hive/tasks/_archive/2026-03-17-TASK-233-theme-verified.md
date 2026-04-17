# TASK-233: Theme Verified — All CSS Variables Working

## Objective
Audit and fix the theme system. Add missing CSS variables to all 5 themes, replace hardcoded colors with theme variables, and verify all themes render correctly.

## Context
Wave 4 Product Polish (Task 4.5). The theme system in `shell-themes.css` defines 150+ variables across 5 themes (default, depth, light, monochrome, high-contrast). However, some components reference undefined variables and some files contain hardcoded hex/rgb colors.

**Rule 3:** NO HARDCODED COLORS. Only `var(--sd-*)`. No hex, no rgb(), no named colors.

**Rule 4 Violation:** `shell-themes.css` is currently 671 lines (exceeds 500-line limit). This task will add more variables. You MUST flag this in your response file as a follow-up issue.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` (671 lines — theme variable definitions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\bpmn-styles.css` (hardcoded BPMN colors)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\nodes\nodes.css` (references undefined `--sd-blue`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal-errors.css` (references undefined `--sd-yellow`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\GovernanceApprovalModal.css` (fallback colors for undefined vars)

## Deliverables

### 1. Add Missing Variables to ALL 5 Themes
Add these variables to EACH of the 5 theme blocks in `shell-themes.css`:

**Blue variants (for canvas nodes):**
- `--sd-blue`: Main blue (similar to existing cyan but distinct)
- `--sd-blue-dimmest`: Transparent blue for backgrounds
- `--sd-blue-dimmer`: Transparent blue for borders/highlights (optional, if needed)

**Yellow variants (for terminal warnings):**
- `--sd-yellow`: Main yellow (warning color)
- `--sd-yellow-dimmest`: Transparent yellow for backgrounds

**Governance/UI variants:**
- `--sd-accent-warning`: Orange/yellow warning accent
- `--sd-accent-success`: Green success accent
- `--sd-accent-success-hover`: Darker green for hover
- `--sd-bg-tertiary`: Third background level (between surface and bg-secondary)
- `--sd-border-color`: Generic border color (if not already defined)

**Color mappings per theme:**

**Default theme (dark purple):**
- `--sd-blue`: `#3b82f6` (blue-500)
- `--sd-blue-dimmest`: `rgba(59, 130, 246, 0.08)`
- `--sd-yellow`: `#eab308` (yellow-500)
- `--sd-yellow-dimmest`: `rgba(234, 179, 8, 0.08)`
- `--sd-accent-warning`: `#f59e0b` (already exists as --sd-orange, can alias)
- `--sd-accent-success`: `#22c55e` (already exists as --sd-green, can alias)
- `--sd-accent-success-hover`: `#16a34a` (already exists as --sd-green-dark, can alias)
- `--sd-bg-tertiary`: `rgba(26, 20, 40, 0.5)`
- `--sd-border-color`: Same as existing `--sd-border` or define separately

**Depth theme (chromatic depth):**
- `--sd-blue`: `#6889b4` (matches mode-simulate)
- `--sd-blue-dimmest`: `rgba(104, 137, 180, 0.08)`
- `--sd-yellow`: `#c28308` (gold tone matching purple-hover)
- `--sd-yellow-dimmest`: `rgba(194, 131, 8, 0.08)`
- `--sd-accent-warning`: Use existing orange
- `--sd-accent-success`: Use existing green
- `--sd-accent-success-hover`: Use existing green-dark
- `--sd-bg-tertiary`: `rgba(20, 24, 32, 0.5)`
- `--sd-border-color`: Same as --sd-border

**Light theme:**
- `--sd-blue`: `#2563eb` (blue-600, darker for contrast)
- `--sd-blue-dimmest`: `rgba(37, 99, 235, 0.05)`
- `--sd-yellow`: `#ca8a04` (yellow-600)
- `--sd-yellow-dimmest`: `rgba(202, 138, 4, 0.05)`
- `--sd-accent-warning`: Use existing orange
- `--sd-accent-success`: Use existing green
- `--sd-accent-success-hover`: Use existing green-dark
- `--sd-bg-tertiary`: `rgba(245, 243, 255, 0.6)`
- `--sd-border-color`: Same as --sd-border

**Monochrome:**
- `--sd-blue`: `#bbbbbb` (same as cyan)
- `--sd-blue-dimmest`: `rgba(187, 187, 187, 0.08)`
- `--sd-yellow`: `#999999` (same as orange)
- `--sd-yellow-dimmest`: `rgba(153, 153, 153, 0.08)`
- `--sd-accent-warning`: Use existing orange
- `--sd-accent-success`: Use existing green
- `--sd-accent-success-hover`: Use existing green-dark
- `--sd-bg-tertiary`: `rgba(30, 30, 30, 0.5)`
- `--sd-border-color`: Same as --sd-border

**High-contrast:**
- `--sd-blue`: `#44aaff` (bright blue for accessibility)
- `--sd-blue-dimmest`: `rgba(68, 170, 255, 0.1)`
- `--sd-yellow`: `#ffff00` (bright yellow, matches purple)
- `--sd-yellow-dimmest`: `rgba(255, 255, 0, 0.1)`
- `--sd-accent-warning`: `#ff8800` (existing orange)
- `--sd-accent-success`: `#00ff88` (existing green)
- `--sd-accent-success-hover`: `#00ff44` (brighter green)
- `--sd-bg-tertiary`: `rgba(10, 5, 20, 0.6)`
- `--sd-border-color`: Same as --sd-border

### 2. Replace Hardcoded Colors in `bpmn-styles.css`

Replace the `:root` block (lines 7-28) with theme-aware variables:

```css
:root {
  /* BPMN Standard Colors — using theme variables */
  --bpmn-event-start: var(--sd-green);
  --bpmn-event-end: var(--sd-red);
  --bpmn-task-bg: var(--sd-blue);
  --bpmn-task-border: var(--sd-blue);
  --bpmn-gateway-bg: var(--sd-yellow);
  --bpmn-gateway-border: var(--sd-yellow);
  --bpmn-subprocess-bg: var(--sd-blue-dimmest);
  --bpmn-subprocess-border: var(--sd-blue);
  --bpmn-event-intermediate: var(--sd-orange);

  /* Typography */
  --bpmn-label-color: var(--sd-text-primary);
  --bpmn-label-font: var(--sd-font-sm) var(--sd-font-sans);

  /* Sizing */
  --bpmn-event-size: 36px;
  --bpmn-task-height: 60px;
  --bpmn-task-width: 120px;
  --bpmn-gateway-size: 48px;
}
```

Also replace:
- Line 42: `filter: drop-shadow(0 0 8px rgba(66, 165, 245, 0.8));` → `filter: drop-shadow(0 0 8px var(--sd-blue));`
- Line 50: `border: 2px solid #1e88e5;` → `border: 2px solid var(--sd-blue);`

### 3. Remove Fallback Hex Values from `GovernanceApprovalModal.css`

Once the variables are defined in all themes, remove the fallback hex values:

- Line 57: `border-left: 3px solid var(--sd-accent-warning, #ffa500);` → `border-left: 3px solid var(--sd-accent-warning);`
- Line 93: `background-color: var(--sd-accent-success, #2ecc71);` → `background-color: var(--sd-accent-success);`
- Line 98: `background-color: var(--sd-accent-success-hover, #27ae60);` → `background-color: var(--sd-accent-success-hover);`
- Line 108: `background-color: var(--sd-bg-tertiary, #f0f0f0);` → `background-color: var(--sd-bg-tertiary);`
- Line 110: `border: 1px solid var(--sd-border-color, #d0d0d0);` → `border: 1px solid var(--sd-border-color);`

Also fix other fallbacks if found (lines 12, 20-24, 42-45, 56, etc.)

### 4. Grep for Remaining Hardcoded Colors

Run this command to find remaining hardcoded colors in component CSS:

```bash
cd browser/src && grep -rn --include="*.css" -E "#[0-9a-fA-F]{3,6}|rgb\(|rgba\(" . | grep -v "shell-themes.css" | grep -v "node_modules"
```

Fix any remaining hardcoded colors found in component CSS files. DO NOT touch:
- `shell-themes.css` (it's the theme definition file, hardcoded colors are OK there)
- Anything in `node_modules`
- HTML files, JS files, or test files (only CSS files)

### 5. Visual Verification Checklist

After making changes, manually test each theme (switch via the theme selector in the app):

- [ ] **Default theme:** Check text-pane, terminal, canvas nodes, governance modal — no invisible text, no missing borders
- [ ] **Depth theme:** Same checks
- [ ] **Light theme:** Same checks, verify contrast on light background
- [ ] **Monochrome:** Verify all elements visible with grayscale palette
- [ ] **High-contrast:** Verify bright colors render correctly, no low-contrast text

Record any issues found in the "Issues / Follow-ups" section of your response.

### 6. Run Tests

```bash
cd browser && npx vitest run
```

All existing tests must pass. This is a CSS-only change, so test failures are unlikely, but verify no regressions.

## Test Requirements

- [ ] TDD not required (pure CSS task per Rule 5)
- [ ] All existing browser tests pass
- [ ] Visual verification completed for all 5 themes (documented in response file)
- [ ] No hardcoded colors remain in component CSS files (per grep results)

## Acceptance Criteria

- [ ] Missing variables added to ALL 5 themes in `shell-themes.css`
- [ ] `bpmn-styles.css` uses `var(--sd-*)` only (no hardcoded hex/rgb)
- [ ] `GovernanceApprovalModal.css` has no fallback hex values
- [ ] Grep search shows no remaining hardcoded colors in component CSS
- [ ] All 5 themes render correctly (visual verification documented)
- [ ] All browser tests pass
- [ ] Response file documents Rule 4 violation (shell-themes.css over 500 lines)

## Constraints

- **Rule 3:** NO HARDCODED COLORS in component CSS. Only `var(--sd-*)`. Hardcoded colors ARE allowed in `shell-themes.css` (theme definition file).
- **Rule 4:** `shell-themes.css` is already 671 lines (over 500-line limit). Adding variables will make it worse. You MUST flag this in your response file as a follow-up issue requiring modularization.
- **Rule 5:** TDD not required for pure CSS tasks.
- **Rule 6:** NO STUBS. All variables must be defined in all 5 themes.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-233-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

**CRITICAL:** You MUST include in section 8:
- "shell-themes.css is now XXX lines (exceeds 500-line limit per Rule 4). Recommend modularization: split into shell-themes-base.css + shell-themes-[default/depth/light/monochrome/high-contrast].css"
- Any visual issues found during theme testing
- Any remaining hardcoded colors that couldn't be removed (with justification)

DO NOT skip any section.
