# Shell Frame Architecture Brief

**Date:** 2026-03-11
**Author:** Q33NR (drafted with Q88N)
**Status:** APPROVED NAMING — tasks numbered, pending dispatch
**Audience:** Next coding agent ("Mr Ai"), Q88N for approval

---

## 1. Core Insight: Frames Are Pane Specs, Not Modes

The shell should not have a "mode" toggle between structured layout and floating desktop. Instead, **scaffold and freeform are two different frame types** — composable pane specs that can appear anywhere in the tree.

| Frame Type | Name | Node Types | Children Layout | Use Case |
|------------|------|-----------|----------------|----------|
| **Scaffold** | Rigid structured layouts | `split`, `triple-split`, `tabbed` | Grid-locked, resizable dividers | Structured IDE layouts, composite EGGs |
| **Freeform** | Free-floating canvas | `canvas` (NEW) | Freely positioned, draggable, overlapping | Desktop metaphor, creative workspaces |

### The Atomization Principle

- A **full scaffold desktop** = the top-level layout node is a split tree (what we have today)
- A **full freeform desktop** = the top-level layout node is a single `canvas` frame
- A **hybrid** = a scaffold split where one pane contains a freeform `canvas`, or a freeform `canvas` where one child contains a scaffold split
- **Nesting is unlimited** (subject to `MAX_SPLIT_DEPTH = 8`): freeform inside scaffold inside freeform inside scaffold

This means the "freeform desktop" is not a special mode. It's just an EGG whose top-level layout node is `type: 'canvas'`.

```yaml
# freeform-desktop.egg.md layout block:
{ "type": "canvas", "nodeId": "desktop", "children": [...] }

# scaffold-desktop.egg.md layout block:
{ "type": "split", "direction": "vertical", ... }

# hybrid.egg.md layout block — scaffold with freeform zone:
{ "type": "split", "direction": "vertical", "children": [
    { "type": "pane", ... },
    { "type": "canvas", "nodeId": "freeform-area", "children": [...] }
]}
```

---

## 2. New Node Type: `canvas` (Freeform Frame)

### Schema

```typescript
interface CanvasNode {
  type: 'canvas';
  id: string;
  children: CanvasChild[];
  background?: string;       // CSS variable for canvas bg
  gridSnap?: number;         // optional snap-to-grid in px
  allowOverlap?: boolean;    // default true
}

interface CanvasChild {
  node: ShellTreeNode;       // any node type: app, split, tabbed, even nested canvas
  position: { x: number; y: number };
  size: { w: number; h: number };
  zIndex?: number;
  minimized?: boolean;
}
```

### Rendering

A freeform `CanvasNode` renders as a `position: relative` container. Each child is `position: absolute` with draggable + resizable chrome (title bar handles, resize corners). Children can overlap. Z-order is array position (last = top) or explicit `zIndex`.

### Depth Counting

Freeform canvas children increment depth by 1 (same as scaffold splits), so `getNodeDepthInTree` treats canvas like a split for depth purposes. This keeps composite EGG nesting under control.

---

## 3. Unwired Reducer Actions

14 actions exist in the reducer with **zero UI triggers**. These need to be wired to menus, keyboard shortcuts, or the command palette.

### Layout Actions (need menu/shortcut wiring)

| Action | What It Does | Proposed UI |
|--------|-------------|-------------|
| `REMOVE_TRIPLE_SPLIT_CHILD` | Remove one child from triple-split, collapse to binary | Hamburger menu on triple-split child panes |
| `REPARENT_TO_BRANCH` | Move node between layout/float/pinned/spotlight | Hamburger menu: "Pop Out as Float" / "Dock to Layout" |
| `SET_Z_ORDER` | Reorder float panes | Float pane title bar drag / context menu |
| `ADD_SPOTLIGHT` | Show node as spotlight overlay | Command palette / keyboard shortcut |
| `LAYOUT_UNDO` | Undo last structural change | `Ctrl+Z` (when no text input focused) |
| `LAYOUT_REDO` | Redo last structural change | `Ctrl+Shift+Z` |

