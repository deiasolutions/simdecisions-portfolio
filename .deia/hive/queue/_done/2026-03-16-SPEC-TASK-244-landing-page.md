# TASK-244: Landing Page — What is ShiftCenter (W5 — 5.5)

## Objective
Create a landing page for ShiftCenter: what it is, one hero screenshot placeholder, sign-up link to ra96it, and a "try it" CTA.

## Context
Wave 5 Ship. People need to find and understand the product before they can use it. This is the front door. Keep it simple — one page, clear value prop, one CTA.

## Source Spec
`docs/specs/WAVE-5-SHIP.md` — Task 5.5

## Files to Read First
- `browser/src/shell/components/LoginPage.tsx` — Existing login page (for design reference)
- `browser/src/shell/shell-themes.css` — Theme variables for consistent styling
- `eggs/` — Available product EGGs (chat, canvas, efemera, etc.)

## Deliverables
- [ ] Create `browser/src/pages/LandingPage.tsx`:
  - Hero section: "ShiftCenter" title, one-line tagline: "Describe your process. Watch it build. Simulate it. See where it breaks."
  - Screenshot placeholder: styled div with border, "Screenshot coming soon" text
  - Three feature cards: Governed Agents, Constitutional Framework, Simulation Before Execution
  - CTA button: "Get Started" → links to ra96it sign-up
  - Secondary link: "Try the demo" → links to `?egg=canvas`
  - Footer: "Built by DEIA Solutions" with link to deiasolutions.org
- [ ] Style using `var(--sd-*)` variables only — no hardcoded colors
- [ ] Make it responsive (works on mobile)
- [ ] Add route: root `/` without `?egg` param shows landing page instead of empty shell
- [ ] Add tests: landing page renders, CTA links are correct
- [ ] Run: `cd browser && npx vitest run src/pages/`

## Priority
P2

## Model
sonnet
