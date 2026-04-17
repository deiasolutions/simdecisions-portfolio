# SPEC-SCAFFOLD-001: Scaffold and Float Layout Service

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** SHELL
**T-Shirt Size:** L
**Depends On:** SPEC-CANVAS-SURFACE-001, split_pane (SPECCED), scene_system (SPECCED)

---

## 1. Purpose

The Scaffold Service manages named layout regions and floating panes over a `canvas_surface`
backdrop. It is the layout layer for EGGs that use `surface: infinite`.

HiveHostPanes in tiled mode fills the screen with panes. In scaffold mode, HiveHostPanes
manages a set of named regions anchored to the viewport (the Glass Layer), while other panes
float freely in the World Layer or are pinned to the Glass Layer as HUD elements.

The scaffold does not replace HiveHostPanes — it is a mode of it.

---

## 2. Layout Modes (Full Model)

Three modes, all implemented by HiveHostPanes + scaffold_service:

| Mode | Description | When Used |
|------|-------------|-----------|
| `tiled` | Screen-bounded. Panes fill every pixel. No canvas backdrop. | Desktop productivity EGGs |
| `scaffold` | canvas_surface active. Named regions + floaters. | Meeting rooms, whiteboards, spatial workspaces |
| `responsive` | EGG declares breakpoints. Morphs between tiled and scaffold. | Any EGG that needs to work across device sizes |

The mode is declared in the EGG config. Most EGGs will use `responsive` with scaffold behavior
at larger viewports and a simplified layout at smaller viewports.

---

## 3. Scaffold Regions

A scaffold region is a named, Glass Layer pane anchored to a viewport position. Regions are
declared by the EGG architect.

```yaml
scaffold:
  regions:
    - id: right-panel-top
      anchor: top-right
      width: 320px
      height: 50vh
      defaultApplet: kanban
      defaultConfig:
        columns: [Backlog, In Progress, Done]
      label: Backlog

    - id: right-panel-bottom
      anchor: bottom-right
      width: 320px
      height: calc(50vh - 32px)   # 32px = divider
      defaultApplet: text
      defaultConfig:
        format: markdown
        label: Agenda
      label: Agenda

    - id: left-panel
      anchor: top-left
      width: 280px
      height: 100vh
      defaultApplet: chat
      label: Team Chat

    - id: hud-timer
      anchor: top-center
      width: 180px
      height: 48px
      defaultApplet: timer
      pin: viewport             # Glass Layer HUD — never scrolls
      dismissible: false
```

### Anchor Values

`top-left` | `top-center` | `top-right`
`middle-left` | `center` | `middle-right`
`bottom-left` | `bottom-center` | `bottom-right`

---

## 4. Pin Types

Every pane in a scaffold EGG declares a pin type:

| Pin Type | Layer | Behavior |
|----------|-------|---------|
| `viewport` | Glass Layer | Fixed to screen position. Never moves. HUD elements. |
| `scaffold` | Glass Layer | Anchored to named viewport region. Responsive rules apply. |
| `canvas` | World Layer | Anchored to world-space coordinate. Moves with pan/zoom. |
| `float` | Glass Layer | Free-floating, draggable by user within Glass Layer. |
| `float-world` | World Layer | Free-floating within world space. Moves with canvas. |

---

## 5. Breakpoint and Responsive Morphing

The architect defines per-region behavior at each breakpoint. The user can override within
bounds the architect sets.

### Breakpoint Definition

```yaml
breakpoints:
  - id: desktop
    minWidth: 1280
    orientation: any

  - id: tablet-landscape
    minWidth: 768
    maxWidth: 1279
    orientation: landscape

  - id: tablet-portrait
    minWidth: 768
    maxWidth: 1279
    orientation: portrait

  - id: phone
    maxWidth: 767
    orientation: any
```

### Per-Region Breakpoint Rules

Each region declares `sizeMode` per breakpoint:

| sizeMode | Behavior |
|----------|---------|
| `fixed` | Region keeps architect-defined size. Content adapts inside. |
| `shrink` | Region shrinks to a configurable minimum. Content reflows. |
| `hide` | Region is hidden. Content accessible via tab or drawer. |
| `float` | Region becomes a user-draggable floater within the Glass Layer. |
| `drawer` | Region slides in from an edge. Triggered by swipe or button. |
| `tab` | Region collapses to a tab in a tab bar at the screen edge. |
| `sheet` | Region becomes a bottom sheet (mobile standard pattern). |

```yaml
- id: right-panel-top
  anchor: top-right
  width: 320px
  sizeMode:
    desktop: fixed
    tablet-landscape: shrink
    tablet-portrait: drawer
    phone: sheet
  userOverride: true          # user can change sizeMode within bounds
  userOverrideBounds:         # what the user is allowed to change to
    - fixed
    - shrink
    - hide
```

### The Key Design Decision (Locked)

The scaffold does NOT auto-collapse based on viewport width alone. The architect defines the
rules. A tablet in landscape with a 1024px viewport can receive `sizeMode: fixed` — the
scaffold stays full size and the canvas area shrinks to accommodate it. This was Dave's
explicit decision: behavior is architect-defined, not assumed.

---

## 6. nav_joystick

A small circular Glass Layer HUD element for navigating the World Layer on touch devices
or when keyboard is preferred.

```yaml
navJoystick:
  visible: auto              # auto = show on touch devices, hide on desktop
  position: bottom-left      # Glass Layer anchor
  size: 64px
  activationGesture: long-press   # long press on empty canvas to show
  dismissGesture: tap-outside
  sensitivity: 1.0           # pan speed multiplier
```

