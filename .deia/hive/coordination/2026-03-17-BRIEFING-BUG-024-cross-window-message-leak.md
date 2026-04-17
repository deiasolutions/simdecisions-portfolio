# BRIEFING: BUG-024 — Cross-window message leaking between EGGs

**Date:** 2026-03-17
**To:** Q33N (Queen Coordinator)
**From:** Q88NR (Regent)
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Fix the relay bus (MessageBus) so that messages from one EGG instance (e.g., Canvas in tab A) do not leak into another EGG instance's panes (e.g., Code chat in tab B) when both are open simultaneously in different browser windows or tabs.

---

## Problem Analysis

**Current state:**
- MessageBus routes messages purely based on `paneId` (node IDs from the shell tree)
- MessageBus has no concept of "EGG instance" or "window context"
- When two EGG instances are open (same or different EGGs), they share the same localStorage/BroadcastChannel event space
- A terminal in Canvas EGG sends IR with `target: links.to_text` → this resolves to a paneId
- If Code EGG happens to have a pane with the same ID (or if BroadcastChannel messages leak), the message appears in the wrong window

**Root cause:**
- No scoping of messages to originating window/tab/EGG context
- BroadcastChannel (if used) would broadcast across all tabs unconditionally
- localStorage events fire across all tabs, but MessageBus doesn't use localStorage for routing (good)
- The issue is likely in how paneIds are generated or how messages are targeted

**Actual issue (reading messageBus.ts carefully):**
- MessageBus is instantiated PER shell (each tab has its own MessageBus instance)
- Messages sent via bus.send() only route to subscribers on THAT instance
- Cross-window leaking should NOT happen through the MessageBus itself...
- **UNLESS:** BroadcastChannel or window.postMessage is being used somewhere to sync messages across tabs

**New hypothesis:**
- Check if GovernanceProxy or configEggCache uses BroadcastChannel
- Check if there's a relay/sync layer that broadcasts bus messages across windows
- Check if localStorage is being used to persist messages and then replayed in other tabs

---

## Files to Investigate

**Core bus:**
- `browser/src/infrastructure/relay_bus/messageBus.ts` — MessageBus class, routing logic
- `browser/src/infrastructure/relay_bus/GovernanceProxy.tsx` — governance wrapper (may intercept/forward)
- `browser/src/infrastructure/relay_bus/configEggCache.ts` — EGG config caching (may use BroadcastChannel)
- `browser/src/infrastructure/relay_bus/types/messages.ts` — message envelope types

**Message senders:**
- `browser/src/primitives/terminal/useTerminal.ts:456-481` — relay mode message sending
- `browser/src/primitives/terminal/useTerminal.ts:594-606` — chat mode message sending (terminal:text-patch)
- `browser/src/primitives/terminal/useTerminal.ts:710-757` — IR mode message sending

**Message receivers:**
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` — receives terminal:text-patch
- Check how text-pane subscribes to bus messages

**Storage/sync layers:**
- Check for BroadcastChannel usage: `grep -r "BroadcastChannel" browser/src/`
- Check for window.postMessage usage: `grep -r "postMessage" browser/src/`
- Check for localStorage message persistence: `grep -r "localStorage.*message" browser/src/`

---

## Acceptance Criteria

From spec:
- [ ] Canvas IR request response only appears in Canvas terminal, not Code chat
- [ ] Messages between panes within same EGG still work
- [ ] No cross-tab message pollution
- [ ] All relay bus tests pass

Additional:
- [ ] Root cause identified and documented in task response
- [ ] Fix implements proper window/tab scoping if needed
- [ ] Tests verify cross-window isolation (mocked or integration)
- [ ] Tests verify same-window routing still works

---

## Constraints

- No file over 500 lines (current messageBus.ts is 301 lines — OK)
- CSS: var(--sd-*) only (no CSS expected)
- No stubs
- TDD: Write tests first demonstrating the bug, then fix

---

## Task Breakdown Guidance for Q33N

**TASK-A: Investigate and reproduce** (P0, haiku)
- Search codebase for BroadcastChannel, postMessage, localStorage message persistence
- Read GovernanceProxy.tsx and configEggCache.ts
- Write test demonstrating cross-window message leak (mock two MessageBus instances)
- Document root cause in response file

**TASK-B: Implement fix** (P0, haiku or sonnet depending on complexity)
- Based on TASK-A findings, implement window/tab scoping mechanism
- Options:
  - Add `windowId` to MessageEnvelope (generated on shell mount, stored in bus instance)
  - Filter BroadcastChannel messages by windowId
  - Add tab/window context to routing logic
- Ensure fix doesn't break same-window routing

**TASK-C: Test coverage** (P0, haiku)
- Tests for cross-window isolation (two bus instances, verify no leak)
- Tests for same-window routing (existing tests should pass)
- Integration test simulating Canvas→Code leak scenario
- All relay bus tests must pass

---

## Test Execution

From spec smoke test:
```bash
cd browser && npx vitest run --reporter=verbose src/infrastructure/
cd browser && npx vitest run
```

---

## Notes

- This is a P0 bug affecting production usage (multiple EGGs open)
- Likely requires architectural fix (not just a patch)
- Q33N should investigate first, then propose fix approach before coding
- If BroadcastChannel is used, we need windowId filtering
- If not, root cause may be in paneId collision or bus instance leaking

---

## Expected Deliverables

From Q33N:
1. **TASK file(s)** for investigation + fix + tests (3 tasks likely)
2. **Response files** with:
   - Root cause analysis
   - Fix approach (with rationale)
   - Test results (all green)
   - No stubs, no TODOs

---

**Action:** Q33N, read the spec and this briefing, investigate the codebase per the file list above, then write task files for the bee(s). Return task files to me (Q88NR) for approval before dispatching bees.
