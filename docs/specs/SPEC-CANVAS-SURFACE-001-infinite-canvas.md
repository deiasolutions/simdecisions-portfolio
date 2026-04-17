# SPEC-CANVAS-SURFACE-001: Infinite Canvas Surface Primitive

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** SHELL
**T-Shirt Size:** XL
**Depends On:** relay_bus (BUILT), split_pane (SPECCED), SPEC-YIJS-001, SPEC-PRESENCE-001

---

## 1. Purpose

`canvas_surface` is a new platform primitive — an infinite, zoomable, pannable 2D coordinate
space that serves as the spatial substrate for EGGs that need more than a screen-bounded
layout. It sits *beneath* the pane tree as an optional backdrop layer.

When an EGG declares `surface: infinite`, `canvas_surface` activates and the HiveHostPanes
layout shifts from "fills the screen" to "manages panes over the surface."

The SC canvas primitive (ReactFlow + ELK, used for IR execution visualization) remains
unchanged. `canvas_surface` is a different thing: it is the *spatial world* that content
lives in, not an IR execution surface. The two coexist without conflict.

---

## 2. Coordinate System

The canvas_surface defines a 2D world space with no hard boundaries.

- **Origin:** (0, 0) at the center of the initial viewport
- **Units:** CSS pixels at zoom 1.0
- **Max tested extent:** ±100,000 units in each direction (effectively infinite for any
  meeting or whiteboard use case)
- **Zoom range:** 0.1x (very zoomed out, minimap-style) to 10x (detailed inspection)
- **Default zoom:** 1.0

### Coordinate Types

| Type | Description | Example |
|------|-------------|---------|
| **World space** | Position in the infinite canvas | (4500, -2200) |
| **Viewport space** | Position on the user's screen | (320, 180) |
| **Normalized** | 0-1 within current viewport | (0.5, 0.5) = center |

Every positioned element declares which coordinate type it uses. This is the central
architectural rule of canvas_surface. Getting it wrong causes elements to jump or drift.

---

## 3. Two Z-Layers

All content on canvas_surface exists in one of two layers:

### Layer 1: World Layer (Canvas-Pinned)

Content that lives "in the world." Moves when the user pans or zooms. Uses world space
coordinates.

Examples:
- Whiteboard drawings (draw.io backdrop)
- Sticky notes, annotations
- IR nodes placed on the canvas
- Region labels ("Team Alpha workspace here")
- Participant-owned work areas

### Layer 2: Glass Layer (Viewport-Pinned)

Content that lives "on the glass." Never moves regardless of pan/zoom. Uses viewport space
coordinates (or named anchor positions: `top-left`, `bottom-right`, etc.).

Examples:
- Minimap (always bottom-right)
- Timer (pinned by user choice)
- Chat (scaffold-anchored or pinned)
- Presence HUD (participant avatars, top-right)
- `nav_joystick` (mobile/tablet navigation control)
- Host sync indicator
- Session end / meeting controls

The Glass Layer always renders above the World Layer. Pointer events can be configured to
pass through Glass Layer elements to World Layer beneath (for transparent overlays).

---

## 4. Zoom and Pan

### Pan

- **Desktop:** click-drag on empty canvas, or two-finger trackpad drag
- **Tablet:** two-finger drag
- **Mobile:** one-finger drag (single-finger is pan; tap is select)
- **Keyboard:** arrow keys when canvas is focused (configurable step size)
- **nav_joystick:** directional control (see SPEC-SCAFFOLD-001)

### Zoom

- **Desktop:** scroll wheel, pinch trackpad, Cmd+/Cmd-
- **Tablet/Mobile:** pinch gesture
- **Minimap:** click a region to navigate there at current zoom; scroll on minimap to zoom

### Navigate to Region

`VIEWPORT_SYNC` event (from host or from own minimap click) animates the viewport to a
world-space coordinate. Animation duration is configurable (default: 600ms ease-in-out).

---

## 5. Minimap

The minimap is a Glass Layer element, viewport-pinned to bottom-right by default. It renders
a scaled-down view of the entire world layer content.

```yaml
minimap:
  visible: true
  position: bottom-right
  size: 200x150           # px, configurable
  showParticipants: true  # dots for each participant's current viewport center
  showRegions: true       # scaffold region outlines
  interactive: true       # click to navigate, scroll to zoom
  dismissible: true       # user can hide it
```

Minimap participant dots are colored by participant cursor color. Hovering a dot shows the
participant's display name.

---

## 6. Responsive Behavior

`canvas_surface` does not collapse or hide on small screens. The world exists regardless
of viewport size. What changes is the default zoom and pan starting position.

| Viewport | Default Zoom | Default Pan | Nav Control |
|----------|-------------|-------------|-------------|
| Desktop | 1.0 | Origin | Scroll + drag |
| Tablet landscape | 0.8 | Origin | Two-finger drag |
| Tablet portrait | 0.6 | Origin | Two-finger drag + nav_joystick |
| Phone | 0.4 | Origin | One-finger pan + nav_joystick |

