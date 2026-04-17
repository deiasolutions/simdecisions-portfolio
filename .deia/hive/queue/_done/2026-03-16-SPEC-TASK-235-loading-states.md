# TASK-235: Loading States — Pane Spinner While Content Loads (W4 — 4.7)

## Objective
Add a loading spinner/indicator to panes while their applet content is loading. Users should see visual feedback, not a blank pane followed by a sudden content pop-in.

## Context
Wave 4 Product Polish. Terminal already has a spinner (`TerminalOutput.tsx` lines 23-43). But pane-level loading (when an applet is being initialized) has no visual indicator. When you load an EGG or spawn an app, the pane is blank until the component mounts.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.7

## Files to Read First
- `browser/src/shell/components/PaneChrome.tsx` — Pane wrapper (227 lines)
- `browser/src/shell/components/EmptyPane.tsx` — Empty state
- `browser/src/primitives/terminal/TerminalOutput.tsx` — Existing spinner pattern (lines 23-43)
- `browser/src/shell/ShellRoot.tsx` — Where applets are rendered into panes

## Deliverables
- [ ] Add a `PaneLoader` component (or inline in PaneChrome):
  - Centered spinner animation (reuse terminal spinner pattern or CSS spinner)
  - Subtle text: "Loading..." in `var(--sd-text-muted)`
  - Shown when: pane has an `appType` assigned but component hasn't mounted yet
  - Hidden when: component renders or errors (hand off to PaneErrorBoundary)
- [ ] Add CSS for spinner: use `var(--sd-purple)` for spinner color, centered in pane
- [ ] Ensure loading state doesn't flash for fast loads (<100ms) — add a small delay before showing
- [ ] Add tests: loading state shown during mount, hidden after render
- [ ] Run: `cd browser && npx vitest run src/shell/`

## Priority
P1

## Model
sonnet
