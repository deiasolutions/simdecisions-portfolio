# TASK-BL-208: App Directory Sort (Re-Queue)

**Assigned to:** BEE
**Model:** Haiku
**Priority:** P0
**Date:** 2026-03-18

---

## Objective

Sort EGGs within each section (core/tools/fun) so **BUILT apps appear before STUB apps**. Add visual distinction for stub apps.

---

## Context

### Why Re-Queued

Previous bee (TASK-BL-208) claimed COMPLETE but verification found **zero sort-by-status logic**.

**Current state:**
- `AppsHome.tsx` groups EGGs into sections (core, tools, fun) via `SECTION_ORDER` constant
- Within each section, eggs appear in the order they're added to the group (lines 45-48)
- No sorting by `status` field exists
- `status` field is set by `eggRegistryService.ts` line 44: `status: e._stub ? 'STUB' : 'BUILT'`

**The issue:** Working EGGs and stub EGGs are mixed randomly within each section.

### Current Implementation

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

### EggMeta Type Shape

```typescript
interface EggMeta {
  egg: string;
  displayName: string;
  description: string;
  version: string;
  status: 'BUILT' | 'STUB';  // ← This is the field to sort by
  icon: string;
  color: string;
  section: 'core' | 'tools' | 'fun';
}
```

---

## Files to Read First

