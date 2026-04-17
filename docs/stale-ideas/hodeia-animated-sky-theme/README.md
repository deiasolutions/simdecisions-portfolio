# Hodeia Animated Sky Theme Landing Page (DEPRECATED)

**Status:** Deprecated
**Date archived:** 2026-03-25
**Replaced by:** hodeia-guru-landing.html (Mr. AI original design)

## What This Was

An animated, interactive landing page for hodeia.guru featuring:

- **Day/night toggle** with smooth sky gradient transitions
- **4 seasonal themes** (spring petals, summer sun rays, autumn leaves, winter snow)
- **10 city weather picker** (Austin, Dublin, Reykjavik, Mumbai, SF, London, Tokyo, Rome, Edinburgh, Menlo Park)
- **6 night weather animations** (clear/stars, rain, snow, storm/lightning, fog, cloudy/driftclouds)
- **Canvas-based particle systems** for all weather effects
- **Iridescent shimmer overlay** on night cloud SVG
- **Moon with crescent shadow**, sun glow effects
- **Domain liturgy** (hodeia.guru, .one, .ai, .win with Basque mantras)
- **Product grid** (SimDecisions, ShiftCenter, ra96it, Efemera, TSaaS, Global Commons)
- **Three currencies** (CLOCK, COIN, CARBON)
- **#NOKINGS footer**

## Why Deprecated

This page was built during early development but was not the original design created by Mr. AI. The Mr. AI design (hodeia-guru-landing.html) is the intended page for hodeia.guru — a clean dark-theme page with auth integration, app family grid, and philosophy strip.

## Original Files

- `HodeiaLanding.tsx` — Main React component (218 lines)
- `DayParticles.tsx` — Canvas day animations (87 lines)
- `WeatherCanvas.tsx` — Canvas night weather (95 lines)
- `Shimmer.tsx` — Iridescent shimmer overlay (53 lines)
- `hodeia-theme-data.ts` — Theme/season/city/domain config (206 lines)
- `hodeiaLandingAdapter.tsx` — Shell app registry adapter (10 lines)
- `HodeiaLanding.test.tsx` — 14 test cases (101 lines)
- `hodeia-sky-theme.jsx` — Original single-file JSX prototype from Downloads (539 lines)

## Technical Notes

- Used React + Canvas 2D API (requestAnimationFrame loops)
- Inline styles with theme-resolved colors (not --sd-* variables — standalone brand page)
- Google Fonts: Newsreader, DM Sans
- Registered as standalone EGG bypassing Shell in App.tsx
