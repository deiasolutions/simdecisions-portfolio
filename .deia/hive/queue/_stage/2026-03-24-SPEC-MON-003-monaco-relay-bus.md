# SPEC-MON-003: Monaco Relay Bus Integration

## Priority
P1

## Depends On
SPEC-MON-001-monaco-applet-component

## Objective
Wire Monaco into the relay bus so it becomes a first-class ShiftCenter citizen. Other panes (AI assistant, log-viewer, terminal) can push code into the editor and receive code output from it via the bus. MON-001 exposes getValue() via ref. This task adds outbound CODE_CHANGED events on content change (debounced 300ms) and inbound code:set / code:save handlers. No pane talks directly to another pane's component — everything goes through the bus.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx

## Scope

Build these files under `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\`:

1. **monacoRelayBus.ts** — Bus wiring module
   - init(editorRef, nodeId, bus) / dispose()
   - Outbound CODE_CHANGED: debounced 300ms, payload includes nodeId, language, content, cursor position. Only emit when content actually changes (compare hash). Emit to topic code-editor:nodeId
   - Inbound code:set: subscribe to code:set events targeting this nodeId. On receipt call setValue(content), optionally switch language. Do NOT re-emit CODE_CHANGED (loop guard)
   - Inbound code:save: subscribe to code:save events, delegate to volume adapter saveFile()

2. **Wire into MonacoApplet.tsx** (minimal)
   - On mount: monacoRelayBus.init(editorRef, nodeId, bus)
   - On unmount: monacoRelayBus.dispose()

3. **Event Ledger** — CODE_CHANGED events with all 3 currencies (CLOCK, COIN, CARBON)

4. **RTD publication** — publish code:line_count metric on every CODE_CHANGED, publish code:language on language switch

## Deliverables
1. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\monacoRelayBus.ts
2. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\MonacoApplet.tsx (minimal additions)
3. C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\code-editor\__tests__\monacoRelayBus.test.ts

## Acceptance Criteria
- [ ] CODE_CHANGED emitted after 300ms debounce on content change
- [ ] CODE_CHANGED NOT emitted when content is set programmatically via code:set (loop guard)
- [ ] code:set payload loads content into editor
- [ ] code:save triggers volume save (delegates correctly)
- [ ] RTD published on CODE_CHANGED with code:line_count
- [ ] CODE_CHANGED appears in Event Ledger with all 3 currencies
- [ ] All tests pass (minimum 10 tests)
- [ ] Existing MON-001 tests still pass (no regressions)

## Response File
20260324-TASK-MON-003-RESPONSE.md