**Controls:**
- Drag in any direction → pan canvas
- Two-finger drag (tablet) → also pans (alternative to joystick)
- Arrow keys when canvas focused → pan (step size configurable)
- Long press on joystick → shows zoom controls (+/-)

The nav_joystick is a reusable Glass Layer primitive, not a meeting-room-specific feature.
Any EGG with `surface: infinite` can declare it.

---

## 7. Floater Panes

Any pane can be declared as a floater — a free-floating window within the Glass Layer that
the user can drag, resize, minimize, and pin.

```yaml
- id: sim-runner-floater
  appType: sim-runner
  pin: float
  initialPosition: { x: 200, y: 100 }   # viewport space
  initialSize: { width: 480, height: 320 }
  resizable: true
  minimizable: true
  pinnable: true        # user can toggle between float and viewport-pin
  zIndex: auto          # auto = comes to front on focus
```

**Floater chrome:**
- Title bar with drag handle
- Minimize button (collapses to title bar only)
- Pin button (toggles `float` ↔ `viewport` pin)
- Resize handles on all edges and corners
- Close button (if EGG config allows)

When `pinnable: true`, the user pressing the pin button locks the floater to its current
viewport position — it stops moving when they scroll the canvas. Pressing again releases it
back to float behavior.

---

## 8. Meeting Room Reference Layout

The canonical meeting room scaffold layout — backlog, agenda, chat, timer — expressed as
EGG config:

```yaml
surface:
  type: infinite
  backdropApplet: drawio
  backdropConfig: { mode: freeform, toolbar: minimal }

scaffold:
  regions:
    - id: chat
      anchor: top-left
      width: 260px
      height: 100vh
      defaultApplet: sim-chat
      pin: scaffold
      sizeMode:
        desktop: fixed
        tablet-landscape: shrink
        tablet-portrait: drawer
        phone: sheet

    - id: backlog
      anchor: top-right
      width: 300px
      height: 55vh
      defaultApplet: kanban
      pin: scaffold
      sizeMode:
        desktop: fixed
        tablet-landscape: shrink
        tablet-portrait: tab
        phone: tab

    - id: agenda
      anchor: bottom-right
      width: 300px
      height: calc(45vh - 48px)
      defaultApplet: text
      defaultConfig: { format: markdown, label: Agenda }
      pin: scaffold
      sizeMode:
        desktop: fixed
        tablet-landscape: shrink
        tablet-portrait: tab
        phone: tab

    - id: timer
      anchor: top-center
      width: 200px
      height: 48px
      defaultApplet: timer
      pin: viewport
      dismissible: false

navJoystick:
  visible: auto
  position: bottom-left

minimap:
  visible: true
  position: bottom-right
```

---

## 9. Bus Events

### Emitted

| Event | When |
|-------|------|
| `SCAFFOLD_REGION_RESIZED` | User resizes a region |
| `SCAFFOLD_REGION_MODE_CHANGED` | Region sizeMode changes (breakpoint or user) |
| `FLOATER_MOVED` | User drags a floater |
| `FLOATER_PINNED` | User pins a floater to viewport |
| `FLOATER_MINIMIZED` | User minimizes a floater |

### Consumed

| Event | Effect |
|-------|--------|
| `VIEWPORT_RESIZE` | Triggers breakpoint re-evaluation |
| `VIEWPORT_ORIENTATION_CHANGED` | Triggers breakpoint re-evaluation |
| `KEYBOARD_VISIBLE` | Triggers keyboard-aware reflow (mobile) |

### Keyboard Visibility (Mobile)

When the virtual keyboard appears (detected via `visualViewport` API), scaffold regions with
`sizeMode: sheet` or `sizeMode: drawer` that contain text inputs are pushed above the
keyboard. This is a known mobile web challenge. The `KEYBOARD_VISIBLE` event carries the
keyboard height so regions can reflow correctly.

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-SCAFFOLD-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

Scaffold is the **layout orchestrator** — it consumes viewport/canvas events and emits layout state changes.

**Emitted events → consumed by:**

| Event | Consumers | Handler Location |
|-------|-----------|-----------------|
| `SCAFFOLD_REGION_RESIZED` | Pane adapters inside the region (resize handlers) | Individual pane adapter `onResize` |
| `SCAFFOLD_REGION_MODE_CHANGED` | Pane adapters (adapt to new sizeMode), AppletShell (away mode if hidden) | Pane adapters, `AppletShell.onAwayMode()` |
| `FLOATER_MOVED` / `FLOATER_PINNED` / `FLOATER_MINIMIZED` | canvas_surface Glass Layer (update floater position) | `services/canvas/canvasSurface.ts` Glass Layer |

**Consumed events:**

| Event | Source | Effect |
|-------|--------|--------|
| `VIEWPORT_RESIZE` | Browser/OS | Re-evaluate breakpoints, apply sizeMode transitions |
| `VIEWPORT_ORIENTATION_CHANGED` | Browser/OS | Re-evaluate breakpoints |
| `KEYBOARD_VISIBLE` | Browser (visualViewport API) | Keyboard-aware reflow for mobile sheet/drawer regions |
| `CANVAS_PAN` / `CANVAS_ZOOM` | canvas_surface | Scaffold regions anchored to viewport don't move; float-world regions do |
| `PRESENCE_STATE_CHANGED` | Presence service | If host goes mobile, scaffold may auto-collapse non-essential regions |

**Supersedes:** BL-011 (expandMode), BL-024 (auto-collapse), BL-025 (pin/unpin) — all moved to icebox. sizeMode and pin types in this spec are the canonical replacements.
