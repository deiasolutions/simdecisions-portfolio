# BRIEFING: BL-208 App Directory Sort (Re-Queue)

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Priority:** P0
**Model Assignment:** sonnet

---

## Background — Why Re-Queued

Previous bee (TASK-BL-208) claimed COMPLETE but verification found **zero sort-by-status logic**.

**Current state:**
- `AppsHome.tsx` groups EGGs into sections (core, tools, fun) via `SECTION_ORDER` constant
- Within each section, eggs appear in the order they're added to the group (lines 45-48)
- No sorting by `status` field exists
- `status` field is set by `eggRegistryService.ts` line 44: `status: e._stub ? 'STUB' : 'BUILT'`

**The issue:** Working EGGs and stub EGGs are mixed randomly within each section.

---

## Objective

Sort EGGs within each section so **BUILT apps appear before STUB apps**. Add visual distinction for stub apps.

---

## Context

### Files Already Read
- `browser/src/primitives/apps-home/AppsHome.tsx` (99 lines) — grouping logic but no sort
- `browser/src/primitives/apps-home/AppCard.tsx` (41 lines) — displays status badge
- `browser/src/services/egg-registry/eggRegistryService.ts` (81 lines) — enriches eggs with status field

### Key Code Locations

**AppsHome.tsx line 38-52 (groupedEggs useMemo):**
```tsx
const groupedEggs = useMemo(() => {
  const groups: Record<string, EggMeta[]> = {
    core: [],
    tools: [],
    fun: [],
  };

  filteredEggs.forEach((egg) => {
    if (groups[egg.section]) {
      groups[egg.section].push(egg);  // ← No sorting here
    }
  });

  return groups;
}, [filteredEggs]);
```

**Missing:** After grouping, each `groups[section]` array needs sorting: BUILT before STUB.

**AppCard.tsx line 16:**
```tsx
const statusClass = `apps-home-badge--${egg.status.toLowerCase()}`;
```

Status badge exists but no visual distinction between BUILT and STUB.

---

## What Needs to Happen

### 1. Add sort-by-status logic
In `AppsHome.tsx`, after building the groups object, sort each section's array:
- BUILT status → sort order 0
- STUB status → sort order 1

### 2. Add visual distinction for stub apps
Two options (Q33N choose best):
- **Option A:** Reduce opacity on stub cards (e.g. `opacity: 0.6`)
- **Option B:** Add "Coming Soon" label or different badge styling
- **Option C:** Separate "Coming Soon" subsection below each main section

### 3. Tests
- Unit test: verify sort order (BUILT before STUB within section)
- Test: verify visual styling applied to stub cards
- Integration test: full AppsHome render with mixed BUILT/STUB eggs

---

## Deliverables

### Code Changes
- [ ] `AppsHome.tsx` — add sort logic in `groupedEggs` useMemo
- [ ] `AppsHome.css` or `AppCard.css` — add visual styling for stub status
- [ ] Tests in `__tests__/AppsHome.test.tsx` — verify sort order

### Test Requirements
- [ ] At least 3 new tests for sort behavior
- [ ] All existing AppsHome tests still pass
- [ ] No regressions in egg registry tests

---

## Constraints

- **No file over 500 lines** (AppsHome.tsx is 99 lines, plenty of room)
- **CSS: var(--sd-*) only** — no hardcoded colors for stub styling
- **No stubs** — sort logic must be fully implemented
- **TDD** — write tests first

---

## Smoke Test Commands

```bash
# AppsHome tests
cd browser && npx vitest run --reporter=verbose src/primitives/apps-home/

# Full browser test suite
cd browser && npx vitest run
```

---

## Files to Modify (Absolute Paths)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.css` (or AppCard.css)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\__tests__\AppsHome.test.tsx`

---

## Success Criteria

- [ ] Within each section (core/tools/fun), BUILT apps render before STUB apps
- [ ] Stub apps have visible distinction (opacity, badge style, or label)
- [ ] At least 3 new tests verify sort order
- [ ] All existing tests pass
- [ ] No files exceed 500 lines
- [ ] CSS uses var(--sd-*) only

---

## Notes for Q33N

1. **Read the files first** before writing the task file
2. **Single bee task** — this is small enough for one bee (estimated 1-2 hours)
3. **Model: Haiku** — straightforward sort logic, no complex architecture
4. **TDD required** — bee writes sort tests first, then implements sort

---

## Previous Failure Analysis

**Previous response:** `20260317-TASK-BL-208-RESPONSE.md`

**Claimed:** "Sort logic added to AppsHome.tsx"

**Reality:** No sort logic exists. The bee added category grouping (which was already there) but not sort-by-status within groups.

**Root cause:** Bee misread the requirement. Thought "grouping by section" was the same as "sorting by status."

**This time:** Make the requirement crystal clear in the task file. Explicitly state: "After grouping, sort each group's array by status field."

---

**Q33N: Read this briefing, read the three files listed above, write one task file, return for Q33NR review before dispatching the bee.**
