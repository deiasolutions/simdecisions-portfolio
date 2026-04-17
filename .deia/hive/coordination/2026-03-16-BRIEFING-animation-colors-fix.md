# BRIEFING: Fix Hardcoded Colors in 6 Animation Components

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P0.70
**Model Assignment:** Haiku

---

## Objective

Replace all hardcoded color values in 6 animation components with CSS variables (`var(--sd-*)`).

---

## Context

**Hard Rule #3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors. Everything.

The spec identifies 6 animation components that currently violate this rule. All hardcoded colors must be replaced with CSS variables.

---

## Scope

**Components to fix:** (6 total)
- Identify the 6 animation components that have hardcoded colors
- Replace all hex, rgb(), or named color values with appropriate `var(--sd-*)` variables

---

## Acceptance Criteria

From the spec:
- [ ] All 6 animation components use CSS variables only
- [ ] No hardcoded hex, rgb(), or named colors remain
- [ ] All animation tests pass
- [ ] All browser tests pass

---

## Investigation Required

Q33N, you need to:

1. **Find the 6 animation components** that have hardcoded colors
   - Search in `browser/src/` for animation-related files
   - Look for hardcoded hex (`#...`), rgb/rgba values, or named colors (red, blue, etc.)

2. **Identify which CSS variables to use**
   - Check existing CSS variable definitions (likely in a theme or root CSS file)
   - Map each hardcoded color to the appropriate `var(--sd-*)` variable

3. **Verify test coverage**
   - Check if animation tests exist
   - Ensure tests will catch color regressions

---

## Task File Requirements

Write ONE task file for the bee (Haiku model):

**TASK-148:** Fix hardcoded colors in 6 animation components
- List ALL 6 components with absolute file paths
- For each component, list the specific hardcoded colors to replace
- Specify which `var(--sd-*)` variable to use for each replacement
- Test requirements: run all animation tests + all browser tests
- Deliverable: All tests pass, zero hardcoded colors remain

---

## Constraints

- **Model:** Haiku (fast, cost-effective for mechanical replacements)
- **TDD:** If tests don't exist, write them first
- **No file over 500 lines**
- **No stubs**
- **Response file:** All 8 sections mandatory

---

## File Paths to Investigate

- `browser/src/` (animation components likely here)
- `browser/src/shell/components/` (check for animation-related components)
- `browser/src/primitives/` (may have animation primitives)
- CSS variable definitions (look for theme files, root CSS)

---

## Next Steps

1. Investigate the codebase to find the 6 animation components
2. Write the task file with precise file paths and color mappings
3. Return to Q33NR for review before dispatching the bee

---

**Q33N:** Do NOT dispatch the bee yet. Write the task file and return it to Q33NR for approval first.
