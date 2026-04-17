# BRIEFING: BUG-018 Canvas IR Response Routing

**To:** Q33N (Queen Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-03-17
**Spec:** `2026-03-17-SPEC-TASK-BUG018-canvas-ir-wrong-pane.md`

---

## Mission

Fix the Canvas IR generation response routing so it appears in the Canvas terminal pane instead of leaking to the Code egg's chat pane.

---

## Background

When a user generates IR (intermediate representation) in the Canvas EGG, the response is appearing in the wrong location:
- Sometimes shows an error in Canvas
- Actual response appears in the Code egg's chat pane (different tab)
- This is an envelope routing/scoping issue

---

## Key Files to Investigate

Per spec, start with:
- `browser/src/primitives/canvas/` (Canvas components)
- `browser/src/primitives/terminal/useTerminal.ts` (Terminal hook)
- `browser/src/primitives/terminal/TerminalApp.tsx` (Terminal component)
- `browser/src/infrastructure/relay_bus/relayBus.ts` (Message bus)
- `eggs/canvas.egg.md` (Canvas EGG layout)

---

## Required Deliverables

1. **Trace IR generation request/response flow** in Canvas
   - Identify where IR request is initiated
   - Follow the envelope through the relay bus
   - Find where response routing decision is made

2. **Fix routing** so IR response targets Canvas terminal pane
   - Ensure envelope has correct EGG context/scope
   - Fix any missing paneId or targetPane metadata

3. **Fix error handling** for IR generation failures
   - Errors should display in Canvas, not be swallowed
   - No error leakage to other eggs

4. **Tests** for Canvas IR response routing
   - Test IR response appears in correct pane
   - Test IR response does NOT leak to Code egg
   - Test error handling displays in Canvas

---

## Acceptance Criteria (from spec)

- [ ] Canvas IR generation response appears in Canvas terminal pane
- [ ] No IR responses leak to Code egg
- [ ] IR generation errors shown in Canvas, not swallowed
- [ ] Tests pass

---

## Smoke Tests Required

```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/
```

---

## Constraints

- **No file over 500 lines** (hard limit 1,000)
- **CSS: `var(--sd-*)` only** (no hex, rgb, named colors)
- **No stubs** (full implementation required)
- **Model:** Sonnet
- **Priority:** P0

---

## Task Breakdown Instructions

Please create task files with:

1. **Absolute file paths** (Windows format: `C:\Users\davee\OneDrive\...`)
2. **Test requirements** specified (how many tests, which scenarios)
3. **Response file template** (8-section format)
4. **Modularization check** (no file over 500 lines)

Break into subtasks if needed (e.g., trace flow, fix routing, add tests).

---

## Questions to Answer in Your Tasks

1. How is the IR request initiated in Canvas? (Which component, which event?)
2. What envelope metadata is attached to the IR request?
3. Where does the relay bus route the IR response? (Decision logic?)
4. Why does it route to Code egg instead of Canvas terminal?
5. What metadata is needed to route correctly?

---

## Ready to Proceed?

Please create task files and submit for approval when ready.

---

**Q88NR**
