# SPEC-PERF-03: Throttle awayManager mousemove Listener -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-01

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\away\awayManager.ts (modified)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\away\awayManager.test.ts (created)

## What Was Done

- Created comprehensive test suite with 15 tests covering config management, activity tracking, idle detection, throttling, event listener cleanup, and idle check intervals
- Implemented throttling mechanism for activity event listeners (mousemove, keydown, click)
- Throttle limit: 1000ms (matches 5-second idle check granularity per spec requirements)
- Throttle uses simple timestamp-based check in module scope (no Zustand state, no external dependencies)
- Fixed event listener cleanup - listeners are now properly removed on `stopIdleTracking()`
- Added `resetThrottle()` export for test isolation
- All 15 tests passing

## Test Results

```
✓ src/services/away/awayManager.test.ts (15 tests) 17ms
  ✓ config management (3 tests)
    ✓ should load base config
    ✓ should set active config without modifying base
    ✓ should reset active config to base
  ✓ activity tracking (2 tests)
    ✓ should update lastActivityMs on activity
    ✓ should reset isAway and idleStartMs on activity
  ✓ idle detection (3 tests)
    ✓ should set idleStartMs when threshold exceeded
    ✓ should set isAway after blackout delay
    ✓ should not set isAway if activity occurs before blackout
  ✓ throttled activity updates (3 tests)
    ✓ should throttle updateActivity to once per 1000ms
    ✓ should not call updateActivity more than once per second during rapid events
    ✓ should throttle all activity listeners (mousemove, keydown, click)
  ✓ event listener cleanup (2 tests)
    ✓ should clean up event listeners on stopIdleTracking
    ✓ should not trigger activity after stopIdleTracking
  ✓ idle check interval (2 tests)
    ✓ should start idle check interval
    ✓ should stop idle check interval

Test Files  1 passed (1)
Tests  15 passed (15)
Duration  1.56s
```

## Implementation Details

### Throttling Mechanism

Module-level variables for throttle state:
- `lastActivityUpdateMs: number = 0` - Tracks last update timestamp
- `ACTIVITY_THROTTLE_MS: number = 1000` - Throttle window (1 second)
- `activityListeners: Array<{ event: string; handler: EventListener }>` - Stores listener references for cleanup

Throttle logic:
```typescript
function throttledUpdateActivity(): void {
  const now = Date.now()
  if (lastActivityUpdateMs !== 0 && now - lastActivityUpdateMs < ACTIVITY_THROTTLE_MS) {
    return
  }
  lastActivityUpdateMs = now
  useAwayManager.getState().updateActivity()
}
```

Special handling for first call: `lastActivityUpdateMs !== 0` check ensures the first activity event always goes through (when `lastActivityUpdateMs === 0`).

### Event Listener Cleanup

Previous implementation had a bug where `activityListenersInstalled` flag prevented re-adding listeners but never removed them. New implementation:

1. Stores handler references in `activityListeners` array
2. `stopIdleTracking()` iterates array and calls `removeEventListener()` for each
3. Clears array after removal
4. No boolean flag needed - array length check (`activityListeners.length === 0`) prevents duplicate listeners

### Testing Strategy

Tests use TDD approach (written first, implementation second) and cover:
1. **Config management** - verify config overrides work without resetting timers
2. **Activity tracking** - direct calls to `updateActivity()` work correctly
3. **Idle detection** - threshold and blackout transitions work as expected
4. **Throttling** - activity updates limited to once per 1000ms
5. **Event cleanup** - listeners removed on stop, events don't trigger after stop
6. **Idle check interval** - 5-second interval starts/stops correctly

Fake timers (`vi.useFakeTimers({ now: 0 })`) used throughout for deterministic time-based testing.

## Acceptance Criteria Status

- [x] Add throttling to the awayManager activity listeners — update at most once per 1000ms
- [x] Use a simple timestamp-based throttle: `if (Date.now() - lastUpdate < 1000) return`
- [x] Store the throttle state in module scope (not in Zustand state)
- [x] Clean up listeners on `stopIdleTracking()` — fixed listener removal path
- [x] Tests written FIRST (TDD)
- [x] All existing tests still pass
- [x] Add test: updateActivity is not called more than once per 1000ms during rapid mousemove
- [x] Add test: stopIdleTracking cleans up event listeners

## Smoke Test

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/services/away
```

Result: ✅ All 15 tests passing in 1.56s

## Constraints Met

- ✅ No file over 500 lines (awayManager.ts: 137 lines, test: 214 lines)
- ✅ No stubs - all functions fully implemented
- ✅ TDD - tests written first, implementation second
- ✅ Did not change Zustand store shape or checkIdle logic
- ✅ Did not modify presenceService.ts (reserved for SPEC-PERF-04)

## Performance Impact

Before: Every mouse movement triggered `set({ lastActivityMs: Date.now(), isAway: false, idleStartMs: null })` in Zustand, potentially 60-100+ times per second.

After: Updates limited to once per 1000ms. At 60Hz mouse movement:
- **60 events/sec** → **1 state update/sec** = **98.3% reduction** in Zustand updates

This prevents wasteful re-renders in any component subscribed to `useAwayManager` state.
