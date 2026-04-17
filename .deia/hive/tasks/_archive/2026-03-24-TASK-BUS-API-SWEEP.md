# TASK-BUS-API-SWEEP: Fix Incorrect MessageBus API Calls

## Objective

Find and fix ALL incorrect MessageBus API calls across `browser/src/`. The MessageBus only has `send()` and `subscribe()`. Bees have introduced calls to non-existent methods (`bus.emit()`, `bus.on()`, `bus.off()`) that cause runtime crashes.

## Context

MessageBus class (`browser/src/infrastructure/relay_bus/messageBus.ts`) has only two public methods:
- `send(message, sourcePane?)` — send a message, returns nonce
- `subscribe(paneId, handler)` — subscribe to messages, returns unsubscribe function

**Common violations:**
- `bus.emit()` — DOES NOT EXIST, use `bus.send()`
- `bus.on()` — DOES NOT EXIST, use `bus.subscribe()`
- `bus.off()` — DOES NOT EXIST, `subscribe()` returns unsubscribe function

**MessageEnvelope shape:**
```typescript
{
  type: string
  sourcePane: string
  target: string | '*'
  nonce: string
  timestamp: string
  data?: unknown
}
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.test.ts`

## Deliverables

- [ ] Search all `.ts` and `.tsx` files under `browser/src/` for violations:
  - `bus.emit(`
  - `bus.on(`
  - `bus.off(`
  - Any other bus method call not `.send(` or `.subscribe(`
- [ ] Fix all violations found:
  - Replace `bus.emit(type, data)` with `bus.send({ type, data, target: '*' })`
  - Replace `bus.on(type, handler)` with `const unsub = bus.subscribe(paneId, (msg) => { if (msg.type === type) handler(msg) })`
  - Replace `bus.off(type, handler)` with unsubscribe function pattern
- [ ] Test file: `browser/src/infrastructure/relay_bus/__tests__/bus-api-violations.test.tsx` (6+ tests)
- [ ] All existing tests pass
- [ ] Violation report: list every file fixed with line numbers and before/after snippets

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - `bus.emit()` with 0 args (should error)
  - `bus.emit()` with 1 arg (type only)
  - `bus.emit()` with 2 args (type + data)
  - `bus.on()` with handler function
  - `bus.off()` removing listener
  - Unsubscribe function called multiple times (idempotent)
  - Subscribe → unsubscribe → re-subscribe (new subscription)
  - Multiple subscriptions to same paneId (all receive messages)
- [ ] Minimum 6 test cases
- [ ] No existing tests broken

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — fully implement all functions
- Do NOT modify messageBus.ts API — fix caller code only
- Do NOT change message envelope format — use existing MessageEnvelope type
- Do NOT add backward-compatibility shims for old API — just fix the violations

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUS-API-SWEEP-RESPONSE.md`

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

## Violation Search Strategy

Use Grep tool to search for violations:
```bash
# Search for bus.emit(
grep -r "bus\.emit\(" browser/src/ --include="*.ts" --include="*.tsx"

# Search for bus.on(
grep -r "bus\.on\(" browser/src/ --include="*.ts" --include="*.tsx"

# Search for bus.off(
grep -r "bus\.off\(" browser/src/ --include="*.ts" --include="*.tsx"
```

For each violation found:
1. Read the file
2. Understand the intent
3. Write a test for the correct behavior
4. Fix the violation
5. Run tests to verify

## Replacement Patterns

### Pattern 1: bus.emit() → bus.send()
**Before:**
```typescript
bus.emit('node:selected', { nodeId: '123' })
```

**After:**
```typescript
bus.send({
  type: 'node:selected',
  sourcePane: paneId,
  target: '*',
  data: { nodeId: '123' }
})
```

### Pattern 2: bus.on() → bus.subscribe()
**Before:**
```typescript
bus.on('node:selected', (data) => {
  console.log('Node selected:', data.nodeId)
})
```

**After:**
```typescript
const unsubscribe = bus.subscribe(paneId, (msg) => {
  if (msg.type === 'node:selected') {
    console.log('Node selected:', msg.data.nodeId)
  }
})

// Store unsubscribe function for cleanup
// Call unsubscribe() when component unmounts
```

### Pattern 3: bus.off() → unsubscribe function
**Before:**
```typescript
const handler = (data) => { /* ... */ }
bus.on('node:selected', handler)
// later...
bus.off('node:selected', handler)
```

**After:**
```typescript
const unsubscribe = bus.subscribe(paneId, (msg) => {
  if (msg.type === 'node:selected') {
    // handler logic
  }
})

// later...
unsubscribe()
```

## Expected Violation Count

Based on recent canvas port work (19 bees), estimate 10-30 violations across:
- FlowDesigner.tsx
- CanvasApp.tsx
- SuggestionsTab.tsx (already has 1 violation on line 89: `bus.on()`)
- NodePalette.tsx
- Properties panel components
- Other canvas-related files

Focus search on files modified in commit 0336f49.
