# ADR-SC-CHROME-001
## Shell Chrome as Pane Primitives

*Revision 3 — All open questions resolved. No ambiguity remains.*

| Field | Value |
|-------|-------|
| ADR ID | ADR-SC-CHROME-001 |
| Status | ACCEPTED |
| Date | 2026-03-26 |
| Revision | 3 — Tables fixed, A7 + B7 tasks added, markdown format |
| Author | Q88N + Claude (Architecture Session) |
| Supersedes | SPEC-HIVE-HOST-SHELL (chrome sections), SDK-APP-BUILDER v0.2.0 ui block, devOverride concept |
| Affects | Shell.tsx, PaneChrome.tsx, EGG ui/layout blocks, APP_REGISTRY, shell reducer, EGG loader/inflater |

---

## 1. Context

ShiftCenter Stage currently renders chrome bars (WorkspaceBar, MenuBar, ShellTabBar, MasterTitleBar, StatusBar) as shell-owned components that sit outside the pane tree. This creates two problems:

- **Failure coupling.** If any chrome component throws, the entire shell crashes and takes every pane with it. There is no error boundary between chrome and content.
- **Compositional rigidity.** Chrome elements cannot be rearranged, duplicated, or placed in non-standard positions. A status bar cannot appear in a sidebar. A menu bar cannot be scoped to a pane group.

Additionally, the current codebase has accumulated dead-weight: ShellTabBar is a broken legacy port (no flex CSS, z-index issues). MasterTitleBar is misnamed and redundant. StatusBar has an EGG property but no component. The devOverride flag shows chrome but prevents editing, which serves no useful purpose.

This ADR resolves all of these issues by establishing a single architectural rule: the shell renders pane boundaries and manages infrastructure. Everything the user sees is a pane primitive.

---

## 2. Hard Rules

These rules are non-negotiable and apply to all implementation tasks derived from this ADR.

### 2.1 Pane Isolation Rule

> **HARD RULE:** No primitive failure may crash the shell. The shell renders pane boundaries and error states. All visible content — including platform chrome — is a primitive running inside a pane boundary with an error boundary. A primitive that throws is replaced with an error fallback. Neighboring panes are unaffected.

The shell wraps every pane node in a React error boundary. If a primitive throws during render or in an effect, the error boundary catches it, logs the error to the event ledger, and renders a fallback UI. The pane boundary (border, focus ring) remains functional.

### 2.2 Shell Ownership Rule

The shell owns exactly five things:

- **Pane tree renderer.** Reads the layout tree, renders splits, dividers, pane boundaries. No content.
- **MessageBus.** Creates, routes, enforces mute levels. Per-window isolation.
- **GovernanceProxy.** Wraps each pane boundary, intercepts bus messages, enforces permissions and ethics config.
- **Shell reducer.** Manages tree structure (split, merge, reparent, focus, maximize). Undoable history. Five-branch root.
- **Error boundary per pane.** Catches throws, renders fallback, logs to event ledger.

The shell renders no visible content. It renders geometry and boundaries. Everything the user sees is a primitive.

### 2.3 Icon Convention

> **HARD RULE:** All icons in the schema are SVG references: `gc://icons/{name}.svg`. No unicode, no emoji, no font icons. The Global Commons hosts the icon set. The shell renders them as inline `<svg>` elements, sized to context (16px in pane chrome, 20px in bottom nav, 24px in floating toolbar). Color inherits from `currentColor` via CSS custom properties.

**Implementation note:** Global Commons does not exist yet. During development, stub the icon resolver: SVGs live in `browser/public/icons/`, the resolver maps `gc://icons/cursor.svg` → `/icons/cursor.svg`. Every component calls `resolveIcon()` — never hardcode local paths. When GC ships, swap the resolver to fetch from GC CDN. One function, one file, one swap.

### 2.4 Everything Is an EGG

> **HARD RULE:** There is no workspace file type. There are only EGGs. User modifications to layout create derived user EGGs stored in the user's hivenode space. The canonical EGG on Global Commons is never overwritten. The workspace concept is dead.

---

## 3. Chrome Components Become Pane Primitives

The following shell-owned components are refactored into registered appTypes in APP_REGISTRY:

| New appType | Replaces | Default Height | seamless |
|-------------|----------|----------------|----------|
| `top-bar` | WorkspaceBar | 36px (desktop) / 28px (mobile) | true |
| `menu-bar` | MenuBar | ~30px | true |
| `status-bar` | (unimplemented) | ~24px | true |
| `bottom-nav` | (new) | ~52px, mobile only | true |
| `tab-bar` | ShellTabBar + pane tab strip | ~32px | true |
| `toolbar` | (new, floating or docked) | ~40px when docked | true |
| `command-palette` | (new) | modal overlay | n/a (spotlight branch) |

Each primitive registers in APP_REGISTRY. Each receives config via the standard EGG layout node. Each communicates via the MessageBus using existing syndication protocols.

### 3.1 top-bar

Renders: hamburger (triggers left slideover), EGG brand icon + displayName, Three Currencies chip (tappable, expands to detail), kebab menu (opens command palette/action sheet), user avatar.

On mobile (chromeMode immersive/compact): shrinks to 28px, drops undo/redo and theme toggle (those move to kebab). Brand shows as favicon-sized icon, not wordmark.

Bus permissions: receives `RTD:*` broadcasts for currency chip, `topbar:*` commands. Emits shell actions via dispatch.

### 3.2 menu-bar

Renders: File/Edit/View/Help menus plus syndicated toolbar action buttons on the right side.

Subscribes to `menu:items-changed` for syndication from focused pane. Emits `menu:action-invoked` on click.

