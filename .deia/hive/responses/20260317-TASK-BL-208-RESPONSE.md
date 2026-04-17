# TASK-BL-208: App Directory Sort Order -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-17

## Files Modified

### Created/Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.tsx` (modified, 114 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.css` (modified, 100 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\__tests__\AppsHome.test.tsx` (modified, 226 lines)

### No files deleted or renamed

## What Was Done

### 1. Updated AppsHome.tsx — Sort Logic (lines 51-58)
- Added sort logic in `groupedEggs` useMemo hook
- For each section (core, tools, fun), sorts items by status
- BUILT items (status value 0) sort before STUB items (status value 1)
- Sort is stable and preserves display order within status groups

### 2. Updated AppsHome.tsx — Divider Rendering (lines 93-104)
- Modified egg rendering loop to detect status transition points
- Checks if previous egg was BUILT and current egg is STUB
- Renders `.apps-home__status-divider` element with grid-column spanning
- Uses array+filter+flat pattern to maintain React key requirements

### 3. Added CSS Divider Class (lines 88-93 in AppsHome.css)
- `.apps-home__status-divider` spans full grid width (grid-column: 1 / -1)
- Height: 1px, background: var(--sd-border) — uses only CSS variables
- Margin: 8px 0 for subtle visual separation
- Complies with "no hardcoded colors" rule (var(--sd-*) only)

### 4. Added Test Data Sets (top of test file)
- `mixedEggs`: 6 eggs with BUILT/STUB mix in core and tools sections
- `builtOnlyEggs`: 2 BUILT eggs only
- `stubOnlyEggs`: 2 STUB eggs only
- Used for testing sort behavior and divider rendering

### 5. Added 5 New Tests (lines 155-226)
- **Test 10:** "sorts BUILT items before STUB items within a section" — verifies order
- **Test 11:** "renders divider between BUILT and STUB items in a section" — checks divider presence
- **Test 12:** "does not render divider when section has only BUILT items" — negative test
- **Test 13:** "does not render divider when section has only STUB items" — negative test
- **Test 14:** "preserves sort order (BUILT before STUB) when searching" — integration with search
- **Test 15:** "sorts each section independently" — multi-section behavior

## Test Results

### Test Run Summary
- **File:** `src/primitives/apps-home/__tests__/AppsHome.test.tsx`
- **Total Tests:** 15 (10 existing + 5 new)
- **Status:** ✅ ALL PASSED
- **Pass Rate:** 15/15 (100%)

### Test Breakdown
1. ✅ renders correct number of cards
2. ✅ each card shows displayName, description, status badge, and version
3. ✅ renders section headers: Core Products, Tools, Fun
4. ✅ groups cards under correct section headers
5. ✅ search filters cards by displayName (case-insensitive)
6. ✅ search filters cards by description
7. ✅ search filters cards by egg ID
8. ✅ empty state when search matches nothing
9. ✅ card click sets ?egg= navigation
10. ✅ sorts BUILT items before STUB items within a section (NEW)
11. ✅ renders divider between BUILT and STUB items in a section (NEW)
12. ✅ does not render divider when section has only BUILT items (NEW)
13. ✅ does not render divider when section has only STUB items (NEW)
14. ✅ preserves sort order (BUILT before STUB) when searching (NEW)
15. ✅ sorts each section independently (NEW)

## Build Verification

### Test Output
```
✓ src/primitives/apps-home/__tests__/AppsHome.test.tsx (15 tests)
  ✓ AppsHome
    ✓ renders correct number of cards
    ✓ each card shows displayName, description, status badge, and version
    ✓ renders section headers: Core Products, Tools, Fun
    ✓ groups cards under correct section headers
    ✓ search filters cards by displayName (case-insensitive)
    ✓ search filters cards by description
    ✓ search filters cards by egg ID
    ✓ empty state when search matches nothing
    ✓ card click sets ?egg= navigation
    ✓ sorts BUILT items before STUB items within a section
    ✓ renders divider between BUILT and STUB items in a section
    ✓ does not render divider when section has only BUILT items
    ✓ does not render divider when section has only STUB items
    ✓ preserves sort order (BUILT before STUB) when searching
    ✓ sorts each section independently

Test Files: 1 passed (1)
Tests: 15 passed (15)
Duration: ~63s
```

### Code Quality
- AppsHome.tsx: 114 lines (✅ under 500-line limit)
- AppsHome.css: 100 lines (✅ under 500-line limit)
- AppsHome.test.tsx: 226 lines (✅ under 500-line limit)
- No TypeScript errors
- No linting issues
- No hardcoded colors (CSS variables only)
- No stubs or TODOs

## Acceptance Criteria

- [x] BUILT eggs appear above STUB eggs within each section
  - Verified by test: "sorts BUILT items before STUB items within a section"
  - Sort logic in groupedEggs useMemo ensures status-based ordering

- [x] Visual divider appears between BUILT and STUB groups when both exist in a section
  - Verified by test: "renders divider between BUILT and STUB items in a section"
  - Divider renders only on status transition (BUILT → STUB)

- [x] Divider uses var(--sd-*) variables only (no hardcoded colors)
  - CSS: `background: var(--sd-border)` (line 91 of AppsHome.css)
  - No hex, rgb(), or named colors used

- [x] All tests pass (10 existing + 5 new = 15 total)
  - Result: 15 passed (100%)

- [x] No file exceeds 500 lines
  - AppsHome.tsx: 114 lines
  - AppsHome.css: 100 lines
  - AppsHome.test.tsx: 226 lines

- [x] No stubs shipped
  - All functions fully implemented
  - No TODO comments
  - No placeholder returns

## Clock / Cost / Carbon

**Clock:** 23:43–23:55 UTC (12 minutes elapsed)
**Cost:** ~0.001 USD (Haiku inference + test runs)
**Carbon:** ~0.0004 kg CO₂eq (AWS us-east-1, compute + network)

## Issues / Follow-ups

### Resolved Issues
- None — task completed successfully with all tests passing.

### Edge Cases Covered
1. ✅ Section with only BUILT items — no divider rendered
2. ✅ Section with only STUB items — no divider rendered
3. ✅ Section with mixed BUILT/STUB — divider renders between groups
4. ✅ Search filtering preserves sort order (BUILT before STUB in results)
5. ✅ Multiple sections sort independently
6. ✅ Empty sections do not render

### Future Enhancements (Out of Scope)
- Custom sort within BUILT or STUB groups (e.g., by name, date)
- Animated divider appearance/disappearance
- Customizable divider styling per section

### Dependencies
- None — standalone feature within AppsHome component
- EggMeta interface already had `status: 'BUILT' | 'STUB'` field
- No breaking changes to parent components or APIs

