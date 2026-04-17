# BUG-024: Cross-window message leaking between EGGs

## Objective
Fix the relay bus so messages from one EGG (e.g. Canvas) do not leak into another EGG's panes (e.g. Code chat) when both are open in different tabs or windows.

## Context
The relay bus in `browser/src/infrastructure/relay_bus/` handles inter-pane messaging. When Canvas sends an IR generation request, the response sometimes appears in the Code egg's chat pane instead. This suggests the bus routing is not properly scoping messages to their originating EGG/window context.

## Files to Read First
- `browser/src/infrastructure/relay_bus/`
- `browser/src/infrastructure/relay_bus/relayBus.ts`
- `browser/src/infrastructure/relay_bus/types.ts`
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/primitives/text-pane/services/chatRenderer.tsx`

## Deliverables
- [ ] Identify how messages leak across windows/tabs
- [ ] Fix bus routing to scope messages to originating EGG context
- [ ] Ensure localStorage/BroadcastChannel events are properly filtered
- [ ] Tests for cross-window isolation
- [ ] Tests for same-window correct routing

## Acceptance Criteria
- [ ] Canvas IR request response only appears in Canvas terminal, not Code chat
- [ ] Messages between panes within same EGG still work
- [ ] No cross-tab message pollution
- [ ] All relay bus tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/infrastructure/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
sonnet

## Priority
P0