On mobile: hidden. Syndicated items surface through the command palette (opened via kebab).

Bus permissions: receives `menu:items-changed`, `menu:action-invoked`. Emits `menu:action-invoked`.

### 3.3 status-bar

Renders: Three Currencies display (CLOCK, COIN, CARBON), connection status (online/offline/syncing), active EGG name.

Configurable via pane config: which currencies to show, whether to show connection status, custom RTD metric keys.

Subscribes to `RTD:*` bus events. No polling. RTDs are emitted on change per the existing RTD protocol.

Can be placed anywhere: bottom of main layout (standard), in a sidebar (for multi-panel dashboards), multiple instances showing different metrics.

### 3.4 bottom-nav

Renders: 3–5 icon buttons for pane switching, anchored to the bottom of the viewport (thumb zone).

Icon sourcing: each pane provides its own icon via APP_REGISTRY entry or EGG pane config. Fallback: first letter of the appType label as a monogram. Mouseover/long-press shows the label.

Filtering: seamless panes are excluded by default (chrome primitives auto-filter out). The bottom-nav config supports explicit include/exclude lists to control ordering and visibility:

```json
{
  "type": "app", "appType": "bottom-nav",
  "nodeId": "chrome-nav", "seamless": true,
  "config": {
    "include": ["canvas-main", "side-chat", "sim-runner"],
    "exclude": []
  }
}
```

Tapping an icon dispatches `SET_FOCUS` for the matching nodeId. In immersive mode, this swaps the visible pane.

Only renders when chromeMode is compact or immersive (or auto on narrow viewports).

### 3.5 tab-bar

Renders: horizontal tab strip for mode switching within a pane group. Pinned tabs (no close button), closable tabs, and a + button for adding allowed tabs.

Binding: the tab-bar dispatches shell actions to control a target content pane. Config includes `targetSplit` (nodeId of the content pane). When user clicks a tab, the tab-bar dispatches `{ type: "SWAP_APP", nodeId: targetNodeId, appType: selectedAppType }`. The shell reducer handles the swap. The tab-bar is a control surface; the reducer is the authority.

On mobile: horizontally scrollable strip. Same behavior, swipeable.

### 3.6 toolbar (docked mode)

The floating toolbar (see Section 8) can alternatively render as a docked pane placed in the layout tree. Same tool definitions, inline rendering. Horizontal or vertical based on the split direction it sits in.

### 3.7 command-palette

Renders as a modal overlay in the spotlight branch. Triggered by Ctrl+Shift+P or the kebab menu.

Aggregates commands from three sources: the command registry (EGG commands block), syndicated menu items (from the focused pane), and shell actions (split, merge, maximize, etc.).

Fuzzy search over all aggregated commands. Keyboard navigable (arrow keys + Enter). Dismisses on Escape or selection.

On mobile: renders as a bottom sheet instead of a centered modal.

---

## 4. Five-Branch Pane Root

The root gains a fifth branch. Any appType can be placed in any branch. The appType defines what the pane does. The branch defines how it appears in the viewport. These are orthogonal.

```
root = {
  layout:    ShellTreeNode       // Main pane tree (splits, tiled)
  float:     AppNode[]           // Draggable overlays
  pinned:    AppNode[]           // Fixed-position overlays
  spotlight: AppNode | null      // Modal governance overlay
  slideover: AppNode[]           // Edge-anchored slide panels
}
```

### 4.1 Slideover Branch

