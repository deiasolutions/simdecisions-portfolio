# SPEC: Fix BUG-022-B paletteClickToPlace tests — _dispatch not a function

## Objective

Fix 8 failing tests in `browser/src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`. All fail with `TypeError: this._dispatch is not a function` at `messageBus.ts:217`.

## Root Cause

The test creates a `MessageBus` instance but the bus now requires a `_dispatch` function (added by the event ledger integration). The test's bus setup doesn't provide it.

## Files to Read First

- `browser/src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`
- `browser/src/infrastructure/relay_bus/messageBus.ts` (line 217 — where `_dispatch` is called)
- Look at other passing test files that use MessageBus for the correct mock/setup pattern (e.g. `browser/src/infrastructure/relay_bus/__tests__/messageBus.crossWindow.test.ts`)

## Deliverables

- [ ] Fix the MessageBus construction in paletteClickToPlace.test.tsx so `_dispatch` is available
- [ ] All 10 tests in paletteClickToPlace.test.tsx pass (8 currently failing + 2 passing)
- [ ] No regressions in TreeNodeRow icon tests (15 tests must still pass)
- [ ] Run: `cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx src/primitives/tree-browser/__tests__/TreeNodeRow.palette-icons.integration.test.tsx`

## Constraints

- Only modify the test file. Do NOT change messageBus.ts or any production code.
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Test Requirements

- [ ] All 10 paletteClickToPlace tests pass
- [ ] All 15 TreeNodeRow icon tests still pass
- [ ] Total: 25 passing, 0 failing
