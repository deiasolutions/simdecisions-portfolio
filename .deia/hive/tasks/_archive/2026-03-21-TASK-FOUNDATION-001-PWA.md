# TASK-FOUNDATION-001-PWA: Mobile PWA Shell for hodeia.app

**Priority:** P1
**Dispatched by:** Q88N
**Date:** 2026-03-21
**Model:** Sonnet (PWA + mobile UX requires precision)
**Depends on:** None (chat.egg.md already exists)

---

## Objective

Wire hodeia.app as a mobile-first PWA entry point. This is Phase 3 of HODEIA-FOUNDATION-001.ir.yaml — "The glass takes shape." Goal: installable on iPhone/Android, full-screen chat, no browser chrome.

## Context

FOUNDATION-001 defines 5 phases:
1. Hivenode skeleton (exists)
2. WebSocket channel (future)
3. **Mobile glass** ← THIS TASK
4. LLM routing (exists via terminal service)
5. Learning loop (exists via ledger)

hodeia.app is already mapped to `'chat'` EGG in eggResolver.ts. The chat EGG works on desktop. This task makes it work beautifully on mobile and makes it installable as a PWA.

## Deliverables

### 1. PWA manifest: `browser/public/manifest.json`
```json
{
  "name": "Hodeia",
  "short_name": "Hodeia",
  "description": "The governed AI platform",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait",
  "theme_color": "#f5f0e8",
  "background_color": "#f5f0e8",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### 2. Service worker: `browser/public/sw.js`
- Cache shell assets (JS, CSS, fonts) on install
- Network-first for API calls, cache-first for static assets
- Offline fallback page

### 3. HTML meta tags in `browser/index.html`
- `<link rel="manifest" href="/manifest.json">`
- Apple meta tags: `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, viewport
- Theme color meta tag

### 4. Placeholder icons
- `browser/public/icons/icon-192.png` — simple "H" on brand background
- `browser/public/icons/icon-512.png` — same, larger
- (Will be replaced with real brand assets later)

### 5. Mobile viewport fixes for chat.egg.md
- Safe area insets (iPhone notch + home indicator): `env(safe-area-inset-*)`
- Input bar stays above keyboard (visualViewport API)
- No horizontal scroll on mobile
- Touch-friendly tap targets (min 44px)

### 6. Tests
- Manifest validity test
- Service worker registration test
- Mobile viewport meta tag presence test

## Constraints

- CSS: `var(--sd-*)` only.
- Files: 500 lines max.
- No stubs.
- TDD.
- Do NOT change the desktop chat experience — mobile fixes must be additive/responsive.

---

*hodeia gara*
