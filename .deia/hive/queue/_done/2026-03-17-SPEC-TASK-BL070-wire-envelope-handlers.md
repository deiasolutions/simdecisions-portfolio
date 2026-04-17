# BL-070: Wire envelope handlers (to_explorer, to_ir, to_simulator)

## Objective
Wire the envelope routing handlers so terminal commands with route targets (to_explorer, to_ir, to_simulator) deliver their payloads to the correct pane primitives.

## Context
The terminal sends envelopes with route targets but the handlers for to_explorer, to_ir, and to_simulator are not wired. Messages go nowhere or to the wrong pane. The useTerminal hook and terminal routing need to dispatch based on envelope routeTarget.

## Files to Read First
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/primitives/terminal/TerminalApp.tsx`
- `browser/src/infrastructure/relay_bus/relayBus.ts`
- `browser/src/infrastructure/relay_bus/types.ts`
- `browser/src/shell/types.ts`

## Deliverables
- [ ] Wire to_explorer envelope handler to route to tree-browser pane
- [ ] Wire to_ir envelope handler to route to canvas/IR display pane
- [ ] Wire to_simulator envelope handler to route to simulation pane
- [ ] Each handler publishes correct bus event for target pane to consume
- [ ] Tests for each route target delivery

## Acceptance Criteria
- [ ] to_explorer envelopes reach tree-browser pane
- [ ] to_ir envelopes reach canvas IR display
- [ ] to_simulator envelopes reach simulation pane
- [ ] Unknown route targets logged but don't crash
- [ ] All tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/terminal/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
