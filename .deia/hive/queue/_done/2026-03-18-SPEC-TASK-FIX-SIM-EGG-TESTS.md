# Fix Sim EGG Tests (11 failing)

## Priority
P1

## Model Assignment
haiku

## Objective
Fix 11 failing sim EGG tests across 4 test files. SimAdapter not registered in app registry.

## What's Broken
- `simEggIntegration.test.ts` (5 failures) — "startup.defaultDocuments must be an array"
- `simEgg.load.test.tsx` (3 failures) — "SimAdapter not registered"
- `simEgg.minimal.test.ts` (1 failure) — "expected undefined not to be undefined"
- `treeBrowserAdapter.autoExpand.test.ts` (2 failures) — AUTO_EXPAND_ADAPTERS missing 'chat-history'

Reference: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` section "Sim EGG"

## Files to Read First
- `browser/src/shell/components/appRegistry.ts`
- `browser/src/eggs/` — sim egg related files
- The failing test files listed above

## What To Do
1. Read appRegistry.ts to see registered adapters
2. Find SimAdapter and register it if missing
3. Fix defaultDocuments array issue
4. Add 'chat-history' to AUTO_EXPAND_ADAPTERS
5. Run all 4 test files and confirm fixes

## Response
Write response to: `.deia/hive/responses/20260318-FIX-SIM-EGG-TESTS.md`