The architect can override these defaults per EGG via the `surface` config block.

---

## 7. EGG Configuration

```yaml
surface:
  type: infinite              # activates canvas_surface
  backdropApplet: drawio      # optional: appType to render as world-layer backdrop
  backdropConfig:             # passed to the backdrop applet
    mode: freeform
    toolbar: minimal
  initialZoom: 1.0
  initialCenter: [0, 0]
  minZoom: 0.1
  maxZoom: 10.0
  showGrid: true
  gridSize: 20               # world-space units
  snapToGrid: false
  minimap:
    visible: true
    position: bottom-right
  sync:
    provider: yjs
    wsUrl: ws://localhost:1234
```

When `backdropApplet` is declared, that applet renders in the World Layer filling the
entire canvas extent. Panes declared in the `layout` block render in the Glass Layer or as
World Layer floaters depending on their `pin` config (see SPEC-SCAFFOLD-001).

---

## 8. canvas_surface vs SC Canvas Primitive

This is a critical distinction. They must never be confused.

| | `canvas_surface` | SC Canvas Primitive (ReactFlow) |
|---|---|---|
| **Purpose** | Spatial world for content to live in | IR execution visualization surface |
| **What renders on it** | Panes, draw.io, sticky notes, annotations | PHASE-IR nodes and edges |
| **Coordinate system** | Infinite 2D world space | ReactFlow internal coordinates |
| **Executes IR** | No | Yes |
| **Used for** | Meeting rooms, whiteboards, spatial workspaces | SimDecisions process designer |
| **Collaborative** | Yes (Y.js) | Single-user authoring |

They can coexist: a `canvas_surface` EGG can contain a pane that renders the SC Canvas
Primitive as a floater window. The SC Canvas Primitive runs IR inside its pane; it doesn't
know or care that it's floating over an infinite canvas.

---

## 9. Bus Events

### Emitted

| Event | Payload | When |
|-------|---------|------|
| `CANVAS_PAN` | `{ x, y, deltaX, deltaY }` | User pans |
| `CANVAS_ZOOM` | `{ zoom, centerX, centerY }` | Zoom level changes |
| `CANVAS_ELEMENT_PLACED` | `{ elementId, worldX, worldY, layer }` | Element dropped onto canvas |
| `CANVAS_REGION_ENTERED` | `{ regionId, participantId }` | Participant viewport enters a named region |

### Consumed

| Event | Effect |
|-------|--------|
| `VIEWPORT_SYNC` | Animate viewport to specified world coordinates |
| `CANVAS_ELEMENT_PLACED` | Register element in world-space index |

---

## 10. Build Notes for Mr. Code

`canvas_surface` is implemented as a React component that wraps a CSS `transform`-based
infinite canvas. Do not use a `<canvas>` element — the content (panes, draw.io, annotations)
is DOM-based and must remain DOM-based for accessibility and React integration.

The implementation pattern:
```
<div class="canvas-surface-root" style="overflow: hidden; width: 100vw; height: 100vh">
  <!-- World Layer -->
  <div class="world-layer" style="transform: translate(panX, panY) scale(zoom); transform-origin: 0 0">
    {backdropApplet}
    {worldLayerElements}   ← sticky notes, IR nodes, region labels
  </div>
  <!-- Glass Layer -->
  <div class="glass-layer" style="position: absolute; inset: 0; pointer-events: none">
    {minimapComponent}
    {presenceHUD}
    {navJoystick}
    {scaffoldPanes}        ← viewport-anchored scaffold regions
  </div>
</div>
```

The `transform` approach gives smooth pan/zoom via GPU compositing. It has been validated
at scale by tldraw, Figma, and Miro. No custom rendering engine needed.

Recommended: study tldraw's coordinate system implementation before writing the pan/zoom
math. Their `Camera` abstraction cleanly separates world↔viewport coordinate transforms.

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-CANVAS-SURFACE-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

canvas_surface is both a **producer and consumer** of relay_bus events.

**Emitted events → consumed by:**

| Event | Consumers | Handler Location |
|-------|-----------|-----------------|
| `CANVAS_PAN` | Minimap (update viewport rect), scaffold (region awareness) | Minimap component, `services/scaffold/scaffoldService.ts` |
| `CANVAS_ZOOM` | Minimap, scaffold (breakpoint re-eval if zoom changes effective viewport) | Minimap component |
| `CANVAS_ELEMENT_PLACED` | canvas_surface internal index, scaffold (region membership) | `services/canvas/canvasSurface.ts` |
| `CANVAS_REGION_ENTERED` | Scaffold (activate region), IR engine (if region triggers exist) | `services/scaffold/scaffoldService.ts` |

**Consumed events:**

| Event | Source | Effect |
|-------|--------|--------|
| `VIEWPORT_SYNC` | Presence service (host snap-to) | Animate viewport to target world coordinates |
| `CANVAS_ELEMENT_PLACED` | Own or remote (via Y.js sync) | Register element in world-space index |
| `SESSION_LEADERLESS` | Presence service | Switch canvas to read-only mode |
