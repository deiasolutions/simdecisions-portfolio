# SPEC: Guard Presence Heartbeat + Deduplicate Activity Listeners

## Priority
P1

## Objective
Fix two issues in presenceService.ts: (1) the heartbeat fires every 60s to a potentially dead endpoint without checking if the API is reachable, and (2) presenceService adds its own set of mousemove/keydown/mousedown listeners that duplicate what awayManager already does.

## Context
**Heartbeat issue:** `presenceService.ts:38` starts `setInterval(sendHeartbeat, 60000)`. Each heartbeat sends `PUT /relay/presence` with a 5-second AbortSignal timeout. On efemera.live, if the relay endpoint isn't deployed, every heartbeat ties up a network connection for 5 seconds before timing out. This runs forever with no circuit breaker.

**Duplicate listeners:** `presenceService.ts:44-46` adds `mousemove`, `keydown`, `mousedown` window listeners (debounced 500ms). `awayManager.ts:99-101` adds the same listeners. Both track user activity for idle detection. The presence service should use awayManager's state instead of running its own listeners.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\presenceService.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\away\awayManager.ts

## Acceptance Criteria
- [ ] Add a circuit breaker to presenceService heartbeat: after 3 consecutive failures, stop the heartbeat interval and log a warning. Do NOT auto-restart.
- [ ] Remove the duplicate mousemove/keydown/mousedown listeners from presenceService
- [ ] Instead, subscribe to awayManager's Zustand store to detect idle transitions: `useAwayManager.subscribe(state => state.isAway, ...)` — when isAway transitions true, call `setStatus('idle')`; when false, call `setStatus('online')`
- [ ] Remove the `onActivity()`, `resetIdleTimer()`, `goIdle()` methods from presenceService since idle detection is now delegated to awayManager
- [ ] Keep the `setStatus()` API call and the heartbeat (with circuit breaker) — presenceService still owns the backend communication
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests still pass: `cd browser && npx vitest run src/primitives/efemera-connector`
- [ ] Add test: heartbeat stops after 3 consecutive failures
- [ ] Add test: presenceService does not add window event listeners
- [ ] Add test: idle transition from awayManager triggers setStatus('idle')

## Smoke Test
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/efemera-connector

## Model Assignment
haiku

## Depends On
- SPEC-PERF-03-away-throttle

## Constraints
- No file over 500 lines
- No stubs
- TDD — tests first
- Do NOT modify awayManager.ts (that's SPEC-PERF-03)
- presenceService public API (start, stop, destroy, setStatus, getStatus) must remain unchanged
- Write response to: .deia/hive/responses/20260401-SPEC-PERF-04-RESPONSE.md
