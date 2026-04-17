---
features_delivered:
  - APPS-HOME-006: AppsHome component test suite (11 tests)
  - APPS-HOME-007: EggRegistryService test suite (10 tests)
  - APPS-HOME-008: parseEggFrontmatter test suite (17 tests)
features_modified: []
features_broken: []
test_summary:
  total: 38
  passed: 38
  failed: 0
---

# TASK-T5: Tests for AppsHome + EggRegistryService — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-14

---

## Files Modified

**Created (3 test files):**
- `browser/src/primitives/apps-home/__tests__/AppsHome.test.tsx` (177 lines, 11 tests)
- `browser/src/services/egg-registry/__tests__/eggRegistryService.test.ts` (128 lines, 10 tests)
- `browser/src/services/egg-registry/__tests__/parseEggFrontmatter.test.ts` (275 lines, 17 tests)

---

## What Was Done

### AppsHome Component Tests (11 tests)
- 1.1: Renders correct number of cards (14) when given full mock data
- 1.2: Each card shows displayName, description, status badge, and version
- 1.3: Section headers render for each group ("Core Products", "Productivity", "Platform Tools")
- 1.4: Cards are grouped under correct section headers
- 1.5: Search input filters cards by displayName (case-insensitive)
- 1.6: Search input filters cards by description (case-insensitive)
- 1.7: Search input filters cards by egg ID (case-insensitive)
- 1.8: Empty state shows "No apps match your search" when search matches nothing
- 1.9: Card click calls `window.location.href` for cards with subdomain
- 1.10: Card click emits `egg:inflate` bus event for cards without subdomain
- 1.11: Cards with BUILT status have correct badge text

### EggRegistryService Tests (10 tests)
- 2.1: `getRegistry()` returns array of length 14
- 2.2: Every item has all required `EggMeta` fields
- 2.3: No item has undefined or empty egg field
- 2.4: Section mapping verified (code-default → core, writers-room → productivity, design-builder → platform)
- 2.5: Color mapping verified (code-default → purple, chat-default → green)
- 2.6: `getRegistryBySection('core')` returns 6 items
- 2.7: `getRegistryBySection('productivity')` returns 4 items
- 2.8: `getRegistryBySection('platform')` returns 4 items
- 2.9: Icon is first character of displayName for every item
- 2.10: Subdomain is `string | null` for every item (never undefined)

### parseEggFrontmatter Tests (17 tests)
- 3.1: Parses valid .egg.md frontmatter with all fields
- 3.2: Extracts egg, displayName, description, version correctly
- 3.3: Missing description defaults to empty string
- 3.4: Missing version defaults to "0.0.0"
- 3.5: Missing _stub defaults to false
- 3.6: Missing displayName defaults to egg value
- 3.7: Returns null for input without frontmatter delimiters
- 3.8: Returns null for empty string
- 3.9: Handles frontmatter with extra whitespace
- 3.10: Derives icon from first character of displayName
- 3.11: Parses content after frontmatter without affecting extracted values
- 3.12: Handles _stub: true correctly
- 3.13: Handles alternative field names (id, display_name, title)
- 3.14: Returns null when egg field is missing
- 3.15: Handles quoted values in frontmatter
- 3.16: Skips lines with comments in frontmatter
- 3.17: Handles frontmatter with only one delimiter (invalid)

### Testing Patterns Followed
- Used `vitest` + `@testing-library/react` for component tests
- Followed patterns from `KanbanPane.test.tsx` for component testing
- Used real registry data from `getRegistry()` for integration-like testing
- Created minimal bus mock with `vi.fn()` for event testing
- Used `within()` helper to scope queries to specific card elements
- All assertions explicit (no snapshot tests)
- Comprehensive edge case coverage for parser

---

## Test Results

```
Test Files  3 passed (3)
     Tests  38 passed (38)
```

### Breakdown:
- **AppsHome.test.tsx**: 11 tests passed
- **eggRegistryService.test.ts**: 10 tests passed
- **parseEggFrontmatter.test.ts**: 17 tests passed

### Full Browser Test Suite:
- **Total**: 2207 passed (38 new from this task)
- **Failed**: 10 (pre-existing, unrelated to this task)
- **Skipped**: 1
- **Files**: 151 passed, 6 failed (pre-existing)

---

## Build Verification

### Vitest Run Summary:
```
Test Files  3 passed (3)
     Tests  38 passed (38)
  Duration  8.63s
```

### Line Counts (all under 500-line limit):
- AppsHome.test.tsx: 177 lines
- eggRegistryService.test.ts: 128 lines
- parseEggFrontmatter.test.ts: 275 lines
- **Total**: 580 lines across 3 files

---

## Acceptance Criteria

- [x] All tests pass (`npx vitest run`)
- [x] AppsHome tests: at least 10 test cases covering rendering, search, clicks, empty state (11 delivered)
- [x] eggRegistryService tests: at least 8 test cases covering data shape, mappings, filters (10 delivered)
- [x] parseEggFrontmatter tests: at least 8 test cases covering parsing, defaults, edge cases (17 delivered)
- [x] No snapshot tests — explicit assertions only
- [x] No file exceeds 500 lines (max: 275 lines)
- [x] No hardcoded colors in test assertions — used scoped `within()` queries instead

### Additional Coverage Beyond Spec:
- Added 7 extra tests for parseEggFrontmatter (17 vs 8 required) for comprehensive edge case coverage
- Added 2 extra tests for eggRegistryService (10 vs 8 required)
- Added 1 extra test for AppsHome (11 vs 10 required)

---

## Clock / Cost / Carbon

**Clock**: 22:18:00 - 22:21:00 (3 minutes)
**Cost**: ~$0.15 (Sonnet 4.5: 66k input, 4k output)
**Carbon**: ~0.8g CO₂e (GPU inference + data transfer)

---

## Issues / Follow-ups

### None — Task Complete

All acceptance criteria met. All tests passing. No edge cases or blockers identified.

### Notes:
1. **Holdout-set QA validation complete**: Tests written from scratch against acceptance criteria without looking at T2/T3 inline tests
2. **Real data used**: Tests use `getRegistry()` output for integration-like validation
3. **Pattern consistency**: Followed existing patterns from `KanbanPane.test.tsx` and `TerminalApp.paneNav.test.tsx`
4. **Comprehensive coverage**: 38 tests total, exceeding minimums across all 3 test suites

### Recommended Next Steps:
- **T2 + T3 integration**: Verify T2 (AppsHome component) and T3 (registry service) passed their own tests
- **Apps-home EGG wiring**: Hook up apps-home.egg.md to the shell and verify rendering
- **E2E testing**: Create smoke test for apps.shiftcenter.com subdomain routing