### Lifecycle Actions (need toolbar/command palette)

| Action | What It Does | Proposed UI |
|--------|-------------|-------------|
| `SPAWN_APP` | Create new app instance | App launcher / command palette |
| `OPEN_PANE` | Open content in a pane | Programmatic + command palette |
| `MINIMIZE_PANE` | Minimize a pane | Title bar minimize button |
| `WARM_KERNEL` | Pre-warm a kernel service | Automatic / settings |
| `SET_LOAD_STATE` | Set pane load state (COLD/WARM/HOT) | Programmatic only (not user-facing) |
| `SAVE_WORKSPACE` | Save workspace to storage | Menu bar: File > Save Workspace |
| `LOAD_WORKSPACE` | Load workspace from storage | Menu bar: File > Load Workspace |
| `REGISTER_PANE_SETTINGS` | Register pane-specific settings | Programmatic only (app init) |

---

## 4. EmptyPane: FAB vs Right-Click

The EmptyPane currently uses a right-click context menu for scaffold actions (split/merge/tab). The intent is to switch to a FAB (Floating Action Button) — a visible `+` button that doesn't require right-click discovery.

### Proposed FAB Behavior

- Centered `+` button in empty panes (replaces "Right-click to add content" text)
- Click opens the same menu items (split, triple-split, add tab, merge, app launcher)
- Right-click still works as an alternative trigger
- FAB disappears when pane gets content (occupied panes use hamburger menu instead)

---

## 5. Missing Smoke Tests

There are **zero smoke tests** validating that reducer actions are reachable from UI. This is why triple-split went unwired for the entire build cycle.

### Proposed Smoke Test Suite

A smoke test should verify for every user-facing action type:

```typescript
// shell/__tests__/smoke.wiring.test.ts
// For each action type in ShellAction:
//   1. Is it dispatched from at least one component? (grep-based or render-based)
//   2. If it's infrastructure-only (SET_LOAD_STATE, WARM_KERNEL), is it explicitly marked as such?
//   3. Does the menu item / button / shortcut exist and not throw on click?
```

Minimum coverage:
- Every hamburger menu item dispatches the correct action
- Every EmptyPane menu item dispatches the correct action
- Every keyboard shortcut dispatches the correct action
- Every unwired action is explicitly tagged `@infrastructure` in the type definition

---

## 6. Depth Limits and Tree Traversal

### Current Configuration

| Constant | Value | Location | Effect |
|----------|-------|----------|--------|
| `MAX_SPLIT_DEPTH` | 8 | `shell/constants.ts` | Max nesting of scaffold/freeform nodes |
| `MIN_PANE_PX` | 150 | `shell/constants.ts` | Minimum pane size — practical pixel limit |

### Depth Counting Rules

| Node Type | Frame Type | Depth Increment | Rationale |
|-----------|-----------|----------------|-----------|
| `split` | Scaffold | +1 | Spatial subdivision |
| `triple-split` | Scaffold | +1 | Spatial subdivision |
| `canvas` | Freeform | +1 | Spatial subdivision (children are independent mini-layouts) |
| `tabbed` | Neither | +0 | Visual grouping, not spatial — tabs share the same space |

### Branch Independence

Each branch starts depth counting independently:
- `root.layout` — starts at 0
- `root.float[i]` — each float pane starts at 0
- `root.pinned[i]` — each pinned pane starts at 0
- `root.spotlight` — starts at 0

A composite EGG loaded into a scaffold pane at depth 5 still has 3 more levels of nesting available (5 + 3 = 8). Float panes get the full 8.

### Theoretical Maximums

| Depth | Binary Split Leaves | Triple Split Leaves |
|-------|-------------------|-------------------|
| 4 | 16 | 81 |
| 6 | 64 | 729 |
| 8 | 256 | 6,561 |

