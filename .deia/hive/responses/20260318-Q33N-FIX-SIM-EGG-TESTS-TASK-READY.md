# Q33N Response: Fix Sim EGG Tests Task File Ready

**To:** Q33NR (Regent)
**From:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Bot ID:** QUEEN-2026-03-18-BRIEFING-FIX-SIM-EG

---

## Task File Created

**File:** `.deia/hive/tasks/2026-03-18-TASK-FIX-SIM-EGG-TESTS.md`

---

## Summary

I've analyzed the 11 failing sim EGG tests and identified three root causes:

1. **Test setup missing `registerApps()` call** — SimAdapter exists and is registered in `browser/src/apps/index.ts`, but the test setup file (`browser/src/infrastructure/relay_bus/__tests__/setup.ts`) never calls `registerApps()`, so when tests run, the app registry is empty.

2. **sim.egg.md missing defaultDocuments array** — The eggInflater validates that `startup.defaultDocuments` must be an array. The sim.egg.md has a startup block with `sessionRestore: false` but no `defaultDocuments` field. Adding `"defaultDocuments": []` fixes the validation error.

3. **AUTO_EXPAND_ADAPTERS missing 'chat-history'** — The test expects 'chat-history' to be in the AUTO_EXPAND_ADAPTERS Set, but the constant in `treeBrowserAdapter.tsx` only has: `['channels', 'members', 'palette', 'bus']`.

---

## Files to Modify

**3 files total:**

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\setup.ts`
   - Add import: `import { registerApps } from '../../apps'`
   - Add call: `registerApps()` after polyfills

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md`
   - Change startup block from `{ "sessionRestore": false }` to `{ "sessionRestore": false, "defaultDocuments": [] }`

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`
   - Change line 1 from `const AUTO_EXPAND_ADAPTERS = new Set(['channels', 'members', 'palette', 'bus'])` to include 'chat-history'

---

## Test Coverage

**Before fixes:**
- `simEggIntegration.test.ts` — 5 failures
- `simEgg.load.test.tsx` — 3 failures
- `simEgg.minimal.test.ts` — 1 failure
- `treeBrowserAdapter.autoExpand.test.ts` — 2 failures (chat-history related)

**After fixes:**
- All 11 tests should pass

---

## Model Assignment

**Haiku** — per briefing

---

## Ready for Review

The task file is complete with:
- ✅ Clear objective (one sentence)
- ✅ Root cause analysis
- ✅ All file paths (absolute)
- ✅ Exact code changes (before/after)
- ✅ Test requirements (4 test files, 11 tests total)
- ✅ Response file requirements (8 mandatory sections)
- ✅ Constraints (no stubs, TDD, file size limits)

Awaiting Q33NR approval to dispatch haiku bee.
