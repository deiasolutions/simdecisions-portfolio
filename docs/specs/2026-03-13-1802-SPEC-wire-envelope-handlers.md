# SPEC: Wire Envelope Handlers — to_ir, to_explorer, to_simulator

## Priority
P0

## Objective
Wire the three unhandled envelope slots in `routeEnvelope()`. Currently only `to_user` and `to_text` are handled. The `to_ir`, `to_explorer`, and `to_simulator` slots are ignored. This was tested and documented in January 2025 and fell through the cracks during the port to the shiftcenter repo.

## Context
The envelope router lives at `browser/src/services/terminal/terminalResponseRouter.ts` (was frank, renamed to terminal). The `routeEnvelope()` function parses the LLM response envelope and dispatches each slot via the relay bus.

Files to read first:
- `browser/src/services/terminal/terminalResponseRouter.ts` — the router
- `browser/src/services/terminal/types.ts` — envelope type definition
- `browser/src/infrastructure/relay_bus/` — bus send/subscribe API
- `browser/src/primitives/terminal/useTerminal.ts` — where routeEnvelope is called
- `browser/src/apps/terminalAdapter.tsx` — pane registry / link config

## Acceptance Criteria

### to_ir handler
- [ ] When envelope contains `to_ir`, routeEnvelope publishes `terminal:ir-deposit` on the bus
- [ ] Message target is resolved from paneRegistry (linked pane for `to_ir` slot) or broadcast if no link
- [ ] Payload is the raw `to_ir` content (JSON — IR nodes, edges, actions)
- [ ] Test: mock bus, call routeEnvelope with to_ir content, verify bus.send called with correct type and data

### to_explorer handler
- [ ] When envelope contains `to_explorer`, routeEnvelope publishes `terminal:explorer-command` on the bus
- [ ] Payload contains `action` (navigate, open, refresh) and `path`
- [ ] Test: mock bus, call routeEnvelope with to_explorer content, verify bus.send called

### to_simulator handler
- [ ] When envelope contains `to_simulator`, routeEnvelope publishes `terminal:simulator-command` on the bus
- [ ] Payload contains `command` (run, pause, reset, step) and optional parameters
- [ ] Test: mock bus, call routeEnvelope with to_simulator content, verify bus.send called

### to_bus handler (already partially handled?)
- [ ] Check if `to_bus` is handled. If not, wire it: publishes the raw content as a bus message with type from the content's `type` field
- [ ] Test: verify to_bus dispatches correctly

### General
- [ ] All existing routeEnvelope tests still pass
- [ ] 8+ new tests (2 per slot)
- [ ] If no pane is linked for a slot, log a warning to terminal's mini-display ("No pane linked for to_ir — use /link to_ir <pane> to connect") — don't silently drop
- [ ] Envelope with multiple slots filled dispatches ALL of them (not just the first one found)

## Smoke Test
- [ ] In chat.egg.md, send a message — to_user and to_text still work as before
- [ ] In a future canvas.egg.md, to_ir would route to the canvas — for now just verify the bus message is published

## Model Assignment
haiku

## Constraints
- This is a SMALL task — the router already exists and handles two slots. Adding three more follows the exact same pattern. Do not overcomplicate.
- Do not modify the envelope format — only add dispatch logic for slots that are currently ignored
