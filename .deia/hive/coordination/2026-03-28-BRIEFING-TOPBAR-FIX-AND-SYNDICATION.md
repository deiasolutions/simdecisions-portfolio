# BRIEFING: Fix TopBar Icons + Add Canvas File Menu Syndication

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

Two problems:

1. TopBar has broken icon images (hamburger, kebab) that show alt text and compete with the brand name. The `resolveIcon('gc://icons/menu.svg')` call likely returns a path that doesn't exist. The user avatar circle covers the broken kebab text.

2. The File menu in the menu-bar is sparse because the canvas (sim) pane doesn't syndicate its file operations (save, export, import) to the menu bar via `menu:items-changed` bus events.

## Your Mission

### Read First

1. Read `browser/src/services/icons/iconResolver.ts` — understand what `resolveIcon()` returns for `gc://icons/` paths
2. Read `browser/src/primitives/top-bar/TopBar.tsx` — already provided above but read it fresh
3. Read `browser/src/primitives/top-bar/TopBar.css`
4. Check if `gc://icons/menu.svg` and `gc://icons/more.svg` actually exist — look in `browser/public/icons/` or wherever GC icons resolve to
5. Read `browser/src/apps/sim/` — find the main sim component to understand how it could syndicate menu items

### Fix 1: Replace broken icon images in TopBar

The `resolveIcon('gc://icons/menu.svg')` probably resolves to a path that 404s. Fix this:

**Option A (preferred):** Replace the `<img>` tags with inline SVG or simple text characters:
- Hamburger: use the character `☰` (U+2630) or three horizontal lines via CSS
- Kebab/More: use `⋮` (U+22EE, vertical ellipsis) or `⋯` (U+22EF, horizontal)

**Option B:** Check where GC icons resolve and fix the path.

Try Option B first. If icons don't exist, use Option A.

Also: check if the broken images are causing the "squished" layout. An `<img>` with a broken src may collapse to 0 width or expand with alt text, breaking flex layout.

### Fix 2: Clean up TopBar layout

After fixing icons, verify the layout is:
```
[☰ hamburger] [SimDecisions Canvas]  ---- spacer ----  [⋮ kebab] [avatar circle]
```

- Hamburger and kebab should be 32x32 buttons
- Brand text should be properly spaced
- Nothing should overlap
- The whole bar should stretch full width

### Fix 3: Add canvas file syndication to menu bar

The sim (canvas) pane needs to syndicate its file operations to the menu bar.

Read how the MenuBarPrimitive subscribes to `menu:items-changed` (it already does via the syndicatedMenus state).

Then find the sim component's initialization and add a bus emit that syndicates file operations:

Look for the sim pane's mount/useEffect. Add an emit like:

```ts
bus.send({
  type: 'menu:items-changed',
  sourcePane: paneId,
  target: 'chrome-menu',  // the menu-bar's nodeId
  data: {
    menus: [
      {
        targetMenu: 'file',
        groupLabel: 'Canvas',
        items: [
          { id: 'canvas.save', label: 'Save Diagram', shortcut: 'Ctrl+S' },
          { id: 'canvas.export-ir', label: 'Export PHASE-IR', shortcut: 'Ctrl+E' },
          { id: 'canvas.new-diagram', label: 'New Diagram', shortcut: 'Ctrl+N' },
        ]
      }
    ]
  }
})
```

BUT — before doing this, check how the bus subscription works in MenuBarPrimitive. It subscribes on `${paneId}--menus`. That means the source pane needs to send to that specific address. Read the code carefully to understand the addressing.

If the syndication mechanism is too complex to wire up quickly, just add the items directly to the File menu in MenuBarPrimitive.tsx as static items (New Diagram, Save, Export). We can make them dynamic later.

### Fix 4: Run tests

1. `npx vitest run top-bar` from browser/
2. `npx vitest run menu-bar` from browser/
3. Report results

## Deliverable

Write to: `.deia/hive/responses/20260328-TOPBAR-FIX-SYNDICATION.md`

## Constraints

- You MAY edit: TopBar.tsx, TopBar.css, MenuBarPrimitive.tsx, MenuBarPrimitive.css
- You MAY edit ONE sim-related file if adding syndication (identify which file)
- Read each file BEFORE editing
- If GC icons exist and resolve correctly, don't replace them — just fix the path
- If GC icons don't exist, use text/unicode alternatives (NOT emoji)

## Model Assignment

Sonnet — investigation + fixes.
