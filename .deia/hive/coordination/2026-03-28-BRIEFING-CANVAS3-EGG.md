# BRIEFING: Create canvas3.egg.md — New Chrome Layout

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

The canvas2 egg uses ported legacy components. We need a fresh canvas3 egg that uses the new chrome primitives properly. This is a clean-sheet layout using the current EGG spec.

## Your Mission

**Create `eggs/canvas3.egg.md` — a new canvas EGG with proper chrome layout.**

### Read First

1. Read `docs/specs/ADR-SC-CHROME-001-v3.md` — understand what top-bar, menu-bar, status-bar are supposed to be
2. Read `browser/src/primitives/top-bar/` — understand what TopBar renders and what config it accepts
3. Read `browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` — understand what config it accepts
4. Read `browser/src/primitives/status-bar/StatusBar.tsx` — understand what config it accepts
5. Read `eggs/canvas2.egg.md` — understand the existing canvas layout for reference (but we are NOT copying it)
6. Read `browser/src/apps/index.ts` — see all registered appTypes

### Layout Spec

The layout must be a vertical stack (horizontal splits) of 4 zones:

```
┌──────────────────────────────────────────┐
│  top-bar (36px)                          │  ← app title, branding
├──────────────────────────────────────────┤
│  menu-bar (30px)                         │  ← File, Edit, View, etc.
├──────────────────────────────────────────┤
│                                          │
│  main content (1fr)                      │
│  ┌────────┬──────────────────┬─────────┐ │
│  │palette │                  │  chat   │ │
│  │  &     │    canvas        │         │ │
│  │props   │    (sim)         │         │ │
│  │        │                  │         │ │
│  │ 20%    │      55%         │  25%    │ │
│  └────────┴──────────────────┴─────────┘ │
│                                          │
├──────────────────────────────────────────┤
│  status-bar (24px)                       │  ← clock, coin, carbon
└──────────────────────────────────────────┘
```

**Root split:** horizontal, ratio `["36px", "30px", "1fr", "24px"]`, 4 children:
1. `top-bar` (36px) — seamless, chrome pane
2. `menu-bar` (30px) — seamless, chrome pane
3. Main content split — vertical, ratio `[0.20, 0.55, 0.25]`, 3 children:
   a. Left panel: sidebar with palette + properties panels
   b. Center: sim canvas (appType: "sim")
   c. Right: chat (appType: "text-pane", renderMode: "chat")
4. `status-bar` (24px) — seamless, chrome pane

### Chrome Pane Configs

**top-bar:**
```json
{
  "type": "pane",
  "nodeId": "chrome-top",
  "appType": "top-bar",
  "label": "Top",
  "seamless": true,
  "config": {
    "appName": "SimDecisions Canvas",
    "showBreadcrumb": true
  }
}
```

**menu-bar:**
```json
{
  "type": "pane",
  "nodeId": "chrome-menu",
  "appType": "menu-bar",
  "label": "Menu",
  "seamless": true,
  "config": {}
}
```

**status-bar:**
```json
{
  "type": "pane",
  "nodeId": "chrome-status",
  "appType": "status-bar",
  "label": "Status",
  "seamless": true,
  "config": {
    "currencies": ["clock", "coin", "carbon"],
    "showConnection": true
  }
}
```

### Main Content Panes

**Left — Sidebar (palette + properties):**
```json
{
  "type": "pane",
  "nodeId": "canvas-sidebar",
  "appType": "sidebar",
  "label": "Sidebar",
  "chrome": false,
  "minWidth": 48,
  "config": {
    "panels": [
      {
        "id": "design",
        "icon": "✏",
        "label": "Components",
        "appType": "tree-browser",
        "config": {
          "adapter": "palette",
          "header": "Components",
          "searchPlaceholder": "Find component..."
        }
      },
      {
        "id": "properties",
        "icon": "⚙",
        "label": "Properties",
        "appType": "tree-browser",
        "config": {
          "adapter": "properties",
          "header": "Properties"
        }
      }
    ],
    "footerPanels": [],
    "defaultPanel": "design",
    "activityBarWidth": 48,
    "panelWidth": 240,
    "hideHeader": true,
    "hideActivityBar": false
  }
}
```

**Center — Canvas (sim):**
```json
{
  "type": "pane",
  "nodeId": "canvas-editor",
  "appType": "sim",
  "label": "Canvas",
  "chrome": false,
  "config": {
    "defaultMode": "design",
    "zoomEnable": true,
    "gridSnap": true,
    "links": {
      "from_palette": "canvas-sidebar",
      "to_properties": "canvas-sidebar"
    }
  }
}
```

**Right — Chat:**
```json
{
  "type": "pane",
  "nodeId": "canvas-chat",
  "appType": "text-pane",
  "label": "Chat",
  "chrome": false,
  "config": {
    "format": "markdown",
    "readOnly": true,
    "renderMode": "chat",
    "hideHeader": true
  }
}
```

### UI Block

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

NO legacy flags. No `menuBar`, no `statusBar`, no `hideMenuBar`, no `workspaceBar`. Chrome is in the layout tree only.

### Frontmatter

```yaml
---
egg: canvas3
version: 0.1.0
schema_version: 3
displayName: SimDecisions Canvas 3
description: Visual diagramming and design — new chrome layout with top-bar, menu-bar, status-bar. Triple-split main: palette+properties | canvas | chat.
author: daaaave-atx
favicon: /icons/canvas.svg
defaultRoute: /canvas3
license: MIT
_stub: false
---
```

### Other Blocks

Copy the following blocks from canvas2.egg.md:
- `commands` block (6 commands)
- `settings` block
- `away` block
- `startup` block
- `permissions` block
- `prompt` block

### Validation

After creating the file:
1. Run `npx vitest run eggToShell` from browser/ to make sure the egg parses
2. Verify by reading the file back that the layout JSON is valid
3. Confirm all 4 chrome zones are present: top-bar, menu-bar, main split, status-bar

## Deliverable

1. Create: `eggs/canvas3.egg.md`
2. Write response to: `.deia/hive/responses/20260328-CANVAS3-EGG.md`

Include:
- The full layout structure summary
- Validation results
- Any issues found

## Constraints

- Create ONLY the egg file and the response file
- Do NOT modify any source files
- Do NOT modify canvas2.egg.md
- Follow the EGG spec exactly (frontmatter, fenced code blocks with tags)
- 500 line max

## Model Assignment

Sonnet — file creation, validation.
