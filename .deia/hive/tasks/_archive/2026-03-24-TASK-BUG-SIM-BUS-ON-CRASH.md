# TASK-BUG-SIM-BUS-ON-CRASH: Fix "bus.on is not a function" crash in Sim EGG

## Objective

Find and fix the runtime crash in the Sim EGG where something is calling `bus.on()` (EventEmitter API) instead of the correct MessageBus API (`bus.subscribe()`).

## Context

The Sim EGG crashes at runtime with the error:
```
bus.on is not a function
```

Key findings from prior investigation:
1. **NO source-level violations exist** — a prior bus API sweep (TASK-BUS-API-SWEEP) found ZERO instances of `.on()`, `.off()`, or `.emit()` in the codebase
2. MessageBus does NOT have `.on()` method — it uses `.subscribe()` (verified by compliance tests)
3. This is a RUNTIME issue, not a source code issue
4. The error originates in "sim-pane" according to the briefing

Likely root causes:
- A component receiving the wrong object as `bus` (e.g., getting shell context but accessing it incorrectly)
- A dependency or adapter expecting EventEmitter-style API instead of MessageBus API
- Something in the sim adapter chain passing a non-bus object
- Shell context not providing `bus` correctly, or providing a different object

The Sim EGG is a single full-screen pane layout (`eggs/sim.egg.md`). The adapter is `simAdapter.tsx` which maps `AppRendererProps` to `FlowDesigner` props. `FlowDesigner` uses `useShell()` to get the shell context, then extracts `bus` from it (line 71-72 in FlowDesigner.tsx).

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md` (EGG definition)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\simAdapter.tsx` (app adapter)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (main component, uses `useShell()`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\useShell.tsx` (shell hook)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\Shell.tsx` (shell context provider)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts` (MessageBus implementation)

## Deliverables

### 1. Root Cause Identification
- [ ] Reproduce the crash in a test or local dev environment
- [ ] Identify the EXACT line/component where `.on()` is called
- [ ] Determine what object is being called with `.on()` and why it's not a MessageBus
- [ ] Identify the full call stack

### 2. Fix Implementation
- [ ] Fix the root cause
- [ ] Ensure `bus` is correctly typed as `MessageBus | null`
- [ ] Ensure all bus access goes through correct API (`subscribe()`, `send()`)
- [ ] If a dependency is using `.on()`, wrap it or replace it

### 3. Regression Tests
- [ ] Write tests that reproduce the original crash
- [ ] Write tests that verify the fix
- [ ] Ensure sim.egg.md loads without crash
- [ ] Test bus message routing in sim context

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Shell context returns `null` bus
  - Shell context returns `undefined`
  - MessageBus subscribe/send calls work correctly
  - Sim EGG loads without crash

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only (if CSS changes needed)
- No stubs
- MessageBus API compliance (`.subscribe()`, `.send()`, NOT `.on()`, `.emit()`, `.off()`)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-BUG-SIM-BUS-ON-CRASH-RESPONSE.md`

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
