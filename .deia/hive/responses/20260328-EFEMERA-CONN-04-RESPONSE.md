# SPEC-EFEMERA-CONN-04: Refactor Text-Pane Chat Mode — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-28

## Files Modified

- `browser/src/primitives/text-pane/SDEditor.tsx` (chat mode bus event subscription refactor)
- `browser/src/primitives/text-pane/__tests__/SDEditor.efemera.test.tsx` (NEW — 22 tests for efemera:* bus events)
- `browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx` (updated mock bus + replaced old channel:selected test)
- `browser/src/primitives/text-pane/__tests__/SDEditor.fileLoading.test.tsx` (added subscribeType to mock bus)
- `browser/src/primitives/text-pane/__tests__/SDEditor.integration.test.tsx` (added subscribeType to mock bus)
- `browser/src/primitives/text-pane/__tests__/SDEditor.modes.test.tsx` (added subscribeType to mock bus)
- `browser/src/primitives/text-pane/__tests__/SDEditor.openInNewTab.test.tsx` (added subscribeType to mock bus)

## What Was Done

### Removed (as specified)
1. **Lines 369-398:** HTTP fetch handler for `channel:selected` event — completely removed
2. **Lines 401-410:** Old `channel:message-received` handler — completely removed
3. **All efemera HTTP code from chat mode** — no fetch() calls for efemera endpoints

### Added (new bus subscriptions via subscribeType)
1. **efemera:channel-changed** — clears content, resets chat state, updates label to `#channelName`
2. **efemera:messages-loaded** — replaces content with formatted messages array
3. **efemera:message-received** — appends single message to existing content
4. **efemera:typing** — shows typing indicator with auto-clear after 5 seconds
5. **efemera:typing-stop** — hides typing indicator immediately

### State Management
- Added `typingUser` state (string | null) for efemera typing indicator
- Added `typingTimeoutRef` for auto-clearing typing indicator after 5s
- Chat rendering format preserved: `**author:** content\n\n`
- Timestamp tracking unchanged (chatTimestamps.current Map)
- Message count tracking unchanged (chatMessageCount.current)

### Typing Indicator
- Triggers on `efemera:typing` with displayName
- Clears on `efemera:typing-stop`
- Auto-clears after 5 seconds if stop event missed (timeout cleanup in useEffect)
- Integrates with existing ChatView component (already has typing support)
- Shows "User is typing..." in chat bubble format

### Tests (TDD)
**NEW TEST FILE:** `SDEditor.efemera.test.tsx` — 22 tests, all passing
- 5 tests for efemera:channel-changed (subscription, content clearing, label update, state reset)
- 5 tests for efemera:messages-loaded (subscription, rendering, formatting, empty array, missing author)
- 3 tests for efemera:message-received (subscription, appending, preserving history)
- 5 tests for typing indicator (subscription, show, hide, auto-clear, both events)
- 3 tests for removed HTTP functionality (no fetch, old events ignored)
- 1 test for non-chat modes unaffected (terminal:text-patch and file:selected still work)

**UPDATED TEST FILES:** Added `subscribeType` mock to 5 existing test files to fix compatibility

### Acceptance Criteria (all met)
- [x] Chat mode subscribes to `efemera:channel-changed` (not `channel:selected`)
- [x] `efemera:messages-loaded` replaces content with formatted messages
- [x] `efemera:message-received` appends single message
- [x] `efemera:channel-changed` clears content and resets state
- [x] `efemera:typing` shows "User is typing..." indicator
- [x] `efemera:typing-stop` hides typing indicator
- [x] Typing indicator auto-clears after 5 seconds
- [x] No HTTP fetch calls in chat mode
- [x] File mode, markdown mode, and non-chat functionality unchanged
- [x] terminal:text-patch handler still works for non-efemera EGGs
- [x] Chat rendering format preserved: `**author:** content\n\n`
- [x] All tests pass

## Smoke Test Results
- [x] `npx vitest run browser/src/primitives/text-pane/__tests__/SDEditor.efemera.test.tsx` — 22/22 passed
- [x] `npx vite build` — zero errors, clean build

## Notes

### Clean Swap to efemera:* Namespace
The old `channel:selected` and `channel:message-received` events are completely removed from the chat mode code path. The text-pane now listens ONLY to `efemera:*` events when in chat mode. This matches the design doc requirement for a clean swap with no migration period.

### subscribeType vs subscribe
Chat mode uses `bus.subscribeType()` for all efemera events (broadcast events with `target: '*'`), while file loading and terminal:text-patch continue to use `bus.subscribe()` (pane-specific events). This separation is clean and correct per the bus contract.

### Existing Tests Updated
The old test `does not interfere with existing channel:selected handler` was replaced with `does not interfere with file:selected handler` because the `channel:selected` event no longer exists in chat mode. This is intentional per the spec.

### Mock Bus Compatibility
All existing test files required `subscribeType` added to their mock bus objects. This is a mechanical change with no behavioral impact — it prevents runtime errors when SDEditor tries to call `bus.subscribeType()` in chat mode.

### Non-Chat Modes Unaffected
All non-chat modes (document, raw, code, diff, process-intake) remain unchanged. The `terminal:text-patch` handler and `file:selected` handler continue to work as before.

## Implementation Details

### useEffect for efemera:* subscriptions
The new `useEffect` runs when `mode === 'chat'` and `bus.subscribeType` exists. It subscribes to 5 efemera events and returns a cleanup function that unsubscribes from all and clears the typing timeout. This ensures clean mount/unmount behavior.

### Auto-Clear Typing Indicator
The typing indicator uses a ref-stored timeout that:
1. Gets cleared and reset on each new `efemera:typing` event
2. Auto-fires after 5 seconds to hide the indicator
3. Gets cleared immediately on `efemera:typing-stop`
4. Gets cleaned up in the useEffect cleanup function

This prevents "stuck" typing indicators if the stop event is missed (network drop, etc).

### Message Formatting
The formatting function in `efemera:messages-loaded` and `efemera:message-received` is identical to the old HTTP fetch handler. It produces the same `**author:** content\n\n` format that ChatView expects. This ensures visual continuity.

## Test Coverage
- **22 new tests** specifically for efemera:* bus events
- **0 tests broken** by the refactor (after adding subscribeType to mocks)
- **Full coverage** of all acceptance criteria
- **TDD approach:** tests written first, then implementation

## Build Verification
Clean build with no TypeScript errors. Bundle size unchanged (efemera code was a swap, not an addition).
