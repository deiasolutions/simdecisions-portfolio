# EGG Schema Specification
**Date:** 2026-03-08  
**Version:** v1.0.0  
**Status:** Locked  
**Authors:** Q88N + Mr. AI (6laude)  
**Depends on:** ADR-FRANK-001, ADR-FRANK-006, ADR-APPLET-SHELL-001

---

## What Is an EGG

An EGG is a ShiftCenter application configuration. It declares a layout, a set of panes, UI chrome behavior, tab bar entries, favicon, away mode behavior, and metadata. EGGs do not live on a server — they inflate in memory at runtime. Assets referenced by an EGG live on the Global Commons CDN or are embedded as data URIs.

EGGs are loaded by SC via the EGG Registry (`src/eggs/index.ts`). SC resolves the active EGG from the current hostname via `eggResolver.ts`.

---

## Full Schema

```typescript
interface EggConfig {
  // ── Identity ───────────────────────────────────────────────────────────────
  egg: string             // unique ID — matches key in EGG_REGISTRY
  version: string         // semver
  displayName: string     // shown in tab bar and SC header
  description?: string    // human-readable, optional
  _stub?: boolean         // true = not fully implemented, SC warns in dev

  // ── Favicon ────────────────────────────────────────────────────────────────
  favicon?: string
  // Accepted formats:
  //   "global-commons://icons/my-app.png"  — platform EGGs, resolved to CDN
  //   "data:image/png;base64,iVBORw..."    — embedded, self-contained, works offline
  //   "https://example.com/favicon.png"    — external URL, use sparingly
  // SC sets document favicon on EGG inflate. Restores SC favicon on EGG unload.
  // If omitted: SC favicon is used.

  // ── UI Chrome ──────────────────────────────────────────────────────────────
  ui: {
    hideMenuBar?: boolean       // default false
    hideStatusBar?: boolean     // default false
    hideTabBar?: boolean        // default false — Zen mode sets true
    hideActivityBar?: boolean   // default false
    statusBarCurrencies?: ('clock' | 'coin' | 'carbon')[]  // default all three
  }

  // ── Tab Bar ────────────────────────────────────────────────────────────────
  tabs?: EggTab[]
  // Tabs declared here are the default tab bar for this EGG host.
  // User can add/remove tabs at runtime — persisted to session store.
  // Empty array = no tab bar (single-EGG host).

  // ── Away Mode ──────────────────────────────────────────────────────────────
  away?: {
    idleThresholdMs?: number    // ms before idle state. default: 300000 (5 min)
    blackoutDelayMs?: number    // ms after idle before black frame. default: 120000 (2 min)
    message?: string            // shown in black frame. e.g. "Please lock your screen or interact to restore."
    showFavicon?: boolean       // show EGG favicon in black frame. default: true
    faviconPosition?: 'center' | 'bottom-right'  // default: 'center'
    welcomeBack?: boolean       // show "Welcome back." in Zone 2 on return. default: true
  }

  // ── Layout ─────────────────────────────────────────────────────────────────
  layout: EggLayoutNode
}
```

---

## `EggTab`

```typescript
interface EggTab {
  id: string        // stable tab ID — never generated, always declared
  eggId: string     // which EGG config to load when this tab is active
  label: string     // display name — user-editable at runtime
  icon?: string     // emoji or global-commons:// icon reference
  active: boolean   // which tab is active on first load
}
```

---

## `EggLayoutNode`

Layout is a recursive tree. Each node is either a split container or an app pane.

```typescript
type EggLayoutNode = EggSplitNode | EggAppNode

interface EggSplitNode {
  type: 'split'
  direction: 'horizontal' | 'vertical'
  ratio: number           // 0–1, proportion given to children[0]
  children: [EggLayoutNode, EggLayoutNode]
}

interface EggAppNode {
  type: 'app'
  appType: string         // registered applet type — 'text' | 'terminal' | 'file-explorer' | etc.
  nodeId: string          // MUST be stable and explicit — never generated
  config: Record<string, unknown>   // applet-specific config, passed to useApplet
  chromeClose?: boolean   // show/hide close X button (default: true)
  chromePin?: boolean     // enable pin toggle (default: false) — when pinned, pane takes full width
  chromeCollapsible?: boolean  // enable collapse toggle (default: false) — pane can shrink to icon strip
}
```

