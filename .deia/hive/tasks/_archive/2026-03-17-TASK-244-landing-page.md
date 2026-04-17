# TASK-244: Landing Page

**Date:** 2026-03-17
**Priority:** P2
**Wave:** Wave 5 Ship
**Estimated Effort:** 2 hours
**Model:** Sonnet

---

## Objective

Create a landing page for ShiftCenter that serves as the "front door" for new users visiting the root URL without an EGG parameter. The landing page explains what ShiftCenter is, shows a screenshot placeholder, presents three feature cards, and provides CTAs for sign-up and demo.

---

## Context

This is **Wave 5 Ship** — the final mile before going public. People need to find the product, understand what it does, sign up via ra96it, and try the demo.

Currently, when a user visits the root URL (`/`) without an `?egg=` parameter, the EGG resolver fails to find an EGG and shows an error state. The landing page should replace this error state with a proper marketing page.

The landing page is NOT an EGG — it is a standalone React component that renders before the EGG system. It will be conditionally shown in `App.tsx` when no EGG parameter is provided and the URL is the root path.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — Root component, where landing page logic will be added
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` — EGG resolution logic (understand how `resolveCurrentEgg()` works)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — Design reference for layout and styling
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.css` — CSS reference
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — Theme CSS variables (Rule 3: no hardcoded colors)

---

## Deliverables

### 1. New React Component: `LandingPage.tsx`

**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\pages\LandingPage.tsx`

**Content Structure:**
- **Hero section:**
  - Title: "ShiftCenter"
  - Tagline: "Describe your process. Watch it build. Simulate it. See where it breaks."
  - Subtitle: "A governed application runtime for building, simulating, and deploying business processes with AI agents under constitutional constraints."

- **Screenshot placeholder:**
  - Styled div (border, padding, aspect ratio)
  - Text: "Screenshot coming soon"
  - Use CSS variables for styling

- **Three feature cards:**
  - Card 1: "Governed Agents" — "AI agents operate under constitutional constraints. Every action is logged, auditable, and reversible."
  - Card 2: "Constitutional Framework" — "Define permissions, policies, and workflows with human-readable configs. No surprises."
  - Card 3: "Simulation Before Execution" — "Test your process in a sandbox before running it in production. See failure modes early."

- **CTA Button (primary):**
  - Text: "Get Started"
  - Links to: ra96it sign-up flow (use `VITE_RA96IT_API` env var + `/signup` path)
  - Styled with `var(--sd-purple)` and hover effects

- **Secondary Link:**
  - Text: "Try the demo"
  - Links to: `?egg=canvas` (loads the canvas EGG)
  - Styled as secondary button

- **Footer:**
  - Text: "Built by DEIA Solutions"
  - Link: `https://deiasolutions.org`

**Props:** None (standalone page)

**Styling constraints:**
- All colors via `var(--sd-*)` variables (Rule 3)
- Responsive design (mobile-first, flexbox/grid)
- File under 500 lines (Rule 4)
- Consistent spacing (use CSS variables where possible)

---

### 2. CSS File: `LandingPage.css`

**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\pages\LandingPage.css`

**Requirements:**
- All colors via `var(--sd-*)` variables
- Responsive breakpoints (mobile, tablet, desktop)
- Animations for hover states (subtle glow, scale)
- No hardcoded colors (Rule 3)
- File under 500 lines (Rule 4)

**Classes to define:**
- `.landing-page-container` — full-height flex container
- `.landing-hero` — hero section layout
- `.landing-screenshot` — screenshot placeholder styling
- `.landing-features` — three-column grid (responsive)
- `.landing-feature-card` — individual feature card
- `.landing-cta-primary` — primary CTA button
- `.landing-cta-secondary` — secondary link button
- `.landing-footer` — footer section

---

### 3. Routing Logic Update: `App.tsx`

**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx`

**Changes:**

**Add import:**
```tsx
import LandingPage from './pages/LandingPage'
```

**Update `App()` function logic:**

Before the `useEggInit()` hook call, check if the current URL should show the landing page:

```tsx
const shouldShowLanding = (): boolean => {
  const params = new URLSearchParams(window.location.search)
  const hasEggParam = params.has('egg')
  const isRootPath = window.location.pathname === '/' || window.location.pathname === ''
  return isRootPath && !hasEggParam
}

export function App() {
  // If landing page should be shown, render it directly (bypass EGG system)
  if (shouldShowLanding()) {
    return <LandingPage />
  }

  // Otherwise, continue with EGG system
  const { loading, error, shellRoot, uiConfig } = useEggInit()
  // ... existing logic
}
```

