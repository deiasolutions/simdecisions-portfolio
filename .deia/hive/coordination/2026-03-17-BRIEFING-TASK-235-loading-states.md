# Briefing: TASK-235 — Pane Loading States (W4 — 4.7)

**For:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-17
**Model:** Sonnet

---

## Objective

Add a loading spinner/indicator to panes while their applet content is loading. Users should see visual feedback, not a blank pane followed by a sudden content pop-in.

---

## Context

Wave 4 Product Polish. Terminal already has a spinner (`TerminalOutput.tsx` lines 23-43). But pane-level loading (when an applet is being initialized) has no visual indicator. When you load an EGG or spawn an app, the pane is blank until the component mounts.

This task is about showing a loading state **at the pane level** — before the applet component renders.

---

## Source Spec

`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.7

---

## Key Files to Review

- `browser/src/shell/components/PaneChrome.tsx` — Pane wrapper (227 lines)
- `browser/src/shell/components/EmptyPane.tsx` — Empty state component
- `browser/src/primitives/terminal/TerminalOutput.tsx` — Existing spinner pattern (lines 23-43)
- `browser/src/shell/ShellRoot.tsx` — Where applets are rendered into panes

---

## Deliverables

1. **PaneLoader component** (or inline in PaneChrome):
   - Centered spinner animation (reuse terminal spinner pattern or CSS spinner)
   - Subtle text: "Loading..." in `var(--sd-text-muted)`
   - Shown when: pane has an `appType` assigned but component hasn't mounted yet
   - Hidden when: component renders or errors (hand off to PaneErrorBoundary)

2. **CSS for spinner:**
   - Use `var(--sd-purple)` for spinner color
   - Centered in pane
   - Only CSS variables (no hex, no rgb())

3. **Loading state should not flash for fast loads (<100ms):**
   - Add a small delay before showing spinner to prevent flash on fast loads

4. **Tests:**
   - Loading state shown during mount
   - Hidden after render
   - Run: `cd browser && npx vitest run src/shell/`

---

## Constraints

- **No hardcoded colors.** Only `var(--sd-*)` CSS variables.
- **No file over 500 lines.** Modularize if PaneChrome approaches limit.
- **TDD.** Tests first, then implementation.
- **No stubs.** Every function fully implemented.
- **Reuse existing patterns.** Terminal spinner is the reference implementation.

---

## Priority

P1

---

## Model Assignment

- **Bee model:** Sonnet (UI state logic)

---

## Success Criteria

- [ ] Loading spinner appears when pane is loading an applet
- [ ] Spinner disappears when applet renders
- [ ] No flash for fast loads (<100ms)
- [ ] All CSS uses `var(--sd-*)` variables
- [ ] Tests cover: loading shown, loading hidden, no flash on fast load
- [ ] All tests pass: `cd browser && npx vitest run src/shell/`

---

## Next Steps for Q33N

1. Read the key files listed above
2. Write a task file for a bee (TASK-235)
3. Return to Q33NR for review before dispatching the bee
