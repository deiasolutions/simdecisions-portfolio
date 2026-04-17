# TASK-EFEMERA-CONN-06: Wire Connector into EGG Lifecycle

## Objective
Wire the EfemeraConnector into the EGG initialization system so it starts when the efemera EGG loads and stops when the EGG unloads. Update the efemera.egg.md permissions block to use the new `efemera:*` bus event namespace.

## Context
The EfemeraConnector (CONN-02) is a plain class with `start()` and `stop()` methods. It needs to be instantiated when the efemera EGG layout is rendered, with:
- The shell's MessageBus instance
- The pane nodeIds from the layout config (efemera-channels, efemera-messages, efemera-compose, efemera-members)
- User info from auth context (or defaults)
- Settings from the EGG's `settings` block (pollingInterval, presenceAutoIdle)

**Depends on:** TASK-EFEMERA-CONN-02 (connector class must exist).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (EGG init hook)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\Shell.tsx` (shell component)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\ShellContext.tsx` (shell context)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md` (EGG config)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\EfemeraConnector.ts` (created by CONN-02)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260328-EFEMERA-CONNECTOR-DESIGN.md` (Section 6)

## Deliverables

### 1. Create connector lifecycle hook or integrate into existing EGG init

Determine the best integration point by reading the shell init code. Two options:

**Option A: New hook `useEfemeraConnector.ts`**
- React hook that creates the connector, starts it on mount, stops it on unmount
- Called from the shell or EGG wrapper component when `egg === 'efemera'`

**Option B: Service registration in existing EGG init**
- Extend `useEggInit.ts` with a service lifecycle pattern
- When EGG config has `settings.pollingInterval` (or similar marker), instantiate the connector

Choose the approach that is simplest and least invasive. Document your choice in the response file.

- [ ] Connector instantiated with: bus, paneIds from layout, userId/displayName from auth or defaults, settings from EGG settings block
- [ ] Connector `start()` called after bus and panes are ready
- [ ] Connector `stop()` called on EGG unload / component unmount
- [ ] Cleanup is reliable (no leaked intervals, no orphaned subscriptions)

### 2. Update `eggs/efemera.egg.md` permissions block

- [ ] Replace old `bus_emit` list with new `efemera:*` events:
  ```
  "bus_emit": [
    "efemera:channel-select",
    "efemera:message-send",
    "efemera:channel-create",
    "efemera:presence-update",
    "efemera:typing-start",
    "efemera:typing-stop"
  ]
  ```
- [ ] Replace old `bus_receive` list with new `efemera:*` events:
  ```
  "bus_receive": [
    "efemera:channels-loaded",
    "efemera:channel-changed",
    "efemera:messages-loaded",
    "efemera:message-received",
    "efemera:message-sent",
    "efemera:members-loaded",
    "efemera:presence-changed",
    "efemera:typing",
    "efemera:typing-stop",
    "efemera:error",
    "efemera:ready",
    "terminal:text-patch"
  ]
  ```
- [ ] Keep `terminal:text-patch` in bus_receive (still used by non-efemera bus handlers in text-pane)

### 3. Delete `browser/src/services/efemera/relayPoller.ts`

- [ ] relayPoller.ts is now fully absorbed into messageService.ts (CONN-01)
- [ ] Remove any imports of RelayPoller from other files
- [ ] Verify no other code references relayPoller

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Test the lifecycle hook/integration:
  - Connector starts when efemera EGG mounts
  - Connector stops when efemera EGG unmounts
  - Connector receives correct paneIds from layout
  - Connector receives correct settings from EGG config
  - Non-efemera EGGs do NOT instantiate the connector
- [ ] Existing browser tests still pass

## Constraints
- No file over 500 lines
- No stubs
- Minimize changes to Shell.tsx and useEggInit.ts — prefer creating a new hook if possible
- The connector lifecycle must be tied to React component lifecycle (useEffect cleanup) to prevent leaks
- Do NOT modify EfemeraConnector.ts itself — it was built in CONN-02
- This task is about WIRING, not building the connector

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-06-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