**Preserve existing behavior:**
- `?egg=canvas` still loads canvas EGG
- `/efemera` pathname still loads efemera EGG
- All other EGG routing continues to work

---

### 4. Tests: Landing Page Component

**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\pages\__tests__\LandingPage.test.tsx`

**Test Requirements:**

Write tests using vitest + React Testing Library:

1. **Rendering tests:**
   - [ ] Landing page renders without crashing
   - [ ] Hero title "ShiftCenter" is present
   - [ ] Tagline is present
   - [ ] Screenshot placeholder is present
   - [ ] Three feature cards render
   - [ ] CTA button "Get Started" is present
   - [ ] Secondary link "Try the demo" is present
   - [ ] Footer with "Built by DEIA Solutions" is present

2. **Link tests:**
   - [ ] CTA button links to correct sign-up URL (check href)
   - [ ] Secondary link points to `?egg=canvas`
   - [ ] Footer link points to `https://deiasolutions.org`

3. **CSS tests:**
   - [ ] All elements use `var(--sd-*)` CSS variables (no hardcoded colors)
   - [ ] Responsive layout works (smoke test: check that feature cards stack on small screens)

4. **Integration test (App.tsx):**
   - [ ] When URL is `/` without `?egg=`, landing page renders
   - [ ] When URL is `/?egg=canvas`, Shell renders (not landing page)
   - [ ] When URL is `/efemera`, Shell renders (not landing page)

**Minimum test count:** 12 tests

---

## Test Requirements

- [ ] Tests written FIRST (TDD — Rule 5)
- [ ] All tests pass
- [ ] Edge cases covered:
  - URL with `?egg=canvas` does NOT show landing page
  - URL pathname `/chat` does NOT show landing page
  - URL `/` with no params DOES show landing page

**Test command:**
```bash
cd browser && npx vitest run src/pages/__tests__/LandingPage.test.tsx
```

---

## Constraints

- **No file over 500 lines** (Rule 4)
- **CSS: var(--sd-*) only** (Rule 3)
- **No stubs** (Rule 6) — every function fully implemented
- **TDD** (Rule 5) — tests first, then implementation
- **Responsive design** — must work on mobile, tablet, desktop
- **Production-ready code** — this is Wave 5 Ship, not a prototype

---

## Acceptance Criteria

- [ ] `LandingPage.tsx` component created with all sections (hero, screenshot, features, CTAs, footer)
- [ ] `LandingPage.css` created with all styles using CSS variables
- [ ] `App.tsx` updated to conditionally render landing page when URL is `/` without `?egg=`
- [ ] All tests pass (minimum 12 tests)
- [ ] No hardcoded colors (verified in tests)
- [ ] No files exceed 500 lines
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] CTA links point to correct URLs (ra96it sign-up + `?egg=canvas`)
- [ ] Footer link works

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-244-RESPONSE.md`

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

## Notes for the Bee

- **ra96it sign-up URL:** Use `import.meta.env.VITE_RA96IT_API` as the base URL and append `/signup`. If `VITE_RA96IT_API` is empty (local dev), default to relative path `/signup`.
- **Demo link:** Simply use `?egg=canvas` as the href — this will reload the current page with the EGG parameter, triggering the canvas EGG to load.
- **Design inspiration:** Look at `LoginPage.tsx` for layout patterns, but simplify. This is a marketing page, not an auth flow.
- **Screenshot placeholder:** Use a styled div with `border`, `background`, `padding`, and text. NO ACTUAL SCREENSHOT YET. Just a placeholder box that says "Screenshot coming soon".
- **Feature cards:** Keep descriptions short (1-2 sentences each). Focus on benefits, not technical details.
- **Footer:** Simple one-liner. No need for complex footer sections.
- **Responsive breakpoints:** Use `@media (max-width: 768px)` for tablet, `@media (max-width: 480px)` for mobile.
- **CSS animations:** Subtle. Hover glow on buttons, slight scale on cards. Nothing distracting.

---

## File Size Estimates

- `LandingPage.tsx`: ~250 lines (component + JSX)
- `LandingPage.css`: ~200 lines (responsive styles)
- `LandingPage.test.tsx`: ~150 lines (12+ tests)
- `App.tsx` changes: ~10 lines (conditional render logic)

**Total new/modified lines:** ~610 lines across 4 files

---

## Related Tasks

- TASK-245: ra96it sign-up flow (E2E test for sign-up URL)
- TASK-241: Production URL smoke test (verify landing page loads on production)

---

## References

- **Source spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-5-SHIP.md` — Task 5.5
- **Briefing:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\2026-03-17-BRIEFING-TASK-244-landing-page.md`
