# SPEC: Throttle awayManager mousemove Listener

## Priority
P1

## Objective
Add throttling to the awayManager's mousemove event listener which currently fires a Zustand `set()` call on every single mouse movement without any debounce or throttle, causing unnecessary state updates and potential re-renders in any subscriber.

## Context
In `awayManager.ts:98-101`, three event listeners are added. `updateActivity()` calls `set({ lastActivityMs: Date.now(), isAway: false, idleStartMs: null })` which triggers a Zustand state update on EVERY mouse move. Mouse events can fire 60-100+ times per second during normal use. This is wasteful — the idle check interval is 5 seconds, so updating more than once per second is pointless.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\away\awayManager.ts

## Acceptance Criteria
- [ ] Add throttling to the awayManager activity listeners — update at most once per 1000ms (matching idle check granularity)
- [ ] Use a simple timestamp-based throttle (no lodash dependency): `if (Date.now() - lastUpdate < 1000) return`
- [ ] Store the throttle state in module scope (not in Zustand state)
- [ ] Clean up listeners on `stopIdleTracking()` — currently listeners are never removed because `activityListenersInstalled` flag prevents re-adding but there's no removal path
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests still pass: `cd browser && npx vitest run src/services/away`
- [ ] Add test: updateActivity is not called more than once per 1000ms during rapid mousemove
- [ ] Add test: stopIdleTracking cleans up event listeners

## Smoke Test
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/services/away

## Model Assignment
haiku

## Depends On
(none)

## Constraints
- No file over 500 lines
- No stubs
- TDD — tests first
- Do NOT change the Zustand store shape or the checkIdle logic
- Do NOT modify presenceService.ts in this spec (that's SPEC-PERF-04)
- Write response to: .deia/hive/responses/20260401-SPEC-PERF-03-RESPONSE.md
