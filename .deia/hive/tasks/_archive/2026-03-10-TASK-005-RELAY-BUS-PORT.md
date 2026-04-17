# TASK-005: Relay Bus — Port Cross-Pane Message Bus + Governance

## Objective

Port the in-memory message bus and governance system from the old repo to `browser/src/infrastructure/relay_bus/`. This is the cross-pane pub/sub that everything in the browser talks through. Every pane communicates via the bus. Every message is governed: logged to ledger, checked against emit/receive whitelists, mute levels enforced.

## Dependencies

- None for the port itself — this is pure frontend infrastructure.
- The bus dispatches `LOG_EVENT` actions which will eventually bridge to the backend Event Ledger (TASK-001), but the bus itself doesn't import the ledger directly. The bridge is a future task.

## Source Files

Port from `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`:

| Source Path | Dest Path | Lines | What It Does |
|-------------|-----------|-------|-------------|
| `components/shell/shell.context.js` | `relay_bus/messageBus.ts` | 186 | `MessageBus` class: pub/sub, nonce replay protection, telemetry metrics, tree-aware pane routing |
| `components/shell/GovernanceProxy.tsx` | `relay_bus/GovernanceProxy.tsx` | 160 | React wrapper: intercepts `send()` against `bus_emit` whitelist, filters `subscribe()` against `bus_receive` whitelist, logs governance blocks |
| `types/shellMessages.ts` | `relay_bus/types/messages.ts` | 101 | `MessageEnvelope` interface, typed message payloads, `isValidMessageEnvelope()` validator |
| `components/shell/shell.constants.js` | `relay_bus/constants.ts` | ~50 | `BUS_MESSAGE_TYPES`, `BUS_MUTE_CYCLE`, `BUS_MUTE_LABELS`, `BUS_MUTE_ICONS` — bus constants ONLY, strip out themes/CSS/node types |
| `services/shell/permissionsResolver.ts` | `relay_bus/permissionsResolver.ts` | 198 | Computes effective permissions: trust tier → EGG ceiling → node tightening (intersection logic) |
| `types/permissions.ts` | `relay_bus/types/permissions.ts` | 68 | `EggPermissions`, `NodePermissions`, `ResolvedPermissions`, `RequireHumanCondition`, `AutonomyConfig` |
| `services/shell/configEggCache.ts` | `relay_bus/configEggCache.ts` | 46 | In-memory cache for boot-loaded config EGGs (dependency of permissionsResolver) |

## Port Rules

### 1. Convert JS → TS

`shell.context.js` and `shell.constants.js` are plain JS. Convert to TypeScript with proper types during port. The `MessageBus` class should have typed methods:

```typescript
class MessageBus {
  subscribe(paneId: string, handler: (msg: MessageEnvelope) => void): () => void
  send(message: Partial<MessageEnvelope>, sourcePane?: string): string | null
  // ...
}
```

### 2. Fix imports

All old imports reference `../../types/permissions`, `./shell.context`, `./shell.utils.js`, etc. Update to local paths within `relay_bus/`.

Key import changes:
- `GovernanceProxy.tsx` imports `ShellCtx, useShell` from `./shell.context` → import from `./messageBus`
- `GovernanceProxy.tsx` imports `ResolvedPermissions` from `../../types/permissions` → import from `./types/permissions`
- `permissionsResolver.ts` imports `configEggCache` from `./configEggCache` → same (no change needed)
- `permissionsResolver.ts` imports permission types from `../../types/permissions` → import from `./types/permissions`

### 3. Extract bus constants only

`shell.constants.js` is 246 lines with themes, CSS, animations, node types, etc. **Only port the bus-related constants:**
- `BUS_MUTE_CYCLE`
- `BUS_MUTE_LABELS`
- `BUS_MUTE_ICONS`
- `BUS_MESSAGE_TYPES`

Everything else (SHELL_CSS, THEMES, NODE_TYPES, LOAD_STATES, KERNEL_SERVICES, BRANCH_TYPES, Z_LAYERS) stays behind — those are shell UI concerns, not bus infrastructure.

### 4. Extract uid() utility

