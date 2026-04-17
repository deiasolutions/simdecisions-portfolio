# BRIEFING: BL-208 — App Directory Sort Order

**From:** Q88NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Spec:** `.deia/hive/queue/2026-03-17-SPEC-TASK-BL208-app-directory-sort-order.md`

---

## Objective

Update the App Directory (AppsHome) to sort EGGs so working/built items appear at the top and unbuilt/stub items appear below in a separate section.

---

## Context from Spec

The App Directory currently shows all EGGs in a flat list, grouped only by section (core/tools/fun). Users want to see working apps first, with unbuilt/stub items clearly separated below in a "Coming Soon" or "In Development" section.

---

## Current Architecture (What Q33N Needs to Know)

### File Structure
- **AppsHome component:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.tsx`
  - Current grouping: by section (core/tools/fun) only
  - Uses `groupedEggs` useMemo to organize by section
  - Sections render in order: core → tools → fun
  - No status-based sorting currently

- **AppCard component:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppCard.tsx`
  - Displays status badge (BUILT/STUB)
  - Uses `statusClass` for badge styling
  - No changes needed here unless status badge styling needs improvement

- **EggRegistry Service:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\egg-registry\eggRegistryService.ts`
  - Fetches `egg-manifest.json` (built by `copy-eggs.cjs`)
  - Enriches with status: `BUILT` or `STUB` (from `_stub` field in manifest)
  - Already provides status data — no changes needed

- **Manifest Generator:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\scripts\copy-eggs.cjs`
  - Parses EGG frontmatter
  - Reads `_stub: true` field to determine status
  - No changes needed — data is already available

### Types
- `EggMeta` interface in `browser/src/services/egg-registry/types.ts`
  - Has `status: 'BUILT' | 'STUB'` field
  - Has `section: 'core' | 'tools' | 'fun'` field
  - Structure is already complete for sorting

### Existing Tests
- `browser/src/primitives/apps-home/__tests__/AppsHome.test.tsx` (121 lines)
  - Tests section grouping
  - Tests search filtering
  - Tests card rendering
  - **Will need updates:** tests currently expect all eggs in section order, not status order

---

## What Needs to Change

### 1. Sorting Logic in AppsHome.tsx
**Current:** Groups by section only (core/tools/fun)
**Needed:** Within each section, sort BUILT items first, then STUB items

**Implementation approach:**
- Modify `groupedEggs` useMemo to sort each section's array
- Sort order: `status === 'BUILT' ? 0 : 1` (BUILT before STUB)
- Preserve existing section grouping (core → tools → fun)

### 2. Visual Separation
**Needed:** Section divider between BUILT and STUB items within each section

**Implementation approach:**
- Option A: Insert a divider element when transitioning from BUILT to STUB status within a section
- Option B: Use two subsections per section ("Available" and "Coming Soon")
- Recommend Option A for simplicity — less DOM overhead

**CSS requirements:**
- Divider styling must use `var(--sd-*)` variables only
- Keep minimal — a thin line or spacing, not heavy visual weight

### 3. Test Updates
**Files to update:**
- `browser/src/primitives/apps-home/__tests__/AppsHome.test.tsx`

**New test scenarios needed:**
- BUILT items appear before STUB items within same section
- Divider appears when section has both BUILT and STUB items
- No divider when section has only BUILT or only STUB items
- Search preserves sort order (BUILT before STUB in results)

**Test count estimate:** 4-6 new tests

---

## Deliverables (from spec)

- [ ] Sort EGGs: working items first, then unbuilt/stub items
- [ ] Add visual section divider between "Available" and "Coming Soon"
- [ ] Status badges reflect actual build status (working/stub/broken) — **already done, verify only**
- [ ] Tests for sort order and section grouping

---

## Acceptance Criteria (from spec)

- [ ] Working EGGs appear above unbuilt EGGs
- [ ] Section headers or dividers separate the groups
- [ ] Status badges accurate — **already implemented**
- [ ] Tests pass

---

## Constraints (from spec)

- No file over 500 lines (current AppsHome.tsx is 98 lines — safe)
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs (full implementation required)

---

## File Paths to Include in Task Files (absolute)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\__tests__\AppsHome.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\egg-registry\types.ts` (read-only reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\egg-registry\eggRegistryService.ts` (read-only reference)

---

## Model Assignment

**haiku** (per spec)

---

## Test Commands

```bash
# Run AppsHome tests only
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/apps-home/

# Run all browser tests
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run
```

---

## Q33N Task Requirements

**Write a single task file:**
- File: `.deia/hive/tasks/2026-03-17-TASK-BL-208-app-directory-sort-order.md`
- Model: haiku
- Role: bee
- Include all 8 sections of response file template

**Task should specify:**
- TDD approach (tests first)
- Exact sorting logic (BUILT before STUB within each section)
- CSS variable usage for divider
- Test count expectation: 4-6 new tests
- All file paths absolute

---

## Notes for Q33N

- Status data is already available — no backend changes needed
- This is purely a frontend sorting + visual change
- Existing tests will need updates (they don't expect status-based sorting)
- Keep the divider subtle — it's a visual hint, not a major separator

---

## Next Steps

1. Q33N: Read this briefing
2. Q33N: Read the files listed in "File Paths to Include"
3. Q33N: Write task file with TDD approach
4. Q33N: Return to Q88NR for review
5. Q88NR: Review task file against checklist
6. Q88NR: Approve or request corrections (max 2 cycles)
7. Q33N: Dispatch bee (haiku)
8. Q88NR: Wait for bee completion
9. Q88NR: Review results
10. Q88NR: Report to Q88N

---

**End of briefing.**