---

## Favicon Resolution

SC resolves the `favicon` field at EGG inflate time using this priority:

```typescript
function resolveFavicon(favicon?: string): string | null {
  if (!favicon) return null

  // Global Commons — resolve to CDN base URL
  if (favicon.startsWith('global-commons://')) {
    const path = favicon.replace('global-commons://', '')
    return `${GLOBAL_COMMONS_CDN_BASE}/${path}`
  }

  // Data URI — use as-is, no network dependency
  if (favicon.startsWith('data:')) {
    return favicon
  }

  // External URL — use as-is
  if (favicon.startsWith('https://')) {
    return favicon
  }

  console.warn(`[SC] Unknown favicon format: ${favicon}`)
  return null
}
```

SC sets the favicon on inflate:

```typescript
const faviconUrl = resolveFavicon(eggConfig.favicon)
if (faviconUrl) {
  const link = document.querySelector('link[rel="icon"]') as HTMLLinkElement
    ?? Object.assign(document.createElement('link'), { rel: 'icon' })
  link.href = faviconUrl
  document.head.appendChild(link)
}
```

On EGG unload (tab swap, session end): SC restores its own favicon.

---

## Away Mode — Black Frame

When the user is away, SC renders a full-screen black overlay above all content.

### Visual elements (all near-black, never muted)

**Breathing pulse** — the overlay breathes at 4-second intervals, opacity cycling `1.0 → 0.97`. Signals alive, not crashed. Visual mute suppresses this.

**`hive>` ghost** — bottom-left corner, `rgba(255,255,255,0.04)`. Safety cue. Confirms ShiftCenter is running. Never suppressed by visual mute.

**Favicon** — if `away.showFavicon: true` (default), the EGG favicon renders at `away.faviconPosition` (default: `center`) at `rgba(255,255,255,0.06)`. Brand anchor in the dark. For corporate EGGs with embedded data URI favicons, this works fully offline.

**Away message** — if `away.message` is set, renders just above the favicon in the same near-black style. Example: `"Please lock your screen or interact to restore."` Never a modal, never a banner. Barely visible, legible on close inspection.

### CSS

```css
.sc-away-overlay {
  position: fixed;
  inset: 0;
  background: #000000;
  z-index: 9999;
  pointer-events: all;
  cursor: default;
}

/* Breathing — suppressed by .sc-visual-mute on body */
body:not(.sc-visual-mute) .sc-away-overlay {
  animation: sc-away-breathe 4s ease-in-out infinite;
}

@keyframes sc-away-breathe {
  0%, 100% { box-shadow: inset 0 0 0px rgba(255,255,255,0); }
  50%       { box-shadow: inset 0 0 40px rgba(255,255,255,0.015); }
}

/* hive> ghost — never suppressed */
.sc-away-ghost {
  position: absolute;
  bottom: 24px;
  left: 24px;
  font-family: var(--sd-font-mono);
  font-size: 13px;
  color: rgba(255,255,255,0.04);
  user-select: none;
  pointer-events: none;
}

/* Favicon */
.sc-away-favicon {
  position: absolute;
  width: 48px;
  height: 48px;
  opacity: 0.06;
  pointer-events: none;
}
.sc-away-favicon--center {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -60%);
}
.sc-away-favicon--bottom-right {
  bottom: 20px;
  right: 24px;
}

/* Away message */
.sc-away-message {
  position: absolute;
  font-family: var(--sd-font-sans);
  font-size: 12px;
  color: rgba(255,255,255,0.04);
  user-select: none;
  pointer-events: none;
  text-align: center;
  width: 100%;
}
.sc-away-favicon--center ~ .sc-away-message {
  top: calc(50% + 12px);
}
```

### Interaction

Any click or keypress anywhere on the overlay restores the frame instantly. SC dispatches `sc:away-end` on the bus. Clock resumes. If `away.welcomeBack: true`, Fr@nk emits `"Welcome back."` in Zone 2.

