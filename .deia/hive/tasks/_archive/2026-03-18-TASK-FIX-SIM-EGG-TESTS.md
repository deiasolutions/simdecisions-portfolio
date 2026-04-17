# TASK-FIX-SIM-EGG-TESTS: Fix 11 Failing Sim EGG Tests

## Objective

Fix 11 failing sim EGG tests across 4 test files by: (1) adding `registerApps()` call to test setup file, (2) adding missing `defaultDocuments: []` to sim.egg.md startup block, and (3) adding 'chat-history' to AUTO_EXPAND_ADAPTERS constant.

## Context

From full test sweep (`.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md`):

**Browser test failures (Sim EGG section):**
- `simEggIntegration.test.ts` (5 failures) — "startup.defaultDocuments must be an array"
- `simEgg.load.test.tsx` (3 failures) — "SimAdapter not registered"
- `simEgg.minimal.test.ts` (1 failure) — "expected undefined not to be undefined"
- `treeBrowserAdapter.autoExpand.test.ts` (2 failures) — AUTO_EXPAND_ADAPTERS missing 'chat-history'

**Root causes:**
1. Test setup file (`browser/src/infrastructure/relay_bus/__tests__/setup.ts`) does NOT call `registerApps()`, so SimAdapter is never registered when tests run
2. `sim.egg.md` startup block has `sessionRestore: false` but is missing `defaultDocuments: []` array (required by eggInflater validation)
3. `AUTO_EXPAND_ADAPTERS` constant in `treeBrowserAdapter.tsx` is missing 'chat-history' adapter

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\setup.ts` — Test setup file (18 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md` — Sim EGG config (startup block missing defaultDocuments)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` — AUTO_EXPAND_ADAPTERS constant (line 1)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` — registerApps() function
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggInflater.ts` — Validation logic for defaultDocuments (lines 64-70)

## Deliverables

- [x] Add `import { registerApps } from '../../apps'` to `browser/src/infrastructure/relay_bus/__tests__/setup.ts`
- [x] Call `registerApps()` in setup.ts after mocks and polyfills
- [x] Add `defaultDocuments: []` to sim.egg.md startup block (empty array is valid)
- [x] Add 'chat-history' to AUTO_EXPAND_ADAPTERS Set in `browser/src/apps/treeBrowserAdapter.tsx` (line 1)
- [x] Run all 4 failing test files and confirm all 11 failures → 11 passes
- [x] Write response file

## Test Requirements

**Before fixes (baseline):**
```bash
cd browser
npx vitest run src/eggs/__tests__/simEggIntegration.test.ts  # 5 failures
npx vitest run src/shell/__tests__/simEgg.load.test.tsx      # 3 failures
npx vitest run src/eggs/__tests__/simEgg.minimal.test.ts     # 1 failure
npx vitest run src/apps/__tests__/treeBrowserAdapter.autoExpand.test.ts  # 2 failures
```

**After fixes (expected):**
- `simEggIntegration.test.ts` — 6 tests passing (0 failures)
- `simEgg.load.test.tsx` — 4 tests passing (0 failures)
- `simEgg.minimal.test.ts` — 1 test passing (0 failures)
- `treeBrowserAdapter.autoExpand.test.ts` — All tests passing (chat-history related: 2 tests)

**Total:** 11 tests must pass (currently failing)

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (not applicable for this task)
- No stubs
- TDD: verify tests pass after fixes

## Changes Checklist

**File 1: `browser/src/infrastructure/relay_bus/__tests__/setup.ts`**
```typescript
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import { registerApps } from '../../apps'  // ADD THIS LINE

// Mock p5 — its transitive dep gifenc is CJS-only and breaks ESM import
// Ported from platform/simdecisions-2/src/test/setup.ts
vi.mock('p5', () => ({
  default: vi.fn(function(this: any, sketch: any) {
    this.remove = vi.fn();
  }),
}));

// Polyfill ResizeObserver for jsdom (required by ReactFlow)
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Register all app adapters so tests can use getAppRenderer()
registerApps()  // ADD THIS LINE
```

**File 2: `eggs/sim.egg.md`**
Change startup block from:
```yaml
```startup
{
  "sessionRestore": false
}
```

To:
```yaml
```startup
{
  "sessionRestore": false,
  "defaultDocuments": []
}
```

**File 3: `browser/src/apps/treeBrowserAdapter.tsx`**
Change line 1 from:
```typescript
const AUTO_EXPAND_ADAPTERS = new Set(['channels', 'members', 'palette', 'bus'])
```

To:
```typescript
const AUTO_EXPAND_ADAPTERS = new Set(['channels', 'members', 'palette', 'bus', 'chat-history'])
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-FIX-SIM-EGG-TESTS-RESPONSE.md`

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