`MessageBus` uses `uid()` from `shell.utils.js` (line 8: `` let _seq = 0; export const uid = () => `p${Date.now()}${++_seq}` ``). Include this as a local utility in the messageBus file or a small `utils.ts` file. Do NOT port all of shell.utils.js — it's 200+ lines of tree manipulation.

### 5. ShellCtx stays with the bus

The `ShellCtx` React context and `useShell` hook are defined in `shell.context.js` alongside the MessageBus. Keep them in the ported `messageBus.ts` — the bus IS the shell context's core infrastructure.

### 6. Mute enforcement

The bus currently does NOT enforce mute levels internally — muting is handled by the reducer setting `busMute` on nodes, and PaneChrome dispatches `SET_BUS_MUTE`. For this port, add mute enforcement to the `MessageBus.send()` method:

```typescript
// In send(), before delivery:
// If target pane has busMute === 'full' → block
// If target pane has busMute === 'inbound' → block incoming to that pane
// If source pane has busMute === 'outbound' → block outgoing from that pane
// 'notifications' mute → block type === 'notification' only
```

The bus needs a `setMuteState(paneId: string, muteLevel: MuteLevel)` method so the shell can update mute levels. The bus then checks mute state during delivery.

## File Structure

```
browser/src/infrastructure/relay_bus/
├── index.ts                    -- Public exports
├── messageBus.ts               -- MessageBus class, ShellCtx, useShell, uid()
├── GovernanceProxy.tsx          -- Governance wrapper component
├── permissionsResolver.ts       -- Permission computation (trust tier → EGG → node)
├── configEggCache.ts            -- Config EGG in-memory cache
├── constants.ts                 -- BUS_MESSAGE_TYPES, BUS_MUTE_*
├── types/
│   ├── messages.ts              -- MessageEnvelope, typed payloads, validator
│   └── permissions.ts           -- EggPermissions, ResolvedPermissions, etc.
```

```
browser/src/infrastructure/relay_bus/__tests__/
├── messageBus.test.ts           -- pub/sub, nonce replay, telemetry, tree-aware routing
├── messageBus.mute.test.ts      -- mute levels: none/notifications/inbound/outbound/full
├── GovernanceProxy.test.tsx     -- intercepts send/subscribe against whitelists, platform invariants bypass
├── permissionsResolver.test.ts  -- trust tiers, EGG ceiling, node tightening, intersection logic
├── messages.test.ts             -- envelope validation, typed payloads
```

## Existing Tests to Reference

The old repo has tests at:
- `components/shell/__tests__/drag-drop.bus.test.ts` — bus message tests
- `components/shell/__tests__/governance-proxy.test.tsx` — governance proxy tests
- `services/shell/__tests__/permissionsResolver.test.ts` — permissions resolver tests
- `components/shell/__tests__/context-advertisement.test.jsx` — context advertisement via bus

Read these for patterns and expected behaviors, but write new tests adapted to the new file structure.

## Test Requirements

### messageBus.test.ts
- [ ] `subscribe()` returns unsubscribe function
- [ ] `send()` delivers to specific pane by target ID
- [ ] `send()` broadcasts to all subscribers with `target: '*'`
- [ ] `send()` rejects messages missing `type` or `target`
- [ ] `send()` generates unique `messageId` and `nonce`
- [ ] Nonce replay protection: same nonce blocked within 5s window
- [ ] `send()` dispatches `LOG_EVENT` with `kind: 'PLATFORM_PANE_MESSAGE'` for every message
- [ ] `subscribe()` + unsubscribe stops delivery
- [ ] Telemetry: `enableTelemetry()` tracks messageCount and messagesByType
- [ ] `getMetrics()` returns correct counts
- [ ] `getLastFocusedPane()` returns correct pane after `setLastFocusedByAppType()`
- [ ] `hasPaneType()` walks tree correctly

### messageBus.mute.test.ts
- [ ] `busMute: 'none'` — all messages delivered
- [ ] `busMute: 'notifications'` — only notification-type messages blocked
- [ ] `busMute: 'inbound'` — all incoming messages to pane blocked
- [ ] `busMute: 'outbound'` — all outgoing messages from pane blocked
- [ ] `busMute: 'full'` — all messages to/from pane blocked
- [ ] Mute does NOT block platform invariants (relay_bus, ledger_writer, gate_enforcer)
- [ ] `setMuteState()` updates mute level for a pane
- [ ] Mute cycle order: none → notifications → inbound → outbound → full → none