Practical limit is always screen real estate (`MIN_PANE_PX = 150`).

---

## 7. Terminology Reference

| Term | Meaning |
|------|---------|
| **Scaffold** | Rigid, grid-locked frame. Node types: `split`, `triple-split`, `tabbed`. Children arranged by dividers. |
| **Freeform** | Free-floating canvas frame. Node type: `canvas`. Children positioned absolutely, draggable, resizable, overlappable. |
| **Hybrid layout** | Any tree mixing scaffold and freeform nodes. E.g., a scaffold split with one child being a freeform canvas. |
| **Frame** | Generic term for any layout container node (scaffold or freeform). |
| **Pane** | A leaf node (`type: 'app'`) that renders an app primitive. Lives inside any frame type. |

---

## 8. Task Breakdown — MVP

### Freeform Node Type (MVP)

| Task ID | Title | Scope | Depends On |
|---------|-------|-------|-----------|
| TASK-020 | **Freeform canvas node type** — add `canvas` to ShellTreeNode union, reducer actions (CREATE_CANVAS, ADD_CANVAS_CHILD, MOVE_CANVAS_CHILD, RESIZE_CANVAS_CHILD, REMOVE_CANVAS_CHILD), depth counting in `getNodeDepthInTree`, utils | Shell core (types, reducer, utils) | — |
| TASK-021 | **FreeformContainer renderer** — `position: relative` parent, absolutely-positioned draggable/resizable children with PaneChrome, z-order management, click-to-focus raises child | Shell components | TASK-020 |
| TASK-022 | **eggToShell freeform support** — parse `type: 'canvas'` in EGG layout blocks, inflate to CanvasNode, update `eggLayoutToShellTree` | EGG system | TASK-020 |

### Shell Polish

| Task ID | Title | Scope | Depends On |
|---------|-------|-------|-----------|
| TASK-023 | **FAB for EmptyPane** — replace right-click-only UX with visible `+` button, keep right-click as fallback, wire all scaffold + freeform actions | Shell components | — |
| TASK-024 | **Undo/Redo keyboard shortcuts** — wire `Ctrl+Z` → LAYOUT_UNDO, `Ctrl+Shift+Z` → LAYOUT_REDO, only when no text input focused | Shell components | — |
| TASK-025 | **Smoke test suite** — verify every ShellAction type has at least one UI dispatch path or is explicitly tagged `@infrastructure` | Tests | — |

### Deferred (post-MVP, not yet numbered)

| Title | Scope | Notes |
|-------|-------|-------|
| Wire unwired layout actions (REMOVE_TRIPLE_SPLIT_CHILD, REPARENT_TO_BRANCH, SET_Z_ORDER, ADD_SPOTLIGHT) | Shell components | Depends on TASK-020 for freeform context |
| Wire lifecycle actions (SPAWN_APP, OPEN_PANE, SAVE/LOAD_WORKSPACE) | Shell components | Needs command palette / menu bar first |
| Scaffold ↔ Freeform conversion action | Shell reducer + UI | Convert split to canvas or vice versa |

---

## 9. Open Questions

1. **Freeform child chrome** — should freeform canvas children have a mini title bar (like OS windows) or reuse the same PaneChrome as scaffold panes?
2. **Scaffold ↔ Freeform conversion** — should there be a menu action to convert a scaffold node into a freeform canvas (free all children) or vice versa (auto-arrange into grid)?
3. **Freeform in EGG spec** — `type: 'canvas'` is just another layout node type in the existing layout block format. No new EGG block type needed.
4. **Z-order persistence** — should freeform child z-order survive workspace save/load? (Likely yes — it's part of the tree state.)
5. **Grid snap** — should freeform canvas support optional grid snapping for alignment?

---

*Naming locked by Q88N: **scaffold** (rigid) and **freeform** (canvas). All tasks require Q88N approval before dispatch.*
