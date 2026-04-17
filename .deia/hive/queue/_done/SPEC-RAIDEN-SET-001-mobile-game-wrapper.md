# SPEC-RAIDEN-SET-001: Raiden Game Set — Mobile-First Wrapper

**Priority:** P2

## Objective

Create a `raiden.set.md` stage layout that wraps the self-contained Raiden shmup game (`/games/raiden-v1-20260413.html`) as a first-class set, accessible via `?set=raiden` on any ShiftCenter domain. Mobile-first: full-viewport, no shell chrome, no top-bar, no menu-bar.

## Context

The Raiden game is a complete, self-contained HTML file at `browser/public/games/raiden-v1-20260413.html`. It has its own viewport meta, touch handling (`touch-action: none`), canvas rendering, and CSS using `--sd-*` variables. It needs to be wrapped in the ShiftCenter set system so it's accessible at `?set=raiden` on any deployed domain.

**Problem:** There is no `iframe` or `embed` appType in the shell's app registry. The shell renders pane content via `AppFrame.tsx` → `appRegistry.ts`, which maps `appType` strings to React components. A new generic `iframe` appType is needed.

### Key Files

| File | Purpose |
|------|---------|
| `browser/public/games/raiden-v1-20260413.html` | The game (self-contained HTML) |
| `browser/src/shell/components/appRegistry.ts` | App type → component registry (`registerApp()`) |
| `browser/src/shell/components/AppFrame.tsx` | Routes appType to registered renderer |
| `browser/src/sets/eggResolver.ts` | Maps `?set=raiden` to `raiden.set.md` |
| `browser/sets/*.set.md` | Existing set files (see `home.set.md`, `canvas.set.md` for format) |
| `browser/src/sets/types.ts` | Set/egg type definitions |
| `browser/src/sets/eggInflater.ts` | Inflates set markdown into shell tree |

## Deliverables

### 1. `iframe` appType component (~40 lines)

**File:** `browser/src/apps/IframeApp.tsx`

A generic, reusable iframe wrapper component that:
- Reads `config.src` for the iframe URL
- Renders a full-size `<iframe>` (100% width/height, no border)
- Sets `sandbox="allow-scripts allow-same-origin"` for security
- Sets `allow="autoplay"` for game audio
- Implements `AppRendererProps` interface (`paneId`, `isActive`, `config`)

```typescript
// Config shape:
interface IframeAppConfig {
  src: string;         // URL to load (e.g. "/games/raiden-v1-20260413.html")
  sandbox?: string;    // Override sandbox attribute
  allow?: string;      // Permissions policy
}
```

### 2. Register `iframe` appType

**File:** `browser/src/apps/index.ts` (or wherever app registrations happen)

Add: `registerApp('iframe', IframeApp)`

Find where existing appTypes are registered (search for `registerApp(` calls) and add the iframe registration alongside them.

### 3. `raiden.set.md` — mobile-first game layout

**File:** `browser/sets/raiden.set.md`

```yaml
---
egg: raiden
version: 1.0.0
schema_version: 3
displayName: Raiden
description: Raiden shmup arcade game. Mobile-first, full-viewport.
defaultRoute: /raiden
_stub: false
auth: public
---
```

Layout: **single pane, no chrome, no top-bar, no menu-bar.** The game handles its own UI.

```layout
{
  "type": "pane",
  "nodeId": "raiden-game",
  "appType": "iframe",
  "label": "Raiden",
  "chrome": false,
  "seamless": true,
  "config": {
    "src": "/games/raiden-v1-20260413.html",
    "sandbox": "allow-scripts allow-same-origin",
    "allow": "autoplay"
  }
}
```

UI block: no chrome, no command palette (game captures all keyboard input).

```ui
{
  "chromeMode": "none",
  "commandPalette": false,
  "akk": false
}
```

Empty tabs, commands, settings blocks (game is self-contained).

### 4. Vercel routing (if needed)

Check if `vercel.json` already serves `/games/*` files. The current static file rule (`/(.*\.(js|css|png|jpg|svg|ico|woff2?|ttf|json))$`) does NOT match `.html` files. If Vite/Vercel doesn't serve the game HTML at `/games/raiden-v1-20260413.html`, add a route.

**Likely fix in `vercel.json`:**
```json
{ "src": "/games/(.*\\.html)$", "dest": "/games/$1" }
```

Add this BEFORE the catch-all landing page rules.

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] `IframeApp.test.tsx`: renders iframe with correct `src` from config, applies sandbox, applies allow
- [ ] `IframeApp.test.tsx`: renders nothing or fallback when `config.src` is missing
- [ ] `raiden.set.md` parses correctly (add to existing `parseEggMd.test.ts` or `eggInflater.test.ts`)
- [ ] `eggResolver` returns `"raiden"` for `?set=raiden` (already works by design — just verify)
- [ ] All existing tests still pass

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only (IframeApp needs no CSS — it's just an iframe wrapper)
- No stubs
- `auth: public` — no login required to play the game
- The game HTML must NOT be modified — it's self-contained and already works
- The `iframe` appType must be generic/reusable, not Raiden-specific

## Acceptance Criteria

- [ ] `?set=raiden` on localhost:5173 loads the game full-viewport
- [ ] No shell chrome visible (no top-bar, no menu-bar, no pane chrome)
- [ ] Game is playable on mobile (touch controls work through iframe)
- [ ] Game is playable on desktop (keyboard controls work through iframe)
- [ ] `iframe` appType is reusable for any future embedded HTML content
- [ ] Existing sets (`?set=chat`, `?set=canvas`, etc.) unaffected
- [ ] All tests pass

## Notes

- The game already has `touch-action: none` and mobile viewport meta — no additional mobile handling needed in the wrapper
- The `iframe` appType is deliberately simple — just an iframe. No postMessage bridge, no bus integration. Games are isolated.
- Future games or external apps can reuse the same `iframe` appType pattern
