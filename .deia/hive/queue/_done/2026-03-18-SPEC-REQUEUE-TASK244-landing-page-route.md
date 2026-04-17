# TASK-244 (RE-QUEUE): Landing page — wire route into App.tsx

## Background — Why Re-Queued
Original bee created LandingPage.tsx (component), LandingPage.css (styles), and LandingPage.test.tsx (tests). But the App.tsx route was never added. The landing page exists but is unreachable.

## Objective
Wire the existing LandingPage component into App.tsx so that visiting `/` without an `?egg=` param shows the landing page instead of an empty shell.

## What Already Exists (DO NOT recreate)
- `browser/src/pages/LandingPage.tsx` — full component with hero, feature cards, CTA
- `browser/src/pages/LandingPage.css` — styles
- `browser/src/pages/__tests__/LandingPage.test.tsx` — tests

## What Is Missing
`browser/src/App.tsx` does not import or reference LandingPage. It needs:
1. Import LandingPage
2. Check if URL has `?egg=` param
3. If no egg param → render LandingPage
4. If egg param → render Shell (existing behavior)

## Files to Read First
- `browser/src/App.tsx` (current routing logic)
- `browser/src/pages/LandingPage.tsx` (already exists)
- `browser/src/shell/useEggInit.ts` (how egg param is parsed)

## Files to Modify
- `browser/src/App.tsx` — add LandingPage import + conditional routing

## Deliverables
- [ ] App.tsx imports LandingPage
- [ ] Root `/` without `?egg` shows LandingPage
- [ ] Root `/` with `?egg=canvas` still shows Shell (no regression)
- [ ] LandingPage.test.tsx passes
- [ ] No regressions in App or shell tests

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/pages/__tests__/LandingPage.test.tsx`
- [ ] `cd browser && npx vitest run --reporter=verbose src/App.test.tsx` (if exists)
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify App.tsx
- Do NOT recreate LandingPage.tsx or its CSS — they already exist

## Model Assignment
sonnet

## Priority
P2

## Re-Queue Metadata
- Original spec: `_done/2026-03-16-SPEC-TASK-244-landing-page.md`
- Previous response: `20260317-TASK-244-RESPONSE.md`
- Failure reason: App.tsx routing never committed, LandingPage component unreachable
