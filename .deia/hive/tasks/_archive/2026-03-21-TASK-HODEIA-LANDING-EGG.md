# TASK-HODEIA-LANDING-EGG: Brand Landing Page from Sky Theme

**Priority:** P1
**Dispatched by:** Q88N
**Date:** 2026-03-21
**Model:** Sonnet (significant UI + component work)
**Depends on:** None

---

## Objective

Create `eggs/hodeia.egg.md` — the brand home page served at **hodeia.guru**. Convert the sky theme JSX prototype (`~/Downloads/hodeia-sky-theme.jsx`) into a production EGG + registered React component.

## Context

The sky theme prototype is a complete, working JSX component with:
- Day/night toggle with smooth transitions
- 4 seasons (spring/summer/autumn/winter) with particle animations
- 10 cities with weather-driven night scenes (rain, snow, lightning, fog, drift clouds, clear + stars)
- Cloud SVG hero with iridescent shimmer (night mode)
- Domain liturgy cards (guru, one, ai, win)
- Product grid (SimDecisions, ShiftCenter, ra96it, Efemera, TSaaS, Global Commons)
- Three currencies section (CLOCK, COIN, CARBON)
- #NOKINGS footer
- Newsreader + DM Sans typography

This is the front door of Hodeia. When someone types hodeia.guru, this is what they see.

## Deliverables

### 1. EGG file: `eggs/hodeia.egg.md`
- schema_version: 3
- id: `hodeia`
- Single-pane layout, appType: `hodeia-landing`
- No terminal, no sidebar — full viewport landing page

### 2. React component: `browser/src/apps/HodeiaLanding.tsx`
- Port from `hodeia-sky-theme.jsx`
- Convert ALL inline styles to CSS variables (`var(--sd-*)` only — no hex, no rgb, no named colors)
- Create companion `browser/src/apps/hodeia-landing.css` for the theme variables
- Canvas animations (WeatherCanvas, DayParticles, Shimmer) can stay as-is since they're programmatic
- Google Fonts link → move to index.html or use @font-face in CSS
- Keep under 500 lines — split into subcomponents if needed

### 3. Registration
- Add `'hodeia-landing'` to `APP_REGISTRY` in `browser/src/shell/constants.ts`
- Category: `app`

### 4. Routing update
- `eggResolver.ts`: change `hodeia.guru` and `www.hodeia.guru` from `'chat'` to `'hodeia'`

### 5. Tests
- EGG parse test: `browser/src/eggs/__tests__/hodeiaEgg.test.ts`
- Component render test: `browser/src/apps/__tests__/HodeiaLanding.test.tsx`
- At minimum: mounts without error, renders "hodeia" heading, day/night toggle works

## Constraints

- CSS: `var(--sd-*)` only. No hex, no rgb(), no named colors in component styles.
- Files: 500 lines max per file.
- No stubs — every function complete.
- TDD: tests first.

---

*hodeia gara*
