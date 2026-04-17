# BUG-018: Canvas IR generation shows error, response appears in Code egg instead

## Objective
Fix Canvas IR generation so the response appears in the Canvas terminal/IR pane, not in the Code egg's chat pane.

## Context
When Canvas generates IR (intermediate representation), the response sometimes shows an error and/or the actual response appears in the Code egg's chat pane on a different tab. This is a routing issue — the IR response envelope is not scoped to the Canvas EGG context.

## Files to Read First
- `browser/src/primitives/canvas/`
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/primitives/terminal/TerminalApp.tsx`
- `browser/src/infrastructure/relay_bus/relayBus.ts`
- `eggs/canvas.egg.md`

## Deliverables
- [ ] Trace IR generation request/response flow in Canvas
- [ ] Fix routing so IR response targets Canvas terminal pane, not Code chat
- [ ] Fix error handling for IR generation failures
- [ ] Tests for Canvas IR response routing

## Acceptance Criteria
- [ ] Canvas IR generation response appears in Canvas terminal pane
- [ ] No IR responses leak to Code egg
- [ ] IR generation errors shown in Canvas, not swallowed
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/canvas/`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/terminal/`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
sonnet

## Priority
P0
