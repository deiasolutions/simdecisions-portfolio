# SPEC-PERF-04: Guard Presence Heartbeat + Deduplicate Activity Listeners -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-01

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\presenceService.ts` (refactored, now 160 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\efemera-connector\__tests__\presenceService.test.ts` (updated, 306 lines)

## What Was Done

- **Added circuit breaker to heartbeat**: After 3 consecutive failures, heartbeat interval is cleared and a warning is logged. No auto-restart.
- **Removed duplicate event listeners**: Deleted `mousemove`, `keydown`, `mousedown` window event listeners from presenceService.
- **Integrated with awayManager**: Now subscribes to `useAwayManager.subscribe(state => state.isAway, ...)` to detect idle transitions.
- **Removed idle detection methods**: Deleted `onActivity()`, `resetIdleTimer()`, `goIdle()`, `boundActivityHandler`, `idleTimer`, `debounceTimer`, and `idleThresholdMs` fields since idle detection is now delegated to awayManager.
- **Circuit breaker logic**: Tracks `heartbeatFailureCount`, increments on each failure, resets on success. When count reaches `MAX_HEARTBEAT_FAILURES` (3), sets `circuitBreakerTripped` flag and stops the heartbeat timer.
- **Tests written first (TDD)**: 7 new tests added for circuit breaker and awayManager integration.
- **All 96 efemera-connector tests pass**: Full test suite verified.

## Tests Run

```bash
npx vitest run src/primitives/efemera-connector
```

**Result:**
- 7 test files
- 96 tests passed
- 0 failures

## New Tests Added

1. **Circuit breaker tests** (2):
   - `should stop heartbeat after 3 consecutive failures`
   - `should reset failure count on successful heartbeat`

2. **awayManager integration tests** (5):
   - `should not add window event listeners`
   - `should subscribe to awayManager state on start`
   - `should call setStatus("idle") when awayManager.isAway becomes true`
   - `should call setStatus("online") when awayManager.isAway becomes false`
   - `should unsubscribe from awayManager on stop`

## Removed Tests

- Deleted 3 old idle detection tests that tested direct mousemove/keydown/mousedown handling, since presenceService no longer manages its own event listeners.

## Acceptance Criteria

- [x] Add a circuit breaker to presenceService heartbeat: after 3 consecutive failures, stop the heartbeat interval and log a warning. Do NOT auto-restart.
- [x] Remove the duplicate mousemove/keydown/mousedown listeners from presenceService
- [x] Instead, subscribe to awayManager's Zustand store to detect idle transitions: `useAwayManager.subscribe(state => state.isAway, ...)` — when isAway transitions true, call `setStatus('idle')`; when false, call `setStatus('online')`
- [x] Remove the `onActivity()`, `resetIdleTimer()`, `goIdle()` methods from presenceService since idle detection is now delegated to awayManager
- [x] Keep the `setStatus()` API call and the heartbeat (with circuit breaker) — presenceService still owns the backend communication
- [x] Tests written FIRST (TDD)
- [x] All existing tests still pass: `cd browser && npx vitest run src/primitives/efemera-connector`
- [x] Add test: heartbeat stops after 3 consecutive failures
- [x] Add test: presenceService does not add window event listeners
- [x] Add test: idle transition from awayManager triggers setStatus('idle')

## Smoke Test

✅ All tests pass:

```
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/efemera-connector

Test Files  7 passed (7)
Tests      96 passed (96)
```

## Implementation Details

### Circuit Breaker

Added three private fields:
- `heartbeatFailureCount: number = 0`
- `circuitBreakerTripped: boolean = false`
- `MAX_HEARTBEAT_FAILURES = 3`

In `sendHeartbeat()`:
- On success: reset `heartbeatFailureCount` to 0
- On failure: increment `heartbeatFailureCount`
- When count reaches 3: set `circuitBreakerTripped`, clear `heartbeatTimer`, log warning
- Early return if `circuitBreakerTripped` is true

### awayManager Integration

In `start()`:
```ts
this.awayUnsubscribe = useAwayManager.subscribe(
  (state) => state.isAway,
  (isAway) => {
    if (isAway) {
      this.setStatus('idle').catch(() => {})
    } else {
      this.setStatus('online').catch(() => {})
    }
  }
)
```

In `stop()`:
```ts
if (this.awayUnsubscribe) {
  this.awayUnsubscribe()
  this.awayUnsubscribe = null
}
```

### Removed Code

Deleted 7 private fields:
- `idleTimer`
- `debounceTimer`
- `idleThresholdMs`
- `boundActivityHandler`

Deleted 3 methods:
- `onActivity()`
- `resetIdleTimer()`
- `goIdle()`

Removed 3 event listener registrations in `start()`:
- `window.addEventListener('mousemove', ...)`
- `window.addEventListener('keydown', ...)`
- `window.addEventListener('mousedown', ...)`

Removed 3 event listener removals in `stop()`:
- `window.removeEventListener('mousemove', ...)`
- `window.removeEventListener('keydown', ...)`
- `window.removeEventListener('mousedown', ...)`

## Line Count

- **Before:** presenceService.ts = 180 lines
- **After:** presenceService.ts = 160 lines (20 lines removed)
- **Tests:** presenceService.test.ts = 306 lines (71 lines added)

## Notes

- The `idleThresholdMs` parameter in `start()` is no longer used by presenceService but remains in the signature to avoid breaking the public API. awayManager has its own idle threshold config.
- The circuit breaker warning message is logged once when the breaker trips. No retry logic — the service stays stopped until `start()` is called again.
- All event listener registration is now handled exclusively by awayManager (per SPEC-PERF-03).
- The heartbeat still sends the current status every 60 seconds (or custom interval) until the circuit breaker trips.
