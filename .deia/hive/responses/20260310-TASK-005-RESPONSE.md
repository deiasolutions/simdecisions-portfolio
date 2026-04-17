# TASK-005: Relay Bus — Port Cross-Pane Message Bus + Governance -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-10

## Files Modified

### Created Files (All Paths Absolute)

**Project Configuration:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\tsconfig.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vitest.config.ts`

**Core Infrastructure:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\index.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\GovernanceProxy.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\permissionsResolver.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\configEggCache.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\constants.ts`

**Type Definitions:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\permissions.ts`

**Tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\setup.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messages.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.mute.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\GovernanceProxy.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\permissionsResolver.test.ts`

**Total Files Created:** 16

## What Was Done

### Ported Core Infrastructure
- **MessageBus class** (messageBus.ts, 282 lines): In-memory pub/sub message bus with nonce replay protection, telemetry tracking, tree-aware routing, and mute enforcement
- **ShellCtx and useShell** (messageBus.ts): React context and hook for accessing message bus throughout component tree
- **GovernanceProxy component** (GovernanceProxy.tsx, 174 lines): React wrapper that intercepts `bus.send()` and `bus.subscribe()` to enforce `bus_emit` and `bus_receive` whitelists, with platform invariants bypass
- **permissionsResolver** (permissionsResolver.ts, 197 lines): Computes effective permissions from trust tier → EGG ceiling → node tightening intersection logic
- **configEggCache** (configEggCache.ts, 46 lines): In-memory cache for boot-loaded config EGGs used by permissions resolver

### Converted JS → TypeScript
- Converted `shell.context.js` (186 lines) → `messageBus.ts` with typed methods
- Converted `shell.constants.js` (246 lines) → `constants.ts` (bus constants only, 38 lines)
- Extracted `uid()` utility from `shell.utils.js` into `messageBus.ts`

### Added Mute Enforcement
- Implemented mute level enforcement in `MessageBus.send()`:
  - `none`: all messages delivered
  - `notifications`: only notification-type messages blocked
  - `inbound`: all incoming messages to pane blocked
  - `outbound`: all outgoing messages from pane blocked
  - `full`: all messages to/from pane blocked
- Platform invariants (`relay_bus`, `ledger_writer`, `gate_enforcer`, `settings_advertisement`, `metrics_advertisement`) bypass mute
- Added `setMuteState()` and `getMuteState()` methods to MessageBus
- Fixed broadcast message delivery to check mute state per-subscriber

### Fixed Imports and Dependencies
- Updated all imports from old repo structure to local `relay_bus/` paths
- Removed dependencies on shell UI constants (themes, CSS, node types, etc.)
- Kept only bus-related constants in `constants.ts`

### Wrote Comprehensive Tests
- **messages.test.ts** (15 tests): Envelope validation, required fields, edge cases
- **messageBus.test.ts** (28 tests): pub/sub, nonce replay, telemetry, tree-aware routing, LOG_EVENT dispatch
- **messageBus.mute.test.ts** (25 tests): All mute levels, platform invariants bypass, mute cycle
- **GovernanceProxy.test.tsx** (16 tests): bus_emit/bus_receive whitelist enforcement, platform invariants, governed context
- **permissionsResolver.test.ts** (31 tests): Trust tiers, EGG ceiling, node tightening, intersection logic, registry building

**Total Tests Written:** 115 tests
**All Tests Passing:** ✅ 115/115

## Test Results

### Test Files Run
- `messages.test.ts`: ✅ 15 tests passed
- `messageBus.test.ts`: ✅ 28 tests passed
- `messageBus.mute.test.ts`: ✅ 25 tests passed
- `GovernanceProxy.test.tsx`: ✅ 16 tests passed
- `permissionsResolver.test.ts`: ✅ 31 tests passed

### Pass/Fail Counts
- **Test Files:** 5 passed
- **Tests:** 115 passed, 0 failed
- **Duration:** 2.01s (transform 179ms, setup 581ms, collect 467ms, tests 111ms)

### Notes
- stderr output from GovernanceProxy.test.tsx is expected — test verifies that GovernanceProxy throws error when used outside ShellCtx (test passes)

## Build Verification

```
npm install: ✅ Success (253 packages installed)
npm test: ✅ All tests pass (115/115)
```

### Vitest Output Summary
```
Test Files  5 passed (5)
Tests  115 passed (115)
Start at  21:22:28
Duration  2.01s
```

### TypeScript Compilation
- No TypeScript errors
- Strict mode enabled
- All imports resolved correctly

## Acceptance Criteria

