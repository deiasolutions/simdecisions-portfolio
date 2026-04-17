# Briefing: Fix Sim EGG Tests (11 failing)

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Model Assignment:** haiku
**Priority:** P1

## Objective

Fix 11 failing sim EGG tests across 4 test files. Tests report "SimAdapter not registered" and "startup.defaultDocuments must be an array" errors.

## Context

Full test sweep report (.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md) shows:

**Failures:**
- simEggIntegration.test.ts (5 failures) — "startup.defaultDocuments must be an array"
- simEgg.load.test.tsx (3 failures) — "SimAdapter not registered"  
- simEgg.minimal.test.ts (1 failure) — "expected undefined not to be undefined"
- treeBrowserAdapter.autoExpand.test.ts (2 failures) — AUTO_EXPAND_ADAPTERS missing 'chat-history'

## Investigation Results (Q33NR)

I've read the relevant files:

1. **SimAdapter IS registered** — browser/src/apps/index.ts line 45 registers sim → SimAdapter
2. **SimAdapter exists** — browser/src/apps/simAdapter.tsx exports SimAdapter component
3. **Setup calls registerApps()** — browser/src/infrastructure/relay_bus/__tests__/setup.ts line 21
4. **AUTO_EXPAND_ADAPTERS includes chat-history** — browser/src/apps/treeBrowserAdapter.tsx line 39
5. **sim.egg.md has valid startup block** — eggs/sim.egg.md lines 80-85 show valid JSON

## What Q33N Should Do

1. **Run the failing tests** individually to see actual error messages
2. **Check test output** for exact error location and stack traces
3. **Write task files** to fix the actual root cause (NOT hypothesized cause)

## Files Q33N Must Read

- browser/src/eggs/__tests__/simEggIntegration.test.ts
- browser/src/eggs/__tests__/simEgg.minimal.test.ts
- browser/src/apps/__tests__/treeBrowserAdapter.autoExpand.test.ts
- browser/src/apps/simAdapter.tsx
- browser/src/apps/index.ts
- browser/src/infrastructure/relay_bus/__tests__/setup.ts
- browser/src/eggs/eggInflater.ts
- browser/src/apps/treeBrowserAdapter.tsx
- eggs/sim.egg.md

## Success Criteria

- All 11 failing tests pass
- No new test failures introduced
- Test output shows clear pass results

---

**Q33NR NOTE:** This briefing is based on investigation. Q33N should run tests first to get real error messages, then write task files based on actual failures.
