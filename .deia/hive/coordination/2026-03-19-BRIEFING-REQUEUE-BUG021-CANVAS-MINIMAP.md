# Briefing: BUG-021 Requeue — Canvas Minimap Formatting Broken

**To:** Q33N (Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-19
**Priority:** P1

---

## Objective

Fix the canvas minimap styling to match the platform aesthetic. A previous bee (haiku) claimed to verify this but the issue persists at runtime. The minimap either doesn't exist or has broken styling.

---

## Context

**Background:**
- The canvas minimap has "weird formatting" that doesn't match the platform version
- Previous verification by haiku failed to catch the runtime issue
- The minimap may not exist at all, or may exist but be unstyled

**Problem:**
No minimap component exists in `browser/src/primitives/canvas/controls/` — only ZoomControls. React Flow's built-in `<MiniMap>` component may or may not be imported/used in CanvasApp.tsx.

---

## What Q33N Must Do

1. **Read these files FIRST:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` — check for MiniMap import/usage
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvas.css` — existing canvas styles
   - Platform reference (if accessible): `platform/simdecisions-2/src/components/canvas/` for minimap implementation

2. **Write task file(s) for:**
   - Investigate: Does the minimap exist? Is it imported? Is it styled?
   - If minimap exists but unstyled: port CSS from platform OR style with React Flow's MiniMap props
   - If minimap doesn't exist: add React Flow's `<MiniMap>` component with proper styling
   - Ensure minimap matches platform aesthetic: correct background, node colors, viewport indicator
   - **ALL colors must use CSS variables (var(--sd-*))** — no hex, no rgb(), no named colors (Rule 3)

3. **Task requirements:**
   - Tests for minimap rendering (verify it appears, verify styling)
   - Smoke test: no regressions in canvas tests
   - Response file with all 8 sections

---

## Deliverables (for the bee)

- [ ] Canvas has a working minimap
- [ ] Minimap styling matches platform aesthetic (no white zones, proper background)
- [ ] Minimap uses CSS variables (var(--sd-*)) for all colors
- [ ] Tests for minimap rendering
- [ ] No regressions in canvas tests

---

## Smoke Test

```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run
```

---

## Constraints

- **Rule 3:** CSS variables only — no hardcoded colors
- **Rule 4:** No file over 500 lines
- **Rule 5:** TDD — tests first
- **Rule 6:** No stubs

---

## Model Assignment

**Sonnet** — this requires investigation, platform comparison, and careful CSS work.

---

## Next Steps for Q33N

1. Read the files listed above
2. Investigate the current state (does minimap exist? styled?)
3. Write task file(s) to `.deia/hive/tasks/`
4. Return task files to Q33NR for review
5. Wait for Q33NR approval before dispatching bees