Read these files in this order:

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.tsx` (99 lines) — component to modify
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppCard.tsx` (41 lines) — card component, may need visual tweak
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\AppsHome.css` (93 lines) — CSS, stub styling goes here
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\apps-home\__tests__\AppsHome.test.tsx` (121 lines) — existing tests
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\egg-registry\types.ts` (20 lines) — type definitions

---

## Deliverables

### 1. Add sort-by-status logic

In `AppsHome.tsx`, after building the groups object (line 38-52), sort each section's array:

**Implementation:**
- After populating the groups, sort each array by status
- BUILT status → sort order 0 (appears first)
- STUB status → sort order 1 (appears second)

**Example approach:**
```tsx
const groupedEggs = useMemo(() => {
  const groups: Record<string, EggMeta[]> = {
    core: [],
    tools: [],
    fun: [],
  };

  filteredEggs.forEach((egg) => {
    if (groups[egg.section]) {
      groups[egg.section].push(egg);
    }
  });

  // Sort each section: BUILT before STUB
  Object.keys(groups).forEach((section) => {
    groups[section].sort((a, b) => {
      if (a.status === b.status) return 0;
      return a.status === 'BUILT' ? -1 : 1;
    });
  });

  return groups;
}, [filteredEggs]);
```

### 2. Add visual distinction for stub apps

Choose ONE approach (use your judgment):

**Option A: Reduce card opacity for stubs**
- Add class `.apps-home-card--stub` to stub cards
- CSS: `opacity: 0.6` on stub cards
- Keeps layout clean, subtle visual feedback

**Option B: Add "Coming Soon" label to stub badge**
- Modify AppCard.tsx to show "COMING SOON" instead of "STUB"
- Badge already has `.apps-home-badge--stub` styling

**Option C: Add subtle visual marker**
- Add an icon or label on stub cards (e.g., "⏳ Coming Soon" text)
- Keep existing badge styling

**RECOMMENDED: Option A** — it's the least invasive and provides clear visual feedback without cluttering the UI.

### 3. Write tests FIRST (TDD)

Add at least **3 new tests** to `AppsHome.test.tsx`:

**Test 1: BUILT apps render before STUB apps in each section**
```tsx
it('sorts BUILT apps before STUB apps within each section', () => {
  const mixedEggs: EggMeta[] = [
    { egg: 'stub1', displayName: 'Stub App', description: 'Coming soon', version: '1.0.0', status: 'STUB', icon: 'S', color: 'purple', section: 'core' },
    { egg: 'built1', displayName: 'Built App', description: 'Working app', version: '1.0.0', status: 'BUILT', icon: 'B', color: 'green', section: 'core' },
    { egg: 'stub2', displayName: 'Stub Tool', description: 'Coming soon', version: '1.0.0', status: 'STUB', icon: 'S', color: 'orange', section: 'tools' },
    { egg: 'built2', displayName: 'Built Tool', description: 'Working tool', version: '1.0.0', status: 'BUILT', icon: 'B', color: 'cyan', section: 'tools' },
  ];

  render(<AppsHome eggs={mixedEggs} />);

  const coreSection = screen.getByText('Core Products').closest('section');
  const coreCards = within(coreSection!).getAllByText(/BUILT|STUB/);
  const coreCardTexts = coreCards.map(badge => badge.textContent);

  // First card should be BUILT, second should be STUB
  expect(coreCardTexts[0]).toBe('BUILT');
  expect(coreCardTexts[1]).toBe('STUB');
});
```

**Test 2: Stub cards have visual distinction**
```tsx
it('applies visual styling to stub cards', () => {
  const stubEgg: EggMeta[] = [
    { egg: 'stub1', displayName: 'Stub App', description: 'Coming soon', version: '1.0.0', status: 'STUB', icon: 'S', color: 'purple', section: 'core' },
  ];

  render(<AppsHome eggs={stubEgg} />);

  const card = screen.getByText('Stub App').closest('.apps-home-card');
  // If using Option A: check for opacity class
  expect(card).toHaveClass('apps-home-card--stub');
});
```

**Test 3: Mixed BUILT/STUB in multiple sections all sort correctly**
```tsx
it('sorts BUILT before STUB in all sections simultaneously', () => {
  const mixedEggs: EggMeta[] = [
    { egg: 'stub1', displayName: 'Stub Core', description: 'Coming soon', version: '1.0.0', status: 'STUB', icon: 'S', color: 'purple', section: 'core' },
    { egg: 'built1', displayName: 'Built Core', description: 'Working', version: '1.0.0', status: 'BUILT', icon: 'B', color: 'green', section: 'core' },
    { egg: 'stub2', displayName: 'Stub Tool', description: 'Coming soon', version: '1.0.0', status: 'STUB', icon: 'S', color: 'orange', section: 'tools' },
    { egg: 'built2', displayName: 'Built Tool', description: 'Working', version: '1.0.0', status: 'BUILT', icon: 'B', color: 'cyan', section: 'tools' },
    { egg: 'stub3', displayName: 'Stub Fun', description: 'Coming soon', version: '1.0.0', status: 'STUB', icon: 'S', color: 'red', section: 'fun' },
    { egg: 'built3', displayName: 'Built Fun', description: 'Working', version: '1.0.0', status: 'BUILT', icon: 'B', color: 'purple', section: 'fun' },
  ];

  render(<AppsHome eggs={mixedEggs} />);

  // Check core section
  const coreSection = screen.getByText('Core Products').closest('section');
  const coreCards = within(coreSection!).getAllByRole('heading', { level: 3 }); // assuming card names are h3
  expect(coreCards[0]).toHaveTextContent('Built Core');
  expect(coreCards[1]).toHaveTextContent('Stub Core');

  // Check tools section
  const toolsSection = screen.getByText('Tools').closest('section');
  const toolsCards = within(toolsSection!).getAllByRole('heading', { level: 3 });
  expect(toolsCards[0]).toHaveTextContent('Built Tool');
  expect(toolsCards[1]).toHaveTextContent('Stub Tool');

  // Check fun section
  const funSection = screen.getByText('Fun').closest('section');
  const funCards = within(funSection!).getAllByRole('heading', { level: 3 });
  expect(funCards[0]).toHaveTextContent('Built Fun');
  expect(funCards[1]).toHaveTextContent('Stub Fun');
});
```

**Note:** Adjust test selectors based on actual DOM structure. If card names aren't h3, use `getAllByText` or another selector.

---

## Test Requirements

- [ ] **TDD:** Write all 3 new tests BEFORE implementing sort logic
- [ ] All new tests fail before implementation
- [ ] All new tests pass after implementation
- [ ] All existing 10 tests in `AppsHome.test.tsx` still pass
- [ ] No regressions in egg registry tests

---

## Constraints

- **No file over 500 lines** (AppsHome.tsx is 99 lines, AppsHome.css is 93 lines — plenty of room)
- **CSS: var(--sd-*) only** — no hardcoded colors, hex, rgb(), or named colors
- **No stubs** — sort logic must be fully implemented, not commented out or TODO
- **TDD required** — tests first, then implementation
- **No changes to files outside scope** — only modify AppsHome.tsx, AppsHome.css (or AppCard.css), and AppsHome.test.tsx

---

## Acceptance Criteria

- [ ] Within each section (core/tools/fun), BUILT apps render before STUB apps
- [ ] Stub apps have visible visual distinction (opacity, class, or label)
- [ ] At least 3 new tests verify sort order
- [ ] All existing tests pass (10 existing + 3 new = 13 total in AppsHome.test.tsx)
- [ ] No files exceed 500 lines
- [ ] CSS uses `var(--sd-*)` only
- [ ] No stubs, TODOs, or placeholder code shipped

---

## Smoke Test Commands

```bash
# Run AppsHome tests specifically
cd browser && npx vitest run --reporter=verbose src/primitives/apps-home/__tests__/AppsHome.test.tsx

# Run full browser test suite to check for regressions
cd browser && npx vitest run
```

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BL-208-RESPONSE.md`

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

---

## Notes for BEE

1. **Read all files listed in "Files to Read First" before starting**
2. **Write tests FIRST** — TDD is non-negotiable
3. **The sort must happen after grouping, not before** — grouping logic is correct, just missing sort
4. **Keep it simple** — one sort comparator, one CSS class for stub styling
5. **Verify no regressions** — run full test suite after your changes

---

## Previous Failure Analysis

**Previous response:** `20260317-TASK-BL-208-RESPONSE.md`

**Claimed:** "Sort logic added to AppsHome.tsx"

**Reality:** No sort logic exists. The bee added category grouping (which was already there) but not sort-by-status within groups.

**Root cause:** Bee misread the requirement. Thought "grouping by section" was the same as "sorting by status."

**This time:** The requirement is crystal clear: "After grouping, sort each group's array by status field. BUILT before STUB."

---

**End of Task File**
