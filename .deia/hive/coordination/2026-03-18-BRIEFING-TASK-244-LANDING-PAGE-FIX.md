# BRIEFING: TASK-244 Landing Page Fix

**To:** Q33N
**From:** Q33NR
**Date:** 2026-03-18
**Priority:** P2 (re-queue from failed implementation)

## Background

TASK-244 was dispatched on 2026-03-17. The bee (Sonnet) reported "COMPLETE" but the implementation does NOT match the spec.

**Original spec required:**
- Three feature cards: "Governed Agents", "Constitutional Framework", "Simulation Before Execution"
- Each card with icon, title, description

**What was actually built:**
- Uses `AppsHomeAdapter` (the EGG chooser grid from apps-home)
- Tests expect "Core Products" and "Tools" headers (don't exist)
- Tests are FAILING: 2 failures, 11 passing

**Test failures:**
```
✓ renders the landing page component
✓ renders the hero title 'ShiftCenter'
✓ renders the tagline
✓ renders the subtitle
✓ renders AppsHomeAdapter
✗ renders three feature cards
✗ renders all three section headers ('Core Products', 'Tools')
✓ renders the primary CTA button
✓ renders the demo link
✓ renders the footer
✓ CTA button links to ra96it sign-up
✓ demo link has correct href
✓ footer link has correct href
```

## Root Cause

The bee misread the spec. Instead of creating static feature cards (as specified), it reused the AppsHomeAdapter component (which shows the EGG chooser grid). The tests were written for a different implementation than the code.

## What Q33N Must Do

1. **Read the original spec:** `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-244-landing-page.md`
2. **Read the failed implementation:**
   - `browser/src/pages/LandingPage.tsx` (current — uses AppsHomeAdapter)
   - `browser/src/pages/__tests__/LandingPage.test.tsx` (failing tests)
3. **Write ONE task file** for a bee to fix this:
   - Remove AppsHomeAdapter usage from LandingPage.tsx
   - Replace with three static feature cards (as per original spec)
   - Fix or rewrite tests to match the corrected implementation
   - Ensure all tests pass
   - Keep App.tsx routing logic (it's already correct)

## Constraints

- **Do NOT recreate App.tsx routing** — it's already correct (lines 58-69)
- **Do NOT create a new landing page** — modify the existing one
- **File must stay under 500 lines** (currently 57 lines, safe)
- **CSS variables only** (`var(--sd-*)`)
- **TDD:** Tests must pass before marking complete

## Files Q33N Should Reference in Task

- `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-244-landing-page.md` (original spec)
- `.deia/hive\responses\20260317-TASK-244-RESPONSE.md` (failed bee response)
- `browser/src/pages/LandingPage.tsx` (current broken implementation)
- `browser/src/pages/__tests__/LandingPage.test.tsx` (failing tests)
- `browser/src/shell/shell-themes.css` (CSS variables reference)

## Expected Deliverable from Q33N

One task file: `TASK-244-FIX-LANDING-PAGE-FEATURE-CARDS.md`

The task should specify:
1. Remove `AppsHomeAdapter` import and usage
2. Add three feature card divs with icons, titles, descriptions
3. Update tests to match the actual feature cards (not "Core Products"/"Tools")
4. Run tests and verify all pass
5. Model assignment: **haiku** (straightforward fix, well-defined scope)

## Success Criteria

- [ ] LandingPage.tsx shows three static feature cards (not AppsHomeAdapter)
- [ ] All tests pass (0 failures)
- [ ] Component matches original spec from `_done/2026-03-16-SPEC-TASK-244-landing-page.md`
- [ ] No regressions on App.tsx routing

## Model Assignment for This Briefing

Use **sonnet** for Q33N to review the context and write the task file.

---

**Q33NR NOTE:** This is a classic "bee reported complete but didn't verify tests" failure. The bee wrote tests for one implementation and code for another. Q33N's task file must explicitly require the bee to run tests and verify pass before claiming complete.
