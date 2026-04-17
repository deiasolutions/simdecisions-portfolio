# BRIEFING: TASK-244 — Landing Page (Wave 5 Ship)

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-17
**Priority:** P2

---

## Objective

Create a landing page for ShiftCenter as the "front door" for new users. One page, clear value proposition, sign-up CTA, and demo link.

## Context from Q88N (Dave)

This is **Wave 5 Ship** — the final mile before going public. People need to:
1. Find the product
2. Understand what it does
3. Sign up via ra96it
4. Try the demo

The landing page is the answer to "What is ShiftCenter?" Keep it simple. Hero, screenshot placeholder, three feature cards, two CTAs, footer. Done.

## Source Spec

`docs/specs/WAVE-5-SHIP.md` — Task 5.5

Quote:
> "Landing page: what is ShiftCenter, one screenshot, sign up link"

Estimated effort: 2 hours

## Files to Read Before Writing Task Files

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\LoginPage.tsx` — Existing login page (design reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — Theme variables (Rule 3: no hardcoded colors)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\` — Available product EGGs (chat, canvas, efemera, etc.)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — Current routing logic (to understand where to inject landing page)

## What the Bee Must Deliver

1. **New file:** `browser/src/pages/LandingPage.tsx`
   - Hero section: "ShiftCenter" title + tagline "Describe your process. Watch it build. Simulate it. See where it breaks."
   - Screenshot placeholder: styled div with border, "Screenshot coming soon" text
   - Three feature cards: "Governed Agents", "Constitutional Framework", "Simulation Before Execution"
   - CTA button: "Get Started" → links to ra96it sign-up URL
   - Secondary link: "Try the demo" → links to `?egg=canvas`
   - Footer: "Built by DEIA Solutions" with link to deiasolutions.org

2. **CSS styling:**
   - All colors via `var(--sd-*)` variables (Rule 3)
   - Responsive design (works on mobile)
   - File under 500 lines (Rule 4)

3. **Routing:**
   - Modify routing so root `/` without `?egg` param shows LandingPage instead of empty shell
   - Preserve existing behavior: `?egg=canvas` still loads canvas EGG

4. **Tests:**
   - Landing page renders
   - CTA links are correct
   - Feature cards render
   - Responsive behavior (at least smoke test)

5. **Test command:** `cd browser && npx vitest run src/pages/`

## Constraints (10 Hard Rules)

- Rule 3: NO hardcoded colors. Only `var(--sd-*)`.
- Rule 4: No file over 500 lines.
- Rule 5: TDD — tests first, then implementation.
- Rule 6: NO stubs. Every function fully implemented.

## Model Assignment

**Sonnet** — front-end UI work with routing logic and responsive design.

## Expected Task Files from Q33N

One task file:
- `TASK-244-landing-page.md`

## Notes

- ra96it sign-up URL: Bee should check existing code for the correct URL pattern (likely `https://ra96it.com/signup` or similar)
- "Try the demo" link: `?egg=canvas` is the simplest demo EGG
- This is **Wave 5 Ship** — production-ready code, not a prototype

---

## Q33N: Your Next Steps

1. Read the files listed above
2. Write one task file for this work
3. Return to Q33NR for review
4. DO NOT dispatch the bee yet — wait for Q33NR approval