### Deliverables
- [x] `browser/package.json`
- [x] `browser/tsconfig.json`
- [x] `browser/vitest.config.ts`
- [x] `browser/src/infrastructure/relay_bus/index.ts`
- [x] `browser/src/infrastructure/relay_bus/messageBus.ts`
- [x] `browser/src/infrastructure/relay_bus/GovernanceProxy.tsx`
- [x] `browser/src/infrastructure/relay_bus/permissionsResolver.ts`
- [x] `browser/src/infrastructure/relay_bus/configEggCache.ts`
- [x] `browser/src/infrastructure/relay_bus/constants.ts`
- [x] `browser/src/infrastructure/relay_bus/types/messages.ts`
- [x] `browser/src/infrastructure/relay_bus/types/permissions.ts`
- [x] `browser/src/infrastructure/relay_bus/__tests__/messageBus.test.ts`
- [x] `browser/src/infrastructure/relay_bus/__tests__/messageBus.mute.test.ts`
- [x] `browser/src/infrastructure/relay_bus/__tests__/GovernanceProxy.test.tsx`
- [x] `browser/src/infrastructure/relay_bus/__tests__/permissionsResolver.test.ts`
- [x] `browser/src/infrastructure/relay_bus/__tests__/messages.test.ts`

### Test Requirements Met
- [x] messageBus.test.ts: 28 tests (pub/sub, nonce, telemetry, routing)
- [x] messageBus.mute.test.ts: 25 tests (all mute levels enforced)
- [x] GovernanceProxy.test.tsx: 16 tests (whitelist enforcement, platform invariants)
- [x] permissionsResolver.test.ts: 31 tests (trust tiers, EGG, node intersection)
- [x] messages.test.ts: 15 tests (envelope validation)
- [x] **Minimum 40 tests required → 115 tests delivered ✅**

### Constraints Met
- [x] TypeScript (strict mode)
- [x] React 18+ (context, hooks)
- [x] No external dependencies beyond React + testing libs (vitest)
- [x] All files under 500 lines (largest: messageBus.ts at 282 lines)
- [x] No stubs — every function fully implemented
- [x] No CSS (bus infrastructure, no UI)
- [x] Tests use vitest (not jest)

## Clock / Cost / Carbon

### Clock
- **Start Time:** 2026-03-10 21:18:00 UTC
- **End Time:** 2026-03-10 21:24:00 UTC
- **Total Duration:** 6 minutes

### Cost
- **Model:** Claude Sonnet 4.5
- **Input Tokens:** ~72,000
- **Output Tokens:** ~15,000
- **Estimated Cost:** ~$0.90 USD (at $3/MTok input, $15/MTok output)

### Carbon
- **Compute Time:** 6 minutes active work
- **Cloud Region:** US-East (assumed)
- **Estimated CO₂:** ~0.5g (negligible — text generation is extremely low-carbon)

## Issues / Follow-ups

### Edge Cases Noted
1. **Nonce replay window:** Currently 5 seconds. May need adjustment based on real-world usage patterns.
2. **Broadcast mute enforcement:** Now correctly filters per-subscriber. Future optimization: cache mute states to avoid O(n) lookups on every broadcast.
3. **Tree walking:** `_findNode()` and `_walkTree()` use depth-first recursion. For extremely deep trees (100+ levels), consider iterative approach.

### Dependencies for Future Tasks
- **Event Ledger Bridge (future task):** MessageBus dispatches `LOG_EVENT` actions, but the bridge to backend Event Ledger (TASK-001) is not yet implemented. This is intentional — the bus logs events to the reducer, and a separate bridge task will connect to the backend.
- **Governance Dashboard:** GovernanceProxy logs `GOVERNANCE_BLOCKED` events. A governance dashboard UI (future task) will visualize these blocks for debugging/audit.

### Recommended Next Tasks
1. **TASK-006: Gate Enforcer** — Autonomous action gate that enforces `require_human` conditions before executing destructive/sensitive actions
2. **Event Ledger Bridge** — Connect MessageBus LOG_EVENT dispatches to backend Event Ledger writer
3. **Shell UI Integration** — Integrate relay_bus into shell reducer and pane chrome (mute toggle UI, bus routing)
4. **Performance Benchmarking** — Test bus throughput with 100+ subscribers, 1000+ messages/sec to identify bottlenecks

### Code Quality Notes
- **Line counts:** All files under 500 lines (largest: messageBus.ts at 282 lines)
- **Test coverage:** 115 tests cover all critical paths (pub/sub, mute, governance, permissions)
- **TypeScript strict mode:** No `any` types except legacy message fields (`payload`, `fromPaneId`, etc. for backward compatibility)
- **No hardcoded colors:** No CSS in this infrastructure — bus is pure logic

---

**Task completed successfully. All deliverables met. All tests passing. Ready for integration.**
