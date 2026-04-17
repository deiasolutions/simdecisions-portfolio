# TASK-BL-208: App Directory Sort Order

## Objective
Update the App Directory (AppsHome) to sort EGGs by status within each section so BUILT items appear first, then STUB items, with a visual divider between status groups.

## Context

### Current Behavior
- AppsHome groups EGGs by section (core/tools/fun) only
- Within each section, EGGs appear in their original array order
- No status-based sorting exists
- Users cannot quickly distinguish working apps from unbuilt stubs

### What Needs to Change
- Sort EGGs within each section: BUILT first, then STUB
- Add a subtle visual divider when a section contains both BUILT and STUB items
- Preserve existing section grouping (core → tools → fun)
- Update tests to verify new sort behavior

### Architecture Overview
- **EggMeta interface** (`browser/src/services/egg-registry/types.ts`): Already has `status: 'BUILT' | 'STUB'` field
- **AppsHome component** (`browser/src/primitives/apps-home/AppsHome.tsx`): Contains `groupedEggs` useMemo that groups by section — needs sort logic added
- **AppCard component** (`browser/src/primitives/apps-home/AppCard.tsx`): Already displays status badge — no changes needed
- **CSS** (`browser/src/primitives/apps-home/AppsHome.css`): Uses var(--sd-*) variables only — new divider class needed

### Sort Logic
```typescript
// Within groupedEggs useMemo, after grouping by section:
Object.keys(groups).forEach((section) => {
  groups[section].sort((a, b) => {
    // BUILT (0) before STUB (1)
    const aVal = a.status === 'BUILT' ? 0 : 1;
    const bVal = b.status === 'BUILT' ? 0 : 1;
    return aVal - bVal;
  });
});
```

### Divider Implementation
**When to show divider:** Insert divider element between last BUILT item and first STUB item within a section.

**Implementation approach:**
- In the map over `sectionEggs`, check if previous egg was BUILT and current egg is STUB
- If true, render a `<div className="apps-home__status-divider">` before the current card

**CSS for divider (var(--sd-*) only):**
```css
.apps-home__status-divider {
  grid-column: 1 / -1;
  height: 1px;
  background: var(--sd-border);
  margin: 8px 0;
}
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.tsx` — main component, contains groupedEggs useMemo
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.css` — styling, uses var(--sd-*) only
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\__tests__\AppsHome.test.tsx` — existing tests (121 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\egg-registry\types.ts` — EggMeta interface (read-only reference)

## Deliverables
- [ ] Update `groupedEggs` useMemo in AppsHome.tsx to sort each section array by status (BUILT before STUB)
- [ ] Render status divider between BUILT and STUB items within a section
- [ ] Add `.apps-home__status-divider` CSS class using var(--sd-*) variables only
- [ ] Update existing tests in `AppsHome.test.tsx` to verify sort order
- [ ] Add 4-6 new tests:
  - [ ] BUILT items appear before STUB items within same section
  - [ ] Divider appears when section has both BUILT and STUB items
  - [ ] No divider when section has only BUILT or only STUB items
  - [ ] Search filtering preserves sort order (BUILT before STUB in results)
  - [ ] Multiple sections each sort independently
  - [ ] Empty section does not render

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass (currently 10 tests)
- [ ] All new tests pass (4-6 new tests expected)
- [ ] Edge cases covered:
  - All BUILT items in a section (no divider)
  - All STUB items in a section (no divider)
  - Mixed BUILT/STUB (divider appears once per section)
  - Empty section after filtering (no render)
  - Search preserves sort order

## Acceptance Criteria
- [ ] BUILT eggs appear above STUB eggs within each section
- [ ] Visual divider appears between BUILT and STUB groups when both exist in a section
- [ ] Divider uses var(--sd-*) variables only (no hardcoded colors)
- [ ] All tests pass (10 existing + 4-6 new = 14-16 total)
- [ ] No file exceeds 500 lines (AppsHome.tsx currently 98 lines, safe)
- [ ] No stubs shipped

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hex, rgb(), or named colors)
- No stubs (full implementation required)
- TDD approach (tests first, then implementation)

## Test Commands
```bash
# Run AppsHome tests only
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/apps-home/__tests__/AppsHome.test.tsx

# Run all browser tests
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260317-TASK-BL-208-RESPONSE.md`

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

## Model Assignment
haiku

## Priority
P0
