# SDK-APP-BUILDER v0.3.0
## EGG Layout Composition System

**Version:** 0.3.0
**Date:** 2026-03-27
**Supersedes:** SDK-APP-BUILDER v0.2.0
**Related:** ADR-SC-CHROME-001-v3

---

## Table of Contents

1. [Introduction](#introduction)
2. [Breaking Changes from v0.2.0](#breaking-changes-from-v020)
3. [UI Block Reference](#ui-block-reference)
4. [Multi-Child Ratio Syntax](#multi-child-ratio-syntax)
5. [Chrome Primitives Reference](#chrome-primitives-reference)
6. [Slideover Configuration](#slideover-configuration)
7. [Toolbar Definitions](#toolbar-definitions)
8. [Pane Lifecycle Events](#pane-lifecycle-events)
9. [Dirty Tracking API](#dirty-tracking-api)
10. [Design Mode](#design-mode)
11. [RTD Protocol](#rtd-protocol)
12. [Complete Examples](#complete-examples)
13. [Migration Guide](#migration-guide)

---

## Introduction

The EGG Layout Composition System v0.3.0 introduces a major architectural shift: **shell chrome becomes pane primitives**. Instead of boolean flags controlling visibility (`hideMenuBar`, `hideStatusBar`), chrome elements are now placed explicitly in the layout tree as `appType` primitives.

### Key Principles

1. **Chrome is just panes.** Top bars, menu bars, status bars, bottom navigation, tab bars, toolbars, and command palettes are all registered `appType` primitives that can be placed anywhere in the layout tree.

2. **Composition over configuration.** If your EGG includes a `status-bar` primitive in its layout, the status bar renders. If it doesn't, no status bar. No boolean flags needed.

3. **Seamless rendering.** Chrome primitives default to `seamless: true`, meaning they render without PaneChrome (no drag handle, no title bar, no close button). Content fills edge-to-edge.

4. **Five-branch root.** The shell root now has five branches: `layout` (main split tree), `float` (draggable overlays), `pinned` (fixed-position overlays), `spotlight` (modal governance), and `slideover` (edge-anchored panels).

5. **Multi-child splits.** Split nodes now support 3+ children with CSS Grid-style ratio syntax mixing fixed pixel sizes (`36px`) and fractional units (`1fr`, `0.6fr`).

---

## Breaking Changes from v0.2.0

### Removed Flags

The following boolean flags are **removed** and will cause validation errors:

- `hideMenuBar`
- `hideStatusBar`
- `hideTabBar`
- `hideActivityBar`
- `devOverride`

**Migration:** Remove these flags from your `ui` block. Control chrome visibility by including or excluding chrome primitives in your `layout` block.

### New UI Block Structure

**Old (v0.2.0):**

```json
{
  "hideMenuBar": true,
  "hideStatusBar": false,
  "devOverride": false
}
```

**New (v0.3.0):**

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

### Workspace Files Removed

There is no longer a separate "workspace" file type. User modifications to layout create **derived user EGGs** stored in the user's hivenode space (`home://eggs/{user-slug}/{eggId}.egg.md`). The canonical EGG on Global Commons is never overwritten.

---

## UI Block Reference

The `ui` fenced code block now contains only shell-level concerns. Chrome visibility is governed by the layout tree composition.

### Schema

```json
{
  "chromeMode": "auto" | "full" | "compact" | "immersive",
  "commandPalette": boolean,
  "akk": boolean
}
```

### Field Definitions

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `chromeMode` | string | `"auto"` | How the shell adapts the pane tree to viewport size. See Chrome Modes below. |
| `commandPalette` | boolean | `true` | Enables Ctrl+Shift+P / kebab menu command palette. |
| `akk` | boolean | `true` | Enables Assignable Key Kommands (keyboard shortcut system). |

### Chrome Modes

| Mode | Viewport | Behavior |
|------|----------|----------|
| `full` | > 1024px | All primitives render as placed. Split ratios honored. Full PaneChrome on non-seamless panes. |
| `compact` | 600–1024px | `top-bar` shrinks to 28px. `menu-bar` hidden (syndicated items surface in command palette via kebab). Pane chrome controls collapse to icons. |
| `immersive` | < 600px | Single-pane stack navigator. Only the focused pane visible. `bottom-nav` renders. Split tree preserved in state for restoration on wider viewports. |
| `auto` | (any) | Shell picks `full` / `compact` / `immersive` based on viewport width. **Default.** |

### Example

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

---

## Multi-Child Ratio Syntax

Split nodes now support 3+ children with CSS Grid-style ratio arrays mixing fixed pixel sizes and fractional units.

### Syntax

```json
"ratio": ["36px", "1fr", "24px"]
```

| Unit | Meaning | Example |
|------|---------|---------|
| `Npx` | Fixed pixel size. Subtracted first from available space. | `"36px"` — always 36 pixels |
| `Nfr` | Fraction of remaining space after all `px` values are subtracted. | `"1fr"` — all remaining. `"0.6fr"` — 60% of remaining. |

### Render Algorithm

1. Sum all `px` values. Subtract from container size.
2. Remaining space is distributed proportionally among `fr` values.
3. `fr` children can never starve `px` children. Fixed pixels are subtracted first, always.

### CSS Grid Mapping

The sugar syntax `["36px", "1fr", "24px"]` maps directly to `grid-template-rows: 36px 1fr 24px` (or `grid-template-columns` for vertical splits) at render time. The browser handles the layout math natively.

### Examples

**Three children: fixed header, flexible content, fixed footer**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "1fr", "24px"],
  "children": [
    { "type": "app", "appType": "top-bar", "nodeId": "chrome-top", "seamless": true },
    { "type": "app", "appType": "canvas", "nodeId": "canvas-main" },
    { "type": "app", "appType": "status-bar", "nodeId": "chrome-status", "seamless": true }
  ]
}
```

**Four children: header, tabs, content split 60/40, footer**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "32px", "0.6fr", "0.4fr", "24px"],
  "children": [
    { "type": "app", "appType": "top-bar", "nodeId": "chrome-top", "seamless": true },
    { "type": "app", "appType": "tab-bar", "nodeId": "mode-tabs", "seamless": true },
    { "type": "app", "appType": "canvas", "nodeId": "canvas-main" },
    { "type": "app", "appType": "chat", "nodeId": "side-chat" },
    { "type": "app", "appType": "status-bar", "nodeId": "chrome-status", "seamless": true }
  ]
}
```

### Backward Compatibility

Existing two-child splits with a single float ratio continue to work. The inflater detects the legacy form (a single number) and converts it:

```json
// Legacy: "ratio": 0.25
// Inflated: "ratio": [{ "value": 0.25, "unit": "fr" }, { "value": 0.75, "unit": "fr" }]
```

---

## Chrome Primitives Reference

All chrome elements are now registered `appType` primitives that can be placed anywhere in the layout tree.

### Available Primitives

| appType | Replaces | Default Height | seamless | Description |
|---------|----------|----------------|----------|-------------|
| `top-bar` | WorkspaceBar | 36px (desktop) / 28px (mobile) | true | Hamburger, brand, currencies, kebab, avatar |
| `menu-bar` | MenuBar | ~30px | true | File/Edit/View/Help menus + syndicated toolbar actions |
| `status-bar` | (unimplemented) | ~24px | true | Three Currencies display, connection status, active EGG name |
| `bottom-nav` | (new) | ~52px, mobile only | true | Icon buttons for pane switching (thumb zone) |
| `tab-bar` | ShellTabBar + pane tab strip | ~32px | true | Horizontal tab strip for mode switching within a pane group |
| `toolbar` | (new, docked mode) | ~40px when docked | true | Tool palette docked in layout tree |
| `command-palette` | (new) | modal overlay | n/a | Fuzzy search over commands, menu items, shell actions |

---

### top-bar

Renders: hamburger (triggers left slideover), EGG brand icon + displayName, Three Currencies chip (tappable, expands to detail), kebab menu (opens command palette/action sheet), user avatar.

On mobile (`chromeMode` immersive/compact): shrinks to 28px, drops undo/redo and theme toggle (those move to kebab). Brand shows as favicon-sized icon, not wordmark.

**Bus permissions:** receives `RTD:*` broadcasts for currency chip, `topbar:*` commands. Emits shell actions via dispatch.

#### Config Schema

```json
{
  "brand": "egg" | "wordmark" | "icon",
  "showCurrencyChip": boolean,
  "showKebab": boolean,
  "showAvatar": boolean
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `brand` | string | `"egg"` | `"egg"` (EGG icon + name), `"wordmark"` (ShiftCenter logo), `"icon"` (favicon only) |
| `showCurrencyChip` | boolean | `true` | Show the Three Currencies chip (tappable for detail) |
| `showKebab` | boolean | `true` | Show the kebab menu (opens command palette) |
| `showAvatar` | boolean | `true` | Show the user avatar |

#### Example

```json
{
  "type": "app",
  "appType": "top-bar",
  "nodeId": "chrome-top",
  "seamless": true,
  "config": {
    "brand": "egg",
    "showCurrencyChip": true,
    "showKebab": true,
    "showAvatar": true
  }
}
```

---

### menu-bar

Renders: File/Edit/View/Help menus plus syndicated toolbar action buttons on the right side.

Subscribes to `menu:items-changed` for syndication from focused pane. Emits `menu:action-invoked` on click.

On mobile: hidden. Syndicated items surface through the command palette (opened via kebab).

**Bus permissions:** receives `menu:items-changed`, `menu:action-invoked`. Emits `menu:action-invoked`.

#### Config Schema

```json
{}
```

No configuration options. Menu items are syndicated from the focused pane or defined in the EGG's `commands` block.

#### Example

```json
{
  "type": "app",
  "appType": "menu-bar",
  "nodeId": "chrome-menu",
  "seamless": true,
  "config": {}
}
```

---

### status-bar

Renders: Three Currencies display (CLOCK, COIN, CARBON), connection status (online/offline/syncing), active EGG name.

Configurable via pane config: which currencies to show, whether to show connection status, custom RTD metric keys.

Subscribes to `RTD:*` bus events. No polling. RTDs are emitted on change per the existing RTD protocol.

Can be placed anywhere: bottom of main layout (standard), in a sidebar (for multi-panel dashboards), multiple instances showing different metrics.

**Bus permissions:** receives `RTD:*`. No emits.

#### Config Schema

```json
{
  "currencies": string[],
  "showConnection": boolean,
  "customMetrics": string[]
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `currencies` | string[] | `["clock", "coin", "carbon"]` | Which currencies to display. Valid: `"clock"`, `"coin"`, `"carbon"`. |
| `showConnection` | boolean | `true` | Show connection status indicator (online/offline/syncing). |
| `customMetrics` | string[] | `[]` | Custom RTD metric keys to display (e.g., `["sim_status", "queue_depth"]`). |

#### Example

```json
{
  "type": "app",
  "appType": "status-bar",
  "nodeId": "chrome-status",
  "seamless": true,
  "config": {
    "currencies": ["clock", "coin", "carbon"],
    "showConnection": true
  }
}
```

---

### bottom-nav

Renders: 3–5 icon buttons for pane switching, anchored to the bottom of the viewport (thumb zone).

Icon sourcing: each pane provides its own icon via APP_REGISTRY entry or EGG pane config. Fallback: first letter of the appType label as a monogram. Mouseover/long-press shows the label.

Filtering: seamless panes are excluded by default (chrome primitives auto-filter out). The bottom-nav config supports explicit include/exclude lists to control ordering and visibility.

Tapping an icon dispatches `SET_FOCUS` for the matching nodeId. In immersive mode, this swaps the visible pane.

Only renders when `chromeMode` is `compact` or `immersive` (or `auto` on narrow viewports).

**Bus permissions:** none received. Emits shell actions via dispatch (`SET_FOCUS`, `SPAWN_APP`).

#### Config Schema

```json
{
  "include": string[],
  "exclude": string[]
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `include` | string[] | `[]` | Explicit list of nodeIds to show. If provided, only these panes appear. |
| `exclude` | string[] | `[]` | List of nodeIds to hide. Applied after auto-discovery. |

#### Example

```json
{
  "type": "app",
  "appType": "bottom-nav",
  "nodeId": "chrome-nav",
  "seamless": true,
  "config": {
    "include": ["canvas-main", "side-chat", "sim-runner"],
    "exclude": []
  }
}
```

---

### tab-bar

Renders: horizontal tab strip for mode switching within a pane group. Pinned tabs (no close button), closable tabs, and a + button for adding allowed tabs.

Binding: the tab-bar dispatches shell actions to control a target content pane. Config includes `targetSplit` (nodeId of the content pane). When user clicks a tab, the tab-bar dispatches `{ type: "SWAP_APP", nodeId: targetNodeId, appType: selectedAppType }`. The shell reducer handles the swap. The tab-bar is a control surface; the reducer is the authority.

On mobile: horizontally scrollable strip. Same behavior, swipeable.

**Bus permissions:** receives `pane:activated`, `pane:hidden`, `pane:revealed`. Emits shell actions via dispatch (`SWAP_APP`).

#### Config Schema

```json
{
  "targetSplit": string,
  "pinned": string[],
  "allowedTabs": Array<{
    "appType": string,
    "label": string,
    "icon": string
  }>
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `targetSplit` | string | (required) | NodeId of the content pane this tab-bar controls. |
| `pinned` | string[] | `[]` | NodeIds of tabs that cannot be closed. Close button replaced with pin icon. |
| `allowedTabs` | array | `[]` | Definitions of appTypes that the + button offers. If empty, no + button. |

#### Example

```json
{
  "type": "app",
  "appType": "tab-bar",
  "nodeId": "mode-tabs",
  "seamless": true,
  "config": {
    "targetSplit": "canvas-main",
    "pinned": ["canvas-main"],
    "allowedTabs": [
      { "appType": "alterverse", "label": "Branch", "icon": "gc://icons/branch.svg" },
      { "appType": "sim-runner", "label": "Run", "icon": "gc://icons/play.svg" },
      { "appType": "ir-inspector", "label": "IR", "icon": "gc://icons/inspect.svg" },
      { "appType": "metrics", "label": "Metrics", "icon": "gc://icons/chart.svg" }
    ]
  }
}
```

---

### toolbar (docked mode)

The floating toolbar can alternatively render as a docked pane placed in the layout tree. Same tool definitions, inline rendering. Horizontal or vertical based on the split direction it sits in.

See [Toolbar Definitions](#toolbar-definitions) for the toolbar fenced block schema.

#### Example

```json
{
  "type": "app",
  "appType": "toolbar",
  "nodeId": "docked-tools",
  "seamless": true,
  "config": {
    "toolbarId": "canvas-tools"
  }
}
```

---

### command-palette

Renders as a modal overlay in the spotlight branch. Triggered by Ctrl+Shift+P or the kebab menu.

Aggregates commands from three sources: the command registry (EGG commands block), syndicated menu items (from the focused pane), and shell actions (split, merge, maximize, etc.).

Fuzzy search over all aggregated commands. Keyboard navigable (arrow keys + Enter). Dismisses on Escape or selection.

On mobile: renders as a bottom sheet instead of a centered modal.

**Bus permissions:** queries command registry. Emits shell actions via dispatch.

#### Config Schema

```json
{}
```

No configuration options. Command sources are determined by the EGG's `commands` block and active pane syndication.

#### Example

```json
{
  "type": "app",
  "appType": "command-palette",
  "nodeId": "chrome-palette",
  "config": {}
}
```

---

## Slideover Configuration

Slideoverss are panes placed in the `slideover` array of a split node. They anchor to viewport edges and can overlay content or dock into the layout tree.

### Slideover Meta Fields

Pane nodes placed in the `slideover` array must include a `slideoverMeta` object.

```json
{
  "edge": "left" | "right" | "top" | "bottom",
  "width": string,
  "height": string,
  "trigger": string,
  "dockable": boolean,
  "defaultDocked": boolean,
  "minDockWidth": number
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `edge` | string | (required) | Which edge the panel anchors to: `"left"`, `"right"`, `"top"`, `"bottom"`. |
| `width` | string | (required for left/right) | Panel width. CSS value (e.g., `"280px"`). Use for left/right edges. |
| `height` | string | (required for top/bottom) | Panel height. CSS value (e.g., `"200px"`). Use for top/bottom edges. |
| `trigger` | string | (required) | What opens the panel: `"hamburger"`, `"node-select"`, a bus message type, a command ID, or `"swipe"`. |
| `dockable` | boolean | `false` | Whether the pin button appears, allowing the user to dock the panel into the layout tree. |
| `defaultDocked` | boolean | `false` | If true, the panel starts docked (in the layout tree) on viewports wide enough. |
| `minDockWidth` | number | `768` | Minimum viewport width (px) at which docking is allowed. Pin button hidden below this. |

### Overlay vs. Dock Behavior

**Overlay mode (default):** Panel slides out and floats over content. Content underneath does not move. Tap outside or swipe back to dismiss.

**Dock mode:** User taps pin button. The shell reparents the pane from the slideover branch to the layout branch, inserting it as a new child in the outermost split on the appropriate edge. Split ratios adjust. Content reflows. The panel becomes a regular layout pane with full PaneChrome (unless seamless).

**Undock:** User taps unpin. Pane moves back to slideover branch. Content reclaims space. Ratios readjust.

### Docking Safeguards

- The shell checks: `remaining = viewport_width - slideover_width`. If `remaining < 400px`, docking is refused and a toast is shown: "Not enough room to pin this panel."
- The 400px minimum remaining content width is a platform default, overridable per-EGG.
- If the user has a panel docked and resizes the browser below `minDockWidth`, the shell auto-undocks: reparents back to slideover, adjusts ratios, transitions to overlay mode. The panel does not vanish — it becomes an overlay.
- Auto-undock is undoable (goes on the history stack).
- Dock and undock operations are undoable layout actions (`DOCK_SLIDEOVER`, `UNDOCK_SLIDEOVER`).

### Examples

**Left edge palette (hamburger trigger)**

```json
{
  "type": "app",
  "appType": "node-palette",
  "nodeId": "palette",
  "slideoverMeta": {
    "edge": "left",
    "width": "260px",
    "trigger": "hamburger",
    "dockable": true,
    "defaultDocked": false,
    "minDockWidth": 768
  }
}
```

**Right edge properties panel (node-select trigger)**

```json
{
  "type": "app",
  "appType": "properties-panel",
  "nodeId": "properties",
  "slideoverMeta": {
    "edge": "right",
    "width": "300px",
    "trigger": "node-select",
    "dockable": true,
    "defaultDocked": false,
    "minDockWidth": 1024
  }
}
```

**Top edge notifications (bell-icon trigger, not dockable)**

```json
{
  "type": "app",
  "appType": "notifications",
  "nodeId": "notifications",
  "slideoverMeta": {
    "edge": "top",
    "height": "200px",
    "trigger": "bell-icon",
    "dockable": false
  }
}
```

---

## Toolbar Definitions

Toolbars are defined in the `toolbar` fenced code block as an array. Each entry is a separate toolbar.

### Toolbar Schema

```json
[
  {
    "id": string,
    "persistent": boolean,
    "position": string,
    "minimizedIcon": string,
    "snapToEdges": boolean,
    "tools": Array<{
      "id": string,
      "icon": string,
      "action": string
    }>
  }
]
```

### Toolbar Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | string | (required) | Unique toolbar identifier. |
| `persistent` | boolean | `false` | If true, toolbar stays visible even when the owning pane loses focus or its tab is hidden. If false, toolbar hides on `pane:hidden` and shows on `pane:revealed`. |
| `position` | string | `"bottom-center"` | Default position. User can drag to any edge. Position persists in shell state. Valid: `"top-left"`, `"top-center"`, `"top-right"`, `"bottom-left"`, `"bottom-center"`, `"bottom-right"`, `"left-center"`, `"right-center"`. |
| `minimizedIcon` | string | appType registry icon | SVG icon shown when toolbar is minimized to pill. Format: `gc://icons/{name}.svg`. |
| `snapToEdges` | boolean | `true` | Toolbar snaps to viewport edges when dragged. |
| `tools` | array | (required) | Tool definitions. Each has `id`, `icon` (`gc://` SVG ref), and `action` (command registry ID). |

### Tool Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique tool identifier within the toolbar. |
| `icon` | string | SVG icon reference: `gc://icons/{name}.svg`. |
| `action` | string | Command registry ID to invoke when tool is clicked. |

### Minimize, Never Close

The floating toolbar is always either expanded or minimized (single-icon pill, ~36x36px). There is no closed state. The user controls size and position, not existence. A toolbar block being present means the toolbar exists for the lifetime of that pane.

Minimized state: a small draggable pill showing the `minimizedIcon`. Tap to expand. Drag to reposition. Always visible, always grabbable.

### Examples

**Canvas tools (non-persistent, bottom-center)**

```json
{
  "id": "canvas-tools",
  "persistent": false,
  "position": "bottom-center",
  "minimizedIcon": "gc://icons/canvas.svg",
  "tools": [
    { "id": "select", "icon": "gc://icons/cursor.svg", "action": "canvas.select" },
    { "id": "add", "icon": "gc://icons/plus.svg", "action": "canvas.addNode" },
    { "id": "connect", "icon": "gc://icons/link.svg", "action": "canvas.connect" },
    { "id": "pan", "icon": "gc://icons/hand.svg", "action": "canvas.pan" },
    { "id": "undo", "icon": "gc://icons/undo.svg", "action": "canvas.undo" },
    { "id": "redo", "icon": "gc://icons/redo.svg", "action": "canvas.redo" }
  ]
}
```

**Workspace tools (persistent, top-right)**

```json
{
  "id": "workspace-tools",
  "persistent": true,
  "position": "top-right",
  "minimizedIcon": "gc://icons/workspace.svg",
  "tools": [
    { "id": "save", "icon": "gc://icons/save.svg", "action": "workspace.save" },
    { "id": "share", "icon": "gc://icons/share.svg", "action": "workspace.share" }
  ]
}
```

---

## Pane Lifecycle Events

Panes can be in several states without being destroyed. The shell emits lifecycle bus messages to each pane at state transitions.

### Event Types

| Event | Trigger | Pane should... |
|-------|---------|----------------|
| `pane:activated` | Pane gained focus | Resume full rendering, accept input |
| `pane:deactivated` | Another pane gained focus (this pane still visible) | Continue rendering, stop accepting primary input |
| `pane:hidden` | Pane moved behind a tab, minimized, or slideover dismissed | Pause expensive rendering (stop ReactFlow re-renders, animation frames). Bus subscriptions stay active. |
| `pane:revealed` | Pane brought back from hidden (tab switch, slideover open) | Resume rendering, scroll to latest state |
| `pane:destroyed` | Pane being unmounted (closed) | Cleanup, checkpoint state if needed |

### Critical Implication: Tabs Do Not Destroy Panes

When the user switches from the Run tab to the Branch tab, the sim-runner pane receives `pane:hidden` but stays mounted. The simulation keeps running in the background. Bus subscriptions remain active. The pane can emit RTDs (like `RTD:sim_status`) that the status-bar displays, so the user sees simulation progress even while editing a branch.

### Example: Canvas Pausing Render on Hidden

```typescript
useEffect(() => {
  const unsubscribe = bus.subscribe('pane:hidden', (msg) => {
    if (msg.target === nodeId) {
      // Stop React Flow re-renders
      setIsPaused(true)
    }
  })

  return unsubscribe
}, [bus, nodeId])

useEffect(() => {
  const unsubscribe = bus.subscribe('pane:revealed', (msg) => {
    if (msg.target === nodeId) {
      // Resume rendering
      setIsPaused(false)
    }
  })

  return unsubscribe
}, [bus, nodeId])
```

---

## Dirty Tracking API

The shell tracks two independent dirty flags: **layout dirty** and **content dirty**.

### Layout Dirty

The user has moved panes, changed split ratios, added/removed tabs, repositioned the floating toolbar, docked/undocked a slideover. Tracked by the shell. Any structural action (`SPLIT`, `MERGE`, `UPDATE_RATIO`, `REPARENT_TO_BRANCH`, `DOCK_SLIDEOVER`, `UNDOCK_SLIDEOVER`, `SWAP_APP`, etc.) sets layout dirty to true.

### Content Dirty

The user has unsaved work inside a pane. A half-written chat message, edited canvas nodes, IR changes. Tracked per-pane by the pane itself. Each pane reports its dirty state to the shell via a bus message:

```json
{
  "type": "pane:dirty-changed",
  "nodeId": "canvas-main",
  "dirty": true
}
```

The shell aggregates: if any pane reports dirty, the content dirty flag is true.

### Autosave to Temp Storage

The shell autosaves on a timer (every 30–60 seconds) and on every structural layout change. Two targets simultaneously:

- **localStorage** — immediate, synchronous, survives browser refresh.
- **Cloud object storage** (via named volume `cloud://`) — async, survives device loss.

Key structure:

```
temp://eggs/{eggId}/{userId}/layout.json           // layout tree snapshot
temp://eggs/{eggId}/{userId}/content/{paneId}.json  // per-pane state
```

These are temp files, NOT saved EGGs. They have a 7-day TTL.

### On Close — Prompt If Dirty

If either dirty flag is true when the user closes the tab/app:

- "You have unsaved changes. Save as a new version?"
- **Save** — writes the user EGG to `home://eggs/{user-slug}/{eggId}.egg.md` (or updates it). Clears temp files.
- **Don't save** — temp files remain with 7-day TTL.
- **Cancel** — stay in the app.

If neither flag is dirty, close silently. No prompt. Temp files cleared.

The shell also sets the browser's `beforeunload` handler so the native "are you sure?" dialog fires on tab close.

### On Return — Temp File Recovery

When the user loads the same EGG and temp files exist:

- "You have unsaved changes from [date]. Restore?"
- **Restore** — load the temp layout and content. Dirty flags set to true.
- **Discard** — delete temp files, load the canonical or user EGG as normal.

If the user ignores recovery and just uses the app, the temp files remain until the 7-day TTL expires. After 7 days, temp files are deleted silently. No additional warning.

### Example: Pane Reporting Content Dirty

```typescript
useEffect(() => {
  if (hasUnsavedChanges) {
    bus.send({
      type: 'pane:dirty-changed',
      nodeId: nodeId,
      dirty: true
    })
  } else {
    bus.send({
      type: 'pane:dirty-changed',
      nodeId: nodeId,
      dirty: false
    })
  }
}, [hasUnsavedChanges, bus, nodeId])
```

---

## Design Mode

Design mode replaces the old `devOverride` concept. `devOverride` showed chrome but prevented editing, which was useless. Design mode enables actual layout editing with guardrails.

### Activation

Design mode is a runtime toggle available when the environment permits it: local development, or user has edit permissions on the EGG. Activated via the kebab menu or a keyboard shortcut.

### Behavior When Active

- All seamless panes get minimal chrome: drag handle + basic pane operations (split, flip, resize) + close.
- Pane boundaries become visible with dashed borders.
- User can rearrange, resize, add, and remove panes.
- The add menu (+) is scoped:
  - Primitives from the original canonical EGG are always available (if you delete a canvas, you can add it back).
  - Primitives from the Global Commons library are available (public primitives anyone can use).
  - Proprietary primitives from other EGGs are NOT available. The canvas appType is only available inside the Canvas2 EGG and GC-published EGGs that include it.
- Save creates a new derived user EGG in the user's hivenode space. The canonical EGG is never overwritten.
- Exit design mode: minimal chrome disappears, seamless panes become seamless again.

### Saving

When the user saves from design mode:

- The shell serializes the current layout tree into a new `.egg.md` file.
- Stored at: `home://eggs/{user-slug}/{eggId}.egg.md`
- The frontmatter includes `derivedFrom: "gc://eggs/{canonical-egg-id}.egg.md"` for lineage tracking.
- The canonical EGG on Global Commons is untouched.
- Next time the user loads this EGG, the platform checks for a user-derived version and offers a choice: load canonical or load user version.

---

## RTD Protocol

RTD (Real-Time Data) messages are emitted by services tracking CLOCK, COIN, and CARBON. Chrome primitives like `top-bar` and `status-bar` subscribe to these bus events.

### RTD Message Format

```json
{
  "type": "RTD",
  "service_id": string,
  "metric_key": string,
  "value": number,
  "unit": string,
  "currency": "CLOCK" | "COIN" | "CARBON",
  "timestamp": string
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"RTD"`. |
| `service_id` | string | Service emitting the metric (e.g., `"ledger_writer"`). |
| `metric_key` | string | Metric identifier (e.g., `"cost_coin"`, `"elapsed"`, `"cost_carbon"`). |
| `value` | number | Numeric value of the metric. |
| `unit` | string | Unit of measurement (e.g., `"USD"`, `"seconds"`, `"gCO2e"`). |
| `currency` | string | One of `"CLOCK"`, `"COIN"`, `"CARBON"`. |
| `timestamp` | string | ISO 8601 timestamp of when the metric was measured. |

### Example: COIN RTD

```json
{
  "type": "RTD",
  "service_id": "ledger_writer",
  "metric_key": "cost_coin",
  "value": 0.18,
  "unit": "USD",
  "currency": "COIN",
  "timestamp": "2026-03-26T14:30:00Z"
}
```

### Example: CLOCK RTD

```json
{
  "type": "RTD",
  "service_id": "ledger_writer",
  "metric_key": "elapsed",
  "value": 127.5,
  "unit": "seconds",
  "currency": "CLOCK",
  "timestamp": "2026-03-26T14:30:00Z"
}
```

### Example: CARBON RTD

```json
{
  "type": "RTD",
  "service_id": "ledger_writer",
  "metric_key": "cost_carbon",
  "value": 2.4,
  "unit": "gCO2e",
  "currency": "CARBON",
  "timestamp": "2026-03-26T14:30:00Z"
}
```

### Protocol Notes

- RTDs are emitted on change, not on timer.
- Chrome primitives subscribe to `RTD:*` broadcasts (or specific metric keys like `RTD:cost_coin`).
- No polling. Services emit, subscribers receive.
- The `ledger_writer` and any service tracking currencies emit RTDs.

---

## Complete Examples

### Example 1: SimDecisions Canvas2 EGG

Complete EGG layout showing all chrome primitives, slideoverss, and toolbar.

**Frontmatter:**

```yaml
---
egg: canvas2
version: 0.3.0
displayName: Canvas2 — SimDecisions Designer
description: Visual DES modeling with multi-mode interface
author: ShiftCenter
favicon: gc://icons/canvas.svg
license: MIT
---
```

**UI Block:**

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

**Layout Block:**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "32px", "1fr", "24px"],
  "children": [
    {
      "type": "app",
      "appType": "top-bar",
      "nodeId": "chrome-top",
      "seamless": true,
      "config": {
        "brand": "egg",
        "showCurrencyChip": true,
        "showKebab": true,
        "showAvatar": true
      }
    },
    {
      "type": "app",
      "appType": "tab-bar",
      "nodeId": "mode-tabs",
      "seamless": true,
      "config": {
        "targetSplit": "canvas-main",
        "pinned": ["canvas-main"],
        "allowedTabs": [
          { "appType": "alterverse", "label": "Branch", "icon": "gc://icons/branch.svg" },
          { "appType": "sim-runner", "label": "Run", "icon": "gc://icons/play.svg" },
          { "appType": "ir-inspector", "label": "IR", "icon": "gc://icons/inspect.svg" },
          { "appType": "metrics", "label": "Metrics", "icon": "gc://icons/chart.svg" }
        ]
      }
    },
    {
      "type": "app",
      "appType": "canvas",
      "nodeId": "canvas-main",
      "pinned": true,
      "config": { "irId": "main" }
    },
    {
      "type": "app",
      "appType": "status-bar",
      "nodeId": "chrome-status",
      "seamless": true,
      "config": {
        "currencies": ["clock", "coin", "carbon"],
        "showConnection": true
      }
    }
  ],
  "slideover": [
    {
      "type": "app",
      "appType": "node-palette",
      "nodeId": "palette",
      "slideoverMeta": {
        "edge": "left",
        "width": "260px",
        "trigger": "hamburger",
        "dockable": true,
        "defaultDocked": false,
        "minDockWidth": 768
      }
    },
    {
      "type": "app",
      "appType": "properties-panel",
      "nodeId": "properties",
      "slideoverMeta": {
        "edge": "right",
        "width": "300px",
        "trigger": "node-select",
        "dockable": true,
        "defaultDocked": false,
        "minDockWidth": 1024
      }
    }
  ]
}
```

**Toolbar Block:**

```json
[
  {
    "id": "canvas-tools",
    "persistent": false,
    "position": "bottom-center",
    "minimizedIcon": "gc://icons/canvas.svg",
    "tools": [
      { "id": "select", "icon": "gc://icons/cursor.svg", "action": "canvas.select" },
      { "id": "add", "icon": "gc://icons/plus.svg", "action": "canvas.addNode" },
      { "id": "connect", "icon": "gc://icons/link.svg", "action": "canvas.connect" },
      { "id": "pan", "icon": "gc://icons/hand.svg", "action": "canvas.pan" },
      { "id": "undo", "icon": "gc://icons/undo.svg", "action": "canvas.undo" },
      { "id": "redo", "icon": "gc://icons/redo.svg", "action": "canvas.redo" }
    ]
  }
]
```

---

### Example 2: Right Panel with Chat + Terminal + Status

Demonstrates chrome primitives composing freely. A status bar in a sidebar.

```json
{
  "type": "split",
  "direction": "vertical",
  "ratio": ["1fr", "280px"],
  "children": [
    {
      "type": "app",
      "appType": "canvas",
      "nodeId": "canvas-main"
    },
    {
      "type": "split",
      "direction": "horizontal",
      "ratio": ["0.4fr", "0.4fr", "80px"],
      "children": [
        { "type": "app", "appType": "chat", "nodeId": "side-chat" },
        { "type": "app", "appType": "terminal", "nodeId": "side-term" },
        {
          "type": "app",
          "appType": "status-bar",
          "nodeId": "side-status",
          "seamless": true,
          "config": {
            "currencies": ["clock", "coin"],
            "showConnection": true
          }
        }
      ]
    }
  ]
}
```

---

## Migration Guide

Upgrading from SDK v0.2.0 to v0.3.0 requires changes to your EGG files. This guide walks through the steps.

### Step 1: Remove Old Flags from UI Block

**Before (v0.2.0):**

```json
{
  "hideMenuBar": true,
  "hideStatusBar": false,
  "hideTabBar": false,
  "hideActivityBar": true,
  "devOverride": false
}
```

**After (v0.3.0):**

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

**What changed:**
- All `hide*` flags removed.
- `devOverride` removed (replaced by design mode, a runtime toggle).
- Chrome visibility is now controlled by layout tree composition.

---

### Step 2: Add Chrome Primitives to Layout Tree

If you want a menu bar, explicitly add it to your layout. If you don't, omit it.

**Before (v0.2.0):**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": 0.75,
  "children": [
    { "type": "app", "appType": "canvas", "nodeId": "canvas-main" },
    { "type": "app", "appType": "chat", "nodeId": "side-chat" }
  ]
}
```

Menu bar was implicitly rendered because `hideMenuBar` was not set.

**After (v0.3.0):**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr", "24px"],
  "children": [
    {
      "type": "app",
      "appType": "top-bar",
      "nodeId": "chrome-top",
      "seamless": true,
      "config": { "brand": "egg", "showCurrencyChip": true }
    },
    {
      "type": "app",
      "appType": "menu-bar",
      "nodeId": "chrome-menu",
      "seamless": true,
      "config": {}
    },
    {
      "type": "split",
      "direction": "vertical",
      "ratio": ["0.75fr", "0.25fr"],
      "children": [
        { "type": "app", "appType": "canvas", "nodeId": "canvas-main" },
        { "type": "app", "appType": "chat", "nodeId": "side-chat" }
      ]
    },
    {
      "type": "app",
      "appType": "status-bar",
      "nodeId": "chrome-status",
      "seamless": true,
      "config": { "currencies": ["clock", "coin", "carbon"] }
    }
  ]
}
```

**What changed:**
- Chrome primitives are now explicit layout children.
- Ratio changed from single float to array of CSS Grid-style units.
- Content split nested inside outer split (to accommodate chrome).

---

### Step 3: Update Ratio Syntax for Multi-Child Splits

If you have splits with 3+ children, update the ratio array to use CSS Grid-style units.

**Before (v0.2.0):**

Two-child splits only. Ratio was a single float.

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": 0.6,
  "children": [ "...", "..." ]
}
```

**After (v0.3.0):**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["0.6fr", "0.4fr"],
  "children": [ "...", "..." ]
}
```

Or with fixed chrome and flexible content:

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "1fr", "24px"],
  "children": [ "...", "...", "..." ]
}
```

**Backward compatibility:** The inflater still accepts single-float ratios for two-child splits and converts them automatically. But for future-proofing, use the array syntax.

---

### Step 4: Mark Chrome Panes as Seamless

All chrome primitives should have `seamless: true` (this is the default for chrome types, but explicit is better).

```json
{
  "type": "app",
  "appType": "top-bar",
  "nodeId": "chrome-top",
  "seamless": true,
  "config": { ... }
}
```

---

### Step 5: Convert Activity Bar to Bottom Nav (Mobile)

If you used an activity bar (sidebar with icons) in v0.2.0, it likely becomes a `bottom-nav` in v0.3.0 for mobile-first design.

**Before (v0.2.0):**

Activity bar was implicit, controlled by `hideActivityBar`.

**After (v0.3.0):**

```json
{
  "type": "app",
  "appType": "bottom-nav",
  "nodeId": "chrome-nav",
  "seamless": true,
  "config": {
    "include": ["canvas-main", "side-chat", "sim-runner"]
  }
}
```

Only renders when `chromeMode` is `compact` or `immersive` (or `auto` on narrow viewports).

---

### Step 6: Add Slideover Panels (Optional)

If you had always-visible sidebars (like a node palette), convert them to slideoverss for responsive behavior.

**Before (v0.2.0):**

```json
{
  "type": "split",
  "direction": "vertical",
  "ratio": 0.2,
  "children": [
    { "type": "app", "appType": "node-palette", "nodeId": "palette" },
    { "type": "app", "appType": "canvas", "nodeId": "canvas-main" }
  ]
}
```

Palette always visible, steals 20% of viewport.

**After (v0.3.0):**

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "1fr", "24px"],
  "children": [
    { "type": "app", "appType": "top-bar", "nodeId": "chrome-top", "seamless": true },
    { "type": "app", "appType": "canvas", "nodeId": "canvas-main" },
    { "type": "app", "appType": "status-bar", "nodeId": "chrome-status", "seamless": true }
  ],
  "slideover": [
    {
      "type": "app",
      "appType": "node-palette",
      "nodeId": "palette",
      "slideoverMeta": {
        "edge": "left",
        "width": "260px",
        "trigger": "hamburger",
        "dockable": true,
        "defaultDocked": false,
        "minDockWidth": 768
      }
    }
  ]
}
```

Palette is now a slideover. Opens on hamburger click. Can be docked on wide viewports.

---

### Step 7: Add Toolbar Definitions (Optional)

If your EGG has floating tool palettes, define them in the `toolbar` fenced block.

**New in v0.3.0:**

````markdown
```toolbar
[
  {
    "id": "canvas-tools",
    "persistent": false,
    "position": "bottom-center",
    "minimizedIcon": "gc://icons/canvas.svg",
    "tools": [
      { "id": "select", "icon": "gc://icons/cursor.svg", "action": "canvas.select" },
      { "id": "add", "icon": "gc://icons/plus.svg", "action": "canvas.addNode" }
    ]
  }
]
```
````

---

### Step 8: Validate Your EGG

Run the EGG inflater on your updated `.egg.md` file. Check for validation errors.

Common errors:
- Old `hide*` flags present → remove them.
- `devOverride` flag present → remove it.
- `ratio` is a float but split has 3+ children → convert to array.
- Chrome primitive missing `seamless: true` → add it (or rely on default).
- Slideover pane missing `slideoverMeta` → add the meta object.

---

### Summary of Breaking Changes

| v0.2.0 | v0.3.0 | Action |
|--------|--------|--------|
| `hideMenuBar` flag | Layout composition | Remove flag. Add `menu-bar` primitive to layout if needed. |
| `hideStatusBar` flag | Layout composition | Remove flag. Add `status-bar` primitive to layout if needed. |
| `hideTabBar` flag | Layout composition | Remove flag. Add `tab-bar` primitive to layout if needed. |
| `hideActivityBar` flag | `bottom-nav` primitive | Remove flag. Add `bottom-nav` primitive for mobile. |
| `devOverride` flag | Design mode | Remove flag. Use design mode runtime toggle. |
| Single float ratio (2 children) | Array ratio | Convert to array (backward compatible, but explicit is better). |
| Implicit chrome rendering | Explicit chrome primitives | Add chrome primitives to layout tree. |
| Always-visible sidebars | Slideoverss | Convert to `slideover` array with `slideoverMeta`. |

---

## Conclusion

SDK-APP-BUILDER v0.3.0 introduces a compositional layout system where chrome elements are first-class pane primitives. This enables:

- **Crash isolation.** A chrome primitive failure no longer kills the shell.
- **Compositional freedom.** Status bars in sidebars. Multiple menu bars scoped to pane groups.
- **Responsive design.** Slideoverss that dock on desktop, overlay on mobile.
- **Design mode with guardrails.** Users can customize layout without breaking canonical EGGs.
- **One file format.** No workspace files. Everything is an EGG.

For questions or support, see the [CLAUDE.md](../../CLAUDE.md) or contact the ShiftCenter team.

---

**End of SDK-APP-BUILDER v0.3.0**