A slideover is not a special primitive. It is a placement mode. Any pane can be placed in the slideover branch. The EGG layout declares slideoverss alongside the main layout children:

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "1fr", "24px"],
  "children": [ "..." ],
  "slideover": [
    {
      "type": "app", "appType": "channels-list",
      "nodeId": "channels",
      "meta": {
        "edge": "left",
        "width": "280px",
        "trigger": "hamburger",
        "dockable": true,
        "defaultDocked": false,
        "minDockWidth": 768
      }
    },
    {
      "type": "app", "appType": "properties-panel",
      "nodeId": "properties",
      "meta": {
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

#### Slideover meta fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `edge` | string | (required) | `"left"` \| `"right"` \| `"top"` \| `"bottom"`. Which edge the panel anchors to. |
| `width` / `height` | string | (required) | Panel size. Use width for left/right, height for top/bottom. CSS value (e.g. `"280px"`). |
| `trigger` | string | (required) | What opens the panel: `"hamburger"`, `"node-select"`, a bus message type, a command ID, or `"swipe"`. |
| `dockable` | boolean | false | Whether the pin button appears, allowing the user to dock the panel into the layout tree. |
| `defaultDocked` | boolean | false | If true, the panel starts docked (in the layout tree) on viewports wide enough. |
| `minDockWidth` | integer | 768 | Minimum viewport width (px) at which docking is allowed. Pin button hidden below this. |

#### Slideover overlay vs. dock behavior

**Overlay mode (default):** Panel slides out and floats over content. Content underneath does not move. Tap outside or swipe back to dismiss.

**Dock mode:** User taps pin button. The shell reparents the pane from the slideover branch to the layout branch, inserting it as a new child in the outermost split on the appropriate edge. Split ratios adjust. Content reflows. The panel becomes a regular layout pane with full PaneChrome (unless seamless).

**Undock:** User taps unpin. Pane moves back to slideover branch. Content reclaims space. Ratios readjust.

#### Docking safeguards

- The shell checks: `remaining = viewport_width - slideover_width`. If `remaining < 400px`, docking is refused and a toast is shown: "Not enough room to pin this panel."
- The 400px minimum remaining content width is a platform default, overridable per-EGG.
- If the user has a panel docked and resizes the browser below `minDockWidth`, the shell auto-undocks: reparents back to slideover, adjusts ratios, transitions to overlay mode. The panel does not vanish — it becomes an overlay.
- Auto-undock is undoable (goes on the history stack).
- Dock and undock operations are undoable layout actions (`DOCK_SLIDEOVER`, `UNDOCK_SLIDEOVER`).

#### Docking by chromeMode

| chromeMode | Viewport | Behavior |
|------------|----------|----------|
| full | > 1024px | Overlay by default. Pin to dock. Undock to return. Subject to `minDockWidth` and 400px remaining check. |
| compact | 600–1024px | Overlay by default. Docking allowed if `minDockWidth` is met and remaining content > 400px. |
| immersive | < 600px | Overlay only. Pin button hidden. No docking. |

### 4.2 Reparenting Between Branches

The existing `REPARENT_TO_BRANCH` action supports moving panes between all five branches. The right-click context menu (PaneContextMenu) offers all five placements:

- **Layout** — tiled in the split tree
- **Float** — draggable overlay
- **Pin** — fixed-position overlay
- **Spotlight** — modal governance overlay
- **Slide Over** — edge-anchored panel (submenu: pick edge)

---

## 5. Pane Lifecycle Events

Panes can be in several states without being destroyed. The shell emits lifecycle bus messages to each pane at state transitions:

| Event | Trigger | Pane should... |
|-------|---------|----------------|
| `pane:activated` | Pane gained focus | Resume full rendering, accept input |
| `pane:deactivated` | Another pane gained focus (this pane still visible) | Continue rendering, stop accepting primary input |
| `pane:hidden` | Pane moved behind a tab, minimized, or slideover dismissed | Pause expensive rendering (stop ReactFlow re-renders, animation frames). Bus subscriptions stay active. |
| `pane:revealed` | Pane brought back from hidden (tab switch, slideover open) | Resume rendering, scroll to latest state |
| `pane:destroyed` | Pane being unmounted (closed) | Cleanup, checkpoint state if needed |

These are bus messages with `target: nodeId`, not React lifecycle hooks. The pane subscribes to its own lifecycle events on the bus. The shell reducer emits them when dispatching `SET_FOCUS`, `SWAP_APP`, tab switches, minimize, `DOCK_SLIDEOVER`, `UNDOCK_SLIDEOVER`, etc.

**Critical implication: tabs do not destroy panes.** When the user switches from the Run tab to the Branch tab, the sim-runner pane receives `pane:hidden` but stays mounted. The simulation keeps running in the background. Bus subscriptions remain active. The pane can emit RTDs (like `RTD:sim_status`) that the status-bar displays, so the user sees simulation progress even while editing a branch.

---

## 6. Multi-Child Split Ratios

The current split node supports exactly two children with a single float ratio. Chrome-as-primitive requires splits with three or more children, some with fixed pixel sizes.

### 6.1 Ratio Syntax

The ratio field accepts an array of CSS Grid-style values:

```json
"ratio": ["36px", "1fr", "24px"]
```

| Unit | Meaning | Example |
|------|---------|---------|
| `Npx` | Fixed pixel size. Subtracted first from available space. | `"36px"` — always 36 pixels |
| `Nfr` | Fraction of remaining space after all px values are subtracted. | `"1fr"` — all remaining. `"0.6fr"` — 60% of remaining. |

### 6.2 Render Algorithm

1. Sum all `px` values. Subtract from container size.
2. Remaining space is distributed proportionally among `fr` values. `1fr` gets 100%. `0.6fr` and `0.4fr` split 60/40.
3. `fr` children can never starve `px` children. Fixed pixels are subtracted first, always.

**CSS Grid mapping:** the sugar syntax `["36px", "1fr", "24px"]` maps directly to `grid-template-rows: 36px 1fr 24px` (or `grid-template-columns` for vertical splits) at render time. The browser handles the layout math natively. No custom calculation needed.

### 6.3 Inflater Expansion

In the `.egg.md`, authors write the sugar syntax. The EGG inflater expands it to typed IR:

```json
// .egg.md (authored):
"ratio": ["36px", "0.6fr", "0.4fr", "24px"]

// .egg.ir.json (machine-generated):
"ratio": [
  { "value": 36, "unit": "px" },
  { "value": 0.6, "unit": "fr" },
  { "value": 0.4, "unit": "fr" },
  { "value": 24, "unit": "px" }
]
```

Components only receive the expanded form. The sugar is a human convenience in the `.egg.md`.

### 6.4 Backward Compatibility

Existing two-child splits with a single float ratio continue to work. The inflater detects the legacy form (a single number) and converts it:

```json
// Legacy: "ratio": 0.25
// Inflated: "ratio": [{ "value": 0.25, "unit": "fr" }, { "value": 0.75, "unit": "fr" }]
```

### 6.5 Viewport Containment

The outermost split container is `height: 100dvh` (dynamic viewport height, respects mobile browser chrome). No pane content may set its own height to push siblings off-screen. Each pane gets `overflow: hidden` (or `overflow: auto` for scrollable content like terminal/chat). The split ratio system guarantees everything fits within the viewport.

---

## 7. The seamless Property

Pane nodes with `seamless: true` render without PaneChrome (no drag handle, no bus mute button, no close X, no title bar). The content fills the pane boundary edge-to-edge. The pane still has an error boundary and still participates in the bus.

Chrome primitives (top-bar, menu-bar, status-bar, bottom-nav, tab-bar) default to `seamless: true`. Content primitives (canvas, terminal, chat) default to `seamless: false` and get full PaneChrome.

Seamless panes are not rearrangeable during normal use. See Section 11 (Design Mode) for how seamless panes become editable.

---

## 8. Floating Toolbar

The floating toolbar is a draggable tool palette owned by the active pane.

### 8.1 Ownership

The active pane owns the floating toolbar if and only if it has tools declared. When the user switches tabs, if the newly active pane has a toolbar block, the floating toolbar swaps to show those tools. If the new pane has no toolbar block, the toolbar minimizes or hides (depending on the `persistent` flag).

### 8.2 Toolbar Block (per-appType)

The toolbar fenced block in the EGG is an array. Each entry is a separate toolbar:

```json
[
  {
    "id": "workspace-tools",
    "persistent": true,
    "position": "top-right",
    "minimizedIcon": "gc://icons/workspace.svg",
    "tools": [
      { "id": "save", "icon": "gc://icons/save.svg", "action": "workspace.save" },
      { "id": "share", "icon": "gc://icons/share.svg", "action": "workspace.share" }
    ]
  },
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

### 8.3 Toolbar Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | string | (required) | Unique toolbar identifier. |
| `persistent` | boolean | false | If true, toolbar stays visible even when the owning pane loses focus or its tab is hidden. If false, toolbar hides on `pane:hidden` and shows on `pane:revealed`. |
| `position` | string | `"bottom-center"` | Default position. User can drag to any edge. Position persists in shell state. |
| `snapToEdges` | boolean | true | Toolbar snaps to viewport edges when dragged. |
| `minimizedIcon` | string | appType registry icon | SVG icon shown when toolbar is minimized to pill. |
| `tools` | array | (required) | Tool definitions. Each has `id`, `icon` (`gc://` SVG ref), and `action` (command registry ID). |

### 8.4 Minimize, Never Close

> **HARD RULE:** The floating toolbar is always either expanded or minimized (single-icon pill, ~36x36px). There is no closed state. The user controls size and position, not existence. A toolbar block being present means the toolbar exists for the lifetime of that pane.

Minimized state: a small draggable pill showing the `minimizedIcon`. Tap to expand. Drag to reposition. Always visible, always grabbable.

### 8.5 Drag Behavior

- Desktop: `mousedown` + `mousemove`. Mobile: `touchstart` + `touchmove`.
- Visible drag handle (6-dot grip pattern) so users know it moves.
- Snaps to edges, not free-floating.
- Default position: bottom-center on mobile (thumb zone), as declared in `position` field on desktop.
- Position saved per-pane in shell state. Persists across tab switches.

---

## 9. Pane-Level Tabs

### 9.1 pinned Property

Pane nodes with `pinned: true` cannot be closed. The close button (X) does not render on their tab. Used for anchor panes like the canvas. The pinned tab shows a pin icon instead of close.

### 9.2 allowedTabs Property

An array of appType definitions that the + button in the tab-bar offers. If absent, no + button renders. The EGG author controls what can be loaded as sibling tabs:

```json
"allowedTabs": [
  { "appType": "alterverse", "label": "Branch", "icon": "gc://icons/branch.svg" },
  { "appType": "sim-runner", "label": "Run", "icon": "gc://icons/play.svg" },
  { "appType": "ir-inspector", "label": "IR", "icon": "gc://icons/inspect.svg" },
  { "appType": "metrics", "label": "Metrics", "icon": "gc://icons/chart.svg" }
]
```

### 9.3 Tab-Bar → Content Pane Binding

The tab-bar primitive dispatches shell actions to control a target content pane. The tab-bar config includes a `targetSplit` field (nodeId of the content pane it controls).

When the user clicks a tab:

1. Tab-bar dispatches `{ type: "SWAP_APP", nodeId: targetNodeId, appType: selectedAppType }`.
2. The shell reducer handles the swap, replacing the content pane's appType.
3. The previous pane receives `pane:hidden` (not `pane:destroyed`). It stays mounted in the tree.
4. The new pane receives `pane:revealed` (or `pane:activated` if it gains focus).

This is consistent with how PaneChrome already dispatches `SPLIT`, `CLOSE_APP`, `MAXIMIZE`. Chrome components dispatch shell actions; they do not mutate state directly.

### 9.4 Lazy Loading

Tabs are lazy-loaded. The pane is not mounted until the user first clicks the tab. State persists in the shell tree via nodeId, so reopening a closed-and-reopened tab restores its last state. This is a performance win: Branch mode, Run mode, IR Inspector are heavy and only load when needed.

---

## 10. Responsive Chrome Modes

### 10.1 chromeMode

The ui block's `chromeMode` field governs how the shell adapts the pane tree to viewport size:

| Mode | Viewport | Behavior |
|------|----------|----------|
| `full` | > 1024px | All primitives render as placed. Split ratios honored. Full PaneChrome on non-seamless panes. |
| `compact` | 600–1024px | top-bar shrinks to 28px. menu-bar hidden (syndicated items surface in command palette via kebab). Pane chrome controls collapse to icons. |
| `immersive` | < 600px | Single-pane stack navigator. Only the focused pane visible. bottom-nav renders. Split tree preserved in state for restoration on wider viewports. |
| `auto` | (any) | Shell picks full/compact/immersive based on viewport width. Default. |

In immersive mode, the shell does not destroy the split tree. It renders only the focused pane at full viewport size. The bottom-nav provides navigation. Switching to a wider viewport restores the full split layout.

### 10.2 Revised ui Block (v0.3.0)

The EGG ui block shrinks to shell-level concerns only. All chrome visibility is governed by whether the layout tree includes the corresponding primitive. No boolean flags:

```json
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `chromeMode` | string | `"auto"` | `"full"` \| `"compact"` \| `"immersive"` \| `"auto"` |
| `commandPalette` | boolean | true | Enables Ctrl+Shift+P / kebab command palette |
| `akk` | boolean | true | Enables Assignable Key Kommands |

The `devOverride` flag is removed. See Section 11 (Design Mode) for its replacement.

### 10.3 Mobile Touch Targets

> **HARD RULE:** All touch targets in chrome must be minimum 44x44px (Apple HIG) or 48x48dp (Material). The current 22x22px ChromeBtn is too small for touch. On mobile, chrome buttons scale to 44px hit targets with visual icons staying at 16–20px inside the larger tap zone.

### 10.4 Mobile Gesture Mapping

| Gesture | Context | Action |
|---------|---------|--------|
| Swipe left/right | Immersive mode, on content area | Navigate between panes (previous/next in layout tree order) |
| Swipe down | On floating pane | Minimize floating pane to pill |
| Swipe down | On spotlight pane | Dismiss spotlight (if governance allows) |
| Long-press | On any pane content | Open bottom sheet context menu (Float, Pin, Spotlight, Slide Over, Close, bus mute) |
| Pinch-to-zoom | On canvas pane | Delegated to canvas (ReactFlow handles it) |
| Pinch-to-zoom | On terminal/chat | No-op (text panes do not zoom) |
| Tap | On bottom-nav icon | Focus that pane (immersive: swap visible pane) |
| Double-tap | On pane in compact mode | Maximize pane |
| Edge swipe left | iOS Safari | Back navigation — we do NOT fight this. Our swipe starts >30px from left edge. |
| Pull-to-refresh | Android Chrome | Disabled via `overscroll-behavior: none` on shell root |
| Long-press + drag | On floating toolbar | Reposition toolbar |
| Tap | On minimized toolbar pill | Expand toolbar |

---

## 11. Design Mode

Design mode replaces the old `devOverride` concept. `devOverride` showed chrome but prevented editing, which was useless. Design mode enables actual layout editing with guardrails.

### 11.1 Activation

Design mode is a runtime toggle available when the environment permits it: local development, or user has edit permissions on the EGG. Activated via the kebab menu or a keyboard shortcut.

### 11.2 Behavior When Active

- All seamless panes get minimal chrome: drag handle + basic pane operations (split, flip, resize) + close.
- Pane boundaries become visible with dashed borders.
- User can rearrange, resize, add, and remove panes.
- The add menu (+) is scoped:
  - Primitives from the original canonical EGG are always available (if you delete a canvas, you can add it back).
  - Primitives from the Global Commons library are available (public primitives anyone can use).
  - Proprietary primitives from other EGGs are NOT available. The canvas appType is only available inside the Canvas2 EGG and GC-published EGGs that include it.
- Save creates a new derived user EGG in the user's hivenode space. The canonical EGG is never overwritten.
- Exit design mode: minimal chrome disappears, seamless panes become seamless again.

### 11.3 Saving

When the user saves from design mode:

- The shell serializes the current layout tree into a new `.egg.md` file.
- Stored at: `home://eggs/{user-slug}/{eggId}.egg.md`
- The frontmatter includes `derivedFrom: "gc://eggs/{canonical-egg-id}.egg.md"` for lineage tracking.
- The canonical EGG on Global Commons is untouched.
- Next time the user loads this EGG, the platform checks for a user-derived version and offers a choice: load canonical or load user version.

---

## 12. Dirty Tracking and Persistence

### 12.1 Two Independent Dirty Flags

**Layout dirty:** The user has moved panes, changed split ratios, added/removed tabs, repositioned the floating toolbar, docked/undocked a slideover. Tracked by the shell. Any structural action (`SPLIT`, `MERGE`, `UPDATE_RATIO`, `REPARENT_TO_BRANCH`, `DOCK_SLIDEOVER`, `UNDOCK_SLIDEOVER`, `SWAP_APP`, etc.) sets layout dirty to true.

**Content dirty:** The user has unsaved work inside a pane. A half-written chat message, edited canvas nodes, IR changes. Tracked per-pane by the pane itself. Each pane reports its dirty state to the shell via a bus message:

```
pane:dirty-changed { nodeId, dirty: true/false }
```

The shell aggregates: if any pane reports dirty, the content dirty flag is true.

### 12.2 Autosave to Temp Storage

The shell autosaves on a timer (every 30–60 seconds) and on every structural layout change. Two targets simultaneously:

- **localStorage** — immediate, synchronous, survives browser refresh.
- **Cloud object storage** (via named volume `cloud://`) — async, survives device loss.

Key structure:

```
temp://eggs/{eggId}/{userId}/layout.json           // layout tree snapshot
temp://eggs/{eggId}/{userId}/content/{paneId}.json  // per-pane state
```

These are temp files, NOT saved EGGs. They have a 7-day TTL.

Each pane is responsible for serializing and deserializing its own content state. The shell stores and retrieves the blob without understanding pane internals.

### 12.3 On Close — Prompt If Dirty

If either dirty flag is true when the user closes the tab/app:

- "You have unsaved changes. Save as a new version?"
- **Save** — writes the user EGG to `home://eggs/{user-slug}/{eggId}.egg.md` (or updates it). Clears temp files.
- **Don't save** — temp files remain with 7-day TTL.
- **Cancel** — stay in the app.

If neither flag is dirty, close silently. No prompt. Temp files cleared.

The shell also sets the browser's `beforeunload` handler so the native "are you sure?" dialog fires on tab close.

### 12.4 On Return — Temp File Recovery

When the user loads the same EGG and temp files exist:

- "You have unsaved changes from [date]. Restore?"
- **Restore** — load the temp layout and content. Dirty flags set to true.
- **Discard** — delete temp files, load the canonical or user EGG as normal.

If the user ignores recovery and just uses the app, the temp files remain until the 7-day TTL expires. After 7 days, temp files are deleted silently. No additional warning.

**Cleanup mechanism:** Hivenode background task. Runs on hivenode boot and then every 24 hours: scan `temp://eggs/` for files where `ttl < now()`, delete them. For localStorage cleanup (browser side): the shell checks TTLs on app load and deletes expired entries silently.

### 12.5 Temp File Format

Layout temp:

```json
{
  "derivedFrom": "gc://eggs/canvas2.egg.md",
  "savedAt": "2026-03-26T14:30:00Z",
  "ttl": "2026-04-02T14:30:00Z",
  "tree": { "...full layout tree..." },
  "focusedPaneId": "canvas-main"
}
```

Content temp (per pane):

```json
{
  "nodeId": "canvas-main",
  "appType": "canvas",
  "savedAt": "2026-03-26T14:30:00Z",
  "ttl": "2026-04-02T14:30:00Z",
  "state": { "...pane-specific state blob..." }
}
```

---

## 13. Three Currencies in Chrome

CLOCK, COIN, CARBON surface in chrome via two mechanisms:

- **top-bar currency chip:** tappable pill subscribing to RTD bus events (`RTD:elapsed`, `RTD:cost_coin`, `RTD:cost_carbon`). Tapping expands to a detail view. On compact/immersive, shows only the most relevant currency (CLOCK by default).
- **status-bar full display:** renders all configured currencies with labels and values. Configurable via `currencies` array in pane config.

Both are bus subscribers. Neither polls. RTDs are emitted on change, not on timer, per the existing RTD protocol.

### 13.1 RTD Bus Protocol

The RTD protocol is specced conceptually but has no implementation in the current codebase. It is in scope for this ADR.

RTD message format (already defined in platform docs):

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

The ledger_writer and any service tracking CLOCK/COIN/CARBON emits RTD events on the bus. The status-bar and top-bar subscribe. Emitted on change, not on timer.

---

## 14. Chrome Primitive Bus Permissions

Each chrome primitive type declares its bus permissions in the APP_REGISTRY. GovernanceProxy enforces them at the pane boundary:

| appType | bus_receive | bus_emit |
|---------|------------|----------|
| `top-bar` | `RTD:*`, `topbar:*` | Shell actions via dispatch |
| `menu-bar` | `menu:items-changed`, `menu:action-invoked` | `menu:action-invoked` |
| `status-bar` | `RTD:*` | (none) |
| `bottom-nav` | (none) | Shell actions via dispatch (`SET_FOCUS`, `SPAWN_APP`) |
| `tab-bar` | `pane:activated`, `pane:hidden`, `pane:revealed` | Shell actions via dispatch (`SWAP_APP`) |
| `toolbar` | `toolbar:tools-changed` (if subscribing to active pane) | `toolbar:action-invoked` |
| `command-palette` | Command registry queries | Shell actions via dispatch |

Permissions are locked down by design at the registry level. A menu-bar cannot receive arbitrary messages. A status-bar cannot emit commands. GovernanceProxy enforces this identically to how it enforces permissions on any other pane.

---

## 15. Kill List

| Component / Concept | Reason | Replacement |
|---------------------|--------|-------------|
| ShellTabBar.tsx | Dead-weight legacy port. Broken CSS (`.tab-list` has no flex layout). Z-index goes behind panes. TabbedContainer is the real implementation. | `appType: tab-bar` primitive |
| MasterTitleBar.tsx | Misnamed, redundant. Acts as focused-pane bar, not master title. Syndication subscribers migrate to top-bar and toolbar primitives. | Syndication wired to new primitives |
| `devOverride` flag | Shows chrome but prevents editing. Serves no useful purpose. | Design mode (Section 11) |
| `hideMenuBar`, `hideStatusBar`, `hideTabBar`, `hideActivityBar` flags | Replaced by composition. Chrome presence is determined by whether the EGG layout tree includes the corresponding primitive. | Layout tree composition |
| Workspace file type / concept | Unnecessary. User modifications are derived EGGs. One file format, one loader, one mental model. | Derived user EGGs with `derivedFrom` lineage |
| `SAVE_WORKSPACE` / `LOAD_WORKSPACE` reducer actions | Replaced by EGG save/load. | `SAVE_EGG` / `LOAD_EGG` |

---

## 16. What Stays Unchanged

- **MessageBus.** Per-window isolation, mute levels, envelope format, platform invariants (`relay_bus`, `ledger_writer`, `gate_enforcer`, `settings_advertisement`, `metrics_advertisement`). No changes.
- **GovernanceProxy.** Wraps every pane. Intercepts `bus.send()` and `bus.subscribe()`. Validates permissions. Shows approval modal. Logs to event ledger. No changes.
- **PaneChrome (for non-seamless panes).** Drag handle, audio mute, bus mute (5-mode cycle), pin, collapse, close, notification dot (info/attention/governance), lock icon. No changes.
- **Shell reducer actions.** All existing layout, branch, pane state, and lifecycle actions remain. New actions added (`SWAP_APP`, `DOCK_SLIDEOVER`, `UNDOCK_SLIDEOVER`, lifecycle event emission).
- **Toolbar syndication protocol** (`toolbar:actions-changed`, `toolbar:action-invoked`). Stays. Floating toolbar subscribes as new consumer.
- **Menu syndication protocol** (`menu:items-changed`, `menu:action-invoked`). Stays. On mobile, syndicated items surface through command palette.
- **Right-click context menu** (PaneContextMenu). Updated to offer five placements (Layout, Float, Pin, Spotlight, Slide Over).
- **Four existing branches** (layout, float, pinned, spotlight). Unchanged. Fifth branch (slideover) added.

---

## 17. Reference Layout: SimDecisions Canvas2 EGG

Complete EGG layout showing all chrome primitives, slideoverss, and toolbar:

```json
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "32px", "1fr", "24px"],
  "children": [
    {
      "type": "app", "appType": "top-bar",
      "nodeId": "chrome-top", "seamless": true,
      "config": {
        "brand": "egg",
        "showCurrencyChip": true,
        "showKebab": true,
        "showAvatar": true
      }
    },
    {
      "type": "app", "appType": "tab-bar",
      "nodeId": "mode-tabs", "seamless": true,
      "config": {
        "targetSplit": "canvas-main",
        "pinned": ["canvas-main"],
        "allowedTabs": [
          { "appType": "alterverse", "label": "Branch",
            "icon": "gc://icons/branch.svg" },
          { "appType": "sim-runner", "label": "Run",
            "icon": "gc://icons/play.svg" },
          { "appType": "ir-inspector", "label": "IR",
            "icon": "gc://icons/inspect.svg" },
          { "appType": "metrics", "label": "Metrics",
            "icon": "gc://icons/chart.svg" }
        ]
      }
    },
    {
      "type": "app", "appType": "canvas",
      "nodeId": "canvas-main", "pinned": true,
      "config": { "irId": "main" }
    },
    {
      "type": "app", "appType": "status-bar",
      "nodeId": "chrome-status", "seamless": true,
      "config": {
        "currencies": ["clock", "coin", "carbon"],
        "showConnection": true
      }
    }
  ],
  "slideover": [
    {
      "type": "app", "appType": "node-palette",
      "nodeId": "palette",
      "meta": {
        "edge": "left", "width": "260px",
        "trigger": "hamburger",
        "dockable": true, "defaultDocked": false,
        "minDockWidth": 768
      }
    },
    {
      "type": "app", "appType": "properties-panel",
      "nodeId": "properties",
      "meta": {
        "edge": "right", "width": "300px",
        "trigger": "node-select",
        "dockable": true, "defaultDocked": false,
        "minDockWidth": 1024
      }
    }
  ]
}
```

Toolbar fenced block for the same EGG:

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

## 18. Reference Layout: Right Panel with Chat + Terminal + Status

Demonstrates chrome primitives composing freely. A status bar in a sidebar:

```json
{
  "type": "split", "direction": "vertical",
  "ratio": ["1fr", "280px"],
  "children": [
    {
      "type": "app", "appType": "canvas",
      "nodeId": "canvas-main"
    },
    {
      "type": "split", "direction": "horizontal",
      "ratio": ["0.4fr", "0.4fr", "80px"],
      "children": [
        { "type": "app", "appType": "chat", "nodeId": "side-chat" },
        { "type": "app", "appType": "terminal", "nodeId": "side-term" },
        {
          "type": "app", "appType": "status-bar",
          "nodeId": "side-status", "seamless": true,
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

## 19. Backward Compatibility

No inflater shim for old EGGs. All existing EGGs are retrofitted to the new standard. The SDK is updated to v0.3.0. Clean break.

The EGG inflater validates the new format and rejects old-style `hide*` flags with a clear error message directing the author to the migration guide.

---

## 20. Implementation Task Outline

For Q33NR to decompose into bee-dispatchable tasks. Each wave's tasks are independent within the wave and can be dispatched in parallel.

### Wave A: Foundation

- **A1.** Extend split node to support multi-child ratio arrays with CSS Grid-style syntax. Implement inflater expansion from sugar to IR. Render via CSS Grid (`grid-template-rows` / `grid-template-columns`).
- **A2.** Add error boundary wrapper to every pane node in Shell.tsx. Fallback UI shows error message + "Report" button. Error logged to event ledger with pane nodeId, appType, and stack trace.
- **A3.** Verify `seamless: true` suppresses PaneChrome completely (TASK-083 coverage). Ensure error boundary still wraps seamless panes.
- **A4.** Add fifth branch (slideover) to root. Implement `DOCK_SLIDEOVER` and `UNDOCK_SLIDEOVER` reducer actions (undoable). Implement `minDockWidth` and 400px remaining content safeguard. Implement auto-undock on viewport resize.
- **A5.** Implement pane lifecycle bus events (`pane:activated`, `pane:deactivated`, `pane:hidden`, `pane:revealed`, `pane:destroyed`). Shell reducer emits them on `SET_FOCUS`, `SWAP_APP`, tab switch, minimize, dock/undock, close.
- **A6.** Implement `pane:dirty-changed` bus message. Shell aggregates layout dirty (from structural actions) and content dirty (from pane reports). Wire `beforeunload` handler.
- **A7.** Implement RTD bus protocol. The `ledger_writer` and any service tracking CLOCK/COIN/CARBON emits RTD events on the bus. Message format: `{ type: "RTD", service_id, metric_key, value, unit, currency, timestamp }`. Emitted on change, not on timer.

### Wave B: Chrome Primitives

- **B1.** Register `appType: top-bar`. Port WorkspaceBar content. Subscribe to RTD bus events for currency chip. Implement slim 28px variant for compact/immersive modes. Implement kebab menu triggering command palette.
- **B2.** Register `appType: menu-bar`. Port MenuBar content. Subscribe to `menu:items-changed` syndication. On mobile, syndicated items route to command palette instead.
- **B3.** Register `appType: status-bar`. New build. Subscribe to RTD bus events. Config-driven currencies display. Can be placed anywhere in layout tree.
- **B4.** Register `appType: tab-bar`. Port TabbedContainer tab strip. Implement `allowedTabs` + `pinned`. Implement `SWAP_APP` dispatch to target content pane. Horizontal scroll on mobile.
- **B5.** Register `appType: bottom-nav`. New build. Auto-discover panes, exclude seamless by default, support explicit include/exclude config. Dispatch `SET_FOCUS` on tap. Only render in compact/immersive modes. 44px minimum touch targets.
- **B6.** Define bus permissions for each chrome primitive in APP_REGISTRY. Verify GovernanceProxy enforces them.
- **B7.** Build command palette component. Renders in spotlight branch. Aggregates commands from command registry, syndicated menu items, and shell actions. Fuzzy search, keyboard navigable. On mobile, renders as bottom sheet. Triggered by Ctrl+Shift+P or kebab menu.

### Wave C: Floating Toolbar

- **C1.** Build floating toolbar component. Draggable (mouse + touch). 6-dot drag handle. Snap to edges. Minimize to pill. Position persistence in shell state. Respond to `pane:hidden` / `pane:revealed` for persistent vs. non-persistent behavior.
- **C2.** Support toolbar array (multiple toolbars per pane). Persistent flag per toolbar.
- **C3.** Register `appType: toolbar` (docked mode). Same tool definitions, inline rendering.
- **C4.** Parse toolbar fenced block in EGG loader. Wire tool actions through command registry.

### Wave D: Responsive System

- **D1.** Implement chromeMode state in shell reducer. Viewport width listener for auto mode. Breakpoints: >1024 full, 600–1024 compact, <600 immersive.
- **D2.** Immersive mode: single-pane stack navigator. Preserve split tree in state. Render only focused pane. Swipe left/right between panes.
- **D3.** Compact mode: top-bar slim variant (28px). Menu-bar hidden, syndicate to command palette. Slideover docking subject to `minDockWidth`.
- **D4.** Mobile gesture layer: swipe navigation, long-press context menu (bottom sheet), pinch delegation, edge swipe avoidance (30px inset), `overscroll-behavior: none`. Touch target minimum 44x44px enforcement.

### Wave E: Design Mode + Persistence

- **E1.** Implement design mode toggle. Minimal chrome on seamless panes (drag handle + pane ops + close). Dashed pane boundaries. Scoped add menu (original EGG primitives + GC library).
- **E2.** Implement save-as-derived-EGG. Serialize layout tree to `.egg.md`. Store at `home://eggs/{user-slug}/{eggId}.egg.md`. Add `derivedFrom` lineage in frontmatter. On EGG load, check home volume for user-derived version before falling back to canonical.
- **E3.** Implement autosave to temp storage (localStorage + cloud object storage). 30–60 second timer + structural change trigger. 7-day TTL. Hivenode cleanup job (runs on boot + every 24 hours). Browser-side localStorage cleanup on app load.
- **E4.** Implement on-close prompt (save / don't save / cancel). Implement on-return recovery prompt (restore / discard).

### Wave F: Cleanup

- **F1.** Delete ShellTabBar.tsx.
- **F2.** Delete MasterTitleBar.tsx. Migrate syndication subscribers to top-bar and toolbar primitives.
- **F3.** Remove `devOverride` flag from EGG schema and all code paths.
- **F4.** Remove `hide*` flags from EGG schema. Update inflater to reject old-style flags with migration error.
- **F5.** Retrofit all existing EGGs to new layout-composition format.
- **F6.** Update SDK-APP-BUILDER to v0.3.0 documenting new ui block, layout primitives, toolbar block, slideover meta, ratio syntax, lifecycle events, dirty tracking, and design mode.

---

## 21. Consequences

### Positive

- **Crash isolation.** A chrome primitive failure no longer kills the shell.
- **Compositional freedom.** EGG authors place chrome anywhere in the layout tree. Status bars in sidebars. Multiple menu bars scoped to pane groups.
- **Governance on chrome.** Chrome primitives get GovernanceProxy wrapping automatically. TSaaS policies can restrict menu items by user tier.
- **Slideover docking.** Panels that are transient on mobile become persistent on desktop — one EGG layout serves both.
- **Background execution.** Simulations run behind tabs via pane lifecycle events. No destroy on tab switch.
- **Mobile-first.** The responsive system works because chrome is just panes that can be shown, hidden, rearranged, or replaced by viewport-appropriate alternatives (bottom-nav replaces activity bar).
- **One file format.** No workspace files. No separate state format. Everything is an EGG. One loader, one mental model.
- **Design mode with guardrails.** Users can customize layout without breaking canonical EGGs or accessing proprietary primitives from other products.

### Negative

- **More pane nodes in the tree.** A simple EGG that previously had zero explicit chrome now has 2–4 chrome panes in its layout block. EGG files are more verbose.
- **Multi-child split with CSS Grid-style ratios** is a non-trivial extension to the layout engine. The two-child float ratio was simple; the array form with px + fr semantics requires careful implementation.
- **Clean break on backward compatibility** means all existing EGGs must be manually retrofitted. No automated migration.
- **Slideover dock/undock with ratio readjustment** adds complexity to the shell reducer and requires animation work for smooth transitions.
- **Lifecycle bus events add a new protocol** that every pane must handle. Panes that ignore lifecycle events may waste resources (rendering while hidden) or show stale state (not refreshing when revealed).