---

## `nodeId` Rules

`nodeId` is the most important field in an EGG config. Get it wrong and state does not survive EGG swaps.

- **Always declare `nodeId` explicitly** — never let SC generate it
- **Use stable, meaningful strings** — `"editor-main"` not `"pane-1"` not a UUID
- **Two EGGs that share a `nodeId` share state** — this is intentional for tab swaps (e.g. `code-default` and `code-zen` both declare `"editor-main"` so document content survives the swap)
- **Unique within a layout** — no two nodes in the same EGG should share a `nodeId`

---

## Complete Example — `code-default.egg.json`

```json
{
  "egg": "code-default",
  "version": "1.0.0",
  "displayName": "ShiftCenter Code",
  "description": "Fr@nk CLI + SDEditor + File Explorer.",
  "favicon": "global-commons://icons/code-default.png",

  "ui": {
    "hideMenuBar": false,
    "hideStatusBar": false,
    "hideTabBar": false,
    "hideActivityBar": false,
    "statusBarCurrencies": ["clock", "coin", "carbon"]
  },

  "tabs": [
    { "id": "tab-code", "eggId": "code-default", "label": "Code", "icon": "⌨️", "active": true  },
    { "id": "tab-zen",  "eggId": "code-zen",     "label": "Zen",  "icon": "🧘", "active": false }
  ],

  "away": {
    "idleThresholdMs": 300000,
    "blackoutDelayMs": 120000,
    "message": "Click or press any key to return.",
    "showFavicon": true,
    "faviconPosition": "center",
    "welcomeBack": true
  },

  "layout": {
    "type": "split",
    "direction": "horizontal",
    "ratio": 0.22,
    "children": [
      {
        "type": "app",
        "appType": "file-explorer",
        "nodeId": "explorer-main",
        "config": { "rootPath": "/", "showHidden": false }
      },
      {
        "type": "split",
        "direction": "horizontal",
        "ratio": 0.55,
        "children": [
          {
            "type": "app",
            "appType": "text",
            "nodeId": "editor-main",
            "config": {
              "format": "markdown",
              "label": "Document",
              "acceptEditsOn": false
            }
          },
          {
            "type": "app",
            "appType": "terminal",
            "nodeId": "frank-terminal-main",
            "config": {
              "zone2Dock": "bottom",
              "welcomeBanner": true
            }
          }
        ]
      }
    ]
  }
}
```

## Complete Example — `code-zen.egg.json`

```json
{
  "egg": "code-zen",
  "version": "1.0.0",
  "displayName": "Zen",
  "description": "Full screen SDEditor. No chrome. Just the document.",
  "favicon": "global-commons://icons/code-zen.png",

  "ui": {
    "hideMenuBar": true,
    "hideStatusBar": true,
    "hideTabBar": true,
    "hideActivityBar": true
  },

  "tabs": [],

  "away": {
    "idleThresholdMs": 300000,
    "blackoutDelayMs": 120000,
    "message": "Click or press any key to return.",
    "showFavicon": true,
    "faviconPosition": "center",
    "welcomeBack": false
  },

  "layout": {
    "type": "app",
    "appType": "text",
    "nodeId": "editor-main",
    "config": {
      "format": "markdown",
      "label": "Document",
      "acceptEditsOn": false,
      "hideHeader": false
    }
  }
}
```

---

## Adding a New EGG — Checklist

- [ ] Create `src/eggs/my-egg.egg.json` following this schema
- [ ] Add `nodeId` values explicitly — never generated
- [ ] Add favicon: `global-commons://` for platform EGGs, `data:` for custom/corporate
- [ ] Add to `src/eggs/index.ts` EGG_REGISTRY
- [ ] Add hostname mapping in `eggResolver.ts` if subdomain-based
- [ ] If sharing panes with another EGG across tab swaps — confirm `nodeId` values match intentionally
- [ ] Mark `_stub: true` if not fully implemented

---

*"Apps don't live on the server. They live as EGGs in memory."*