### GovernanceProxy.test.tsx
- [ ] Allowed message type passes through to real bus
- [ ] Blocked message type returns null, logs `GOVERNANCE_BLOCKED`
- [ ] `bus_emit: ['*']` allows all message types
- [ ] `bus_emit: []` blocks all non-invariant messages
- [ ] Platform invariants (`relay_bus`, `ledger_writer`, `gate_enforcer`, `settings_advertisement`, `metrics_advertisement`) always bypass governance
- [ ] `bus_receive` filtering: blocked types not delivered to handler
- [ ] Governed context replaces bus.send and bus.subscribe transparently

### permissionsResolver.test.ts
- [ ] Platform trust tier gets `tools: ['*']`, `bus_emit: ['*']`
- [ ] External trust tier gets restrictive defaults
- [ ] EGG permissions set ceiling
- [ ] Node permissions can tighten (subset of EGG)
- [ ] Node permissions cannot widen (no new capabilities)
- [ ] `require_human` conditions merge correctly (node adds, cannot remove locked)
- [ ] `max_tokens_per_session` takes minimum of EGG and node
- [ ] `buildPermissionsRegistry()` walks full tree

### messages.test.ts
- [ ] `isValidMessageEnvelope()` accepts valid envelope
- [ ] Rejects missing `type`, `sourcePane`, `target`, `nonce`
- [ ] Rejects empty strings for required fields

**Minimum: 40 tests total across all test files.**

## What NOT to Build

- No shell UI (pane chrome, split containers, drag-drop)
- No themes or CSS (those are shell concerns)
- No shell reducer (the bus dispatches actions, doesn't own the reducer)
- No actual ledger bridge to backend (future — bus dispatches LOG_EVENT actions, the bridge is separate)
- No React rendering tests beyond GovernanceProxy
- No app registry or pane manifest

## Constraints

- TypeScript (strict mode)
- React 18+ (for context, hooks)
- No external dependencies beyond React + testing libs (vitest)
- All files under 500 lines
- No stubs — every function fully implemented
- CSS: only `var(--sd-*)` custom properties if any CSS is needed (there shouldn't be)
- Test with vitest (not jest) — see `browser/` convention

## Project Setup

`browser/` directory doesn't exist yet. Create minimal structure:

```
browser/
├── package.json               -- name: "@shiftcenter/browser", react, typescript, vitest
├── tsconfig.json              -- strict mode, jsx: react-jsx
├── vitest.config.ts           -- test config
├── src/
│   └── infrastructure/
│       └── relay_bus/
│           └── (all files above)
```

`package.json` dependencies:
- `react` (18+)
- `react-dom` (18+)
- `typescript` (5+)
- Dev: `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom`, `@types/react`

## Deliverables

- [ ] `browser/package.json`
- [ ] `browser/tsconfig.json`
- [ ] `browser/vitest.config.ts`
- [ ] `browser/src/infrastructure/relay_bus/index.ts`
- [ ] `browser/src/infrastructure/relay_bus/messageBus.ts`
- [ ] `browser/src/infrastructure/relay_bus/GovernanceProxy.tsx`
- [ ] `browser/src/infrastructure/relay_bus/permissionsResolver.ts`
- [ ] `browser/src/infrastructure/relay_bus/configEggCache.ts`
- [ ] `browser/src/infrastructure/relay_bus/constants.ts`
- [ ] `browser/src/infrastructure/relay_bus/types/messages.ts`
- [ ] `browser/src/infrastructure/relay_bus/types/permissions.ts`
- [ ] `browser/src/infrastructure/relay_bus/__tests__/messageBus.test.ts`
- [ ] `browser/src/infrastructure/relay_bus/__tests__/messageBus.mute.test.ts`
- [ ] `browser/src/infrastructure/relay_bus/__tests__/GovernanceProxy.test.tsx`
- [ ] `browser/src/infrastructure/relay_bus/__tests__/permissionsResolver.test.ts`
- [ ] `browser/src/infrastructure/relay_bus/__tests__/messages.test.ts`

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-005-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
