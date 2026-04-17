# Pane Behavior Specification — ShiftCenter Stage

**Date:** 2026-03-11
**Author:** Q33NR (compiled from Q88N session feedback + code audit)
**Status:** SPEC — pending implementation
**Companion doc:** `docs/SHELL-FRAME-ARCHITECTURE-BRIEF.md` (scaffold/freeform terminology)

---

## 1. Frame Types (Terminology)

| Term | Node Types | Behavior |
|------|-----------|----------|
| **Scaffold** | `split`, `triple-split`, `tabbed` | Rigid grid, resizable dividers, no overlap |
| **Freeform** | `canvas` (not yet built) | Free-positioned children, draggable, overlappable |
| **Pane** | `app` (leaf node) | Renders a single applet. Can be empty or occupied. |

A pane is **empty** when `appType === 'empty'`. A pane is **occupied** when `appType !== 'empty'`.

---

## 2. Splitting

### 2.1 Binary Split

Divides a pane into two children with a draggable divider.

- **Left/Right** (`direction: 'vertical'`) — children side-by-side, vertical divider
- **Top/Bottom** (`direction: 'horizontal'`) — children stacked, horizontal divider
- The original pane becomes child[0]. Child[1] is a new empty pane.
- Default ratio: 0.5
- Divider is draggable. Double-click resets to 0.5.
- Minimum pane size: `MIN_PANE_PX = 150` pixels.

### 2.2 Triple Split

Divides a pane into three children with two independent draggable dividers.

- **Vertical x3** (`direction: 'vertical'`) — three columns
- **Horizontal x3** (`direction: 'horizontal'`) — three rows
- The original pane becomes child[0]. Children[1] and [2] are new empty panes.
- Default ratios: [0.33, 0.34, 0.33]
- Each divider is independently draggable.

### 2.3 Depth Limit

- Maximum nesting depth: `MAX_SPLIT_DEPTH = 8` (single constant in `shell/constants.ts`)
- `split` and `triple-split` each increment depth by 1
- `tabbed` does NOT increment depth (visual grouping, not spatial)
- Each branch (layout, float, pinned, spotlight) counts depth independently
- If depth limit reached, action is rejected and logged to ledger as `SPLIT_DEPTH_EXCEEDED`

### 2.4 Direction Convention

**IMPORTANT:** The direction refers to the divider orientation, not the child arrangement.

| Direction Value | Divider | Children | flexDirection |
|----------------|---------|----------|---------------|
| `'vertical'` | Vertical line | Side-by-side (left/right) | `row` |
| `'horizontal'` | Horizontal line | Stacked (top/bottom) | `column` |

This convention MUST be consistent across `SplitContainer`, `TripleSplitContainer`, and all menu dispatches.

---

## 3. Merging

### 3.1 Current State (what exists)

- Merge is only available when parent is a binary `split` node
- Merge replaces the split node with one of its two children (the "kept" child)
- The current menu automatically keeps the OTHER child (the sibling of the pane you're merging from)

### 3.2 Required Behavior (what should exist)

#### 3.2.1 Merge Should Always Be Available

The "Merge" option should appear in the hamburger menu for ANY pane that has a merge-eligible neighbor. This includes:

- Children of binary splits (existing)
- Children of triple-splits (NOT currently wired — needs `REMOVE_TRIPLE_SPLIT_CHILD`)
- Deeply nested panes (merge with sibling, collapsing the immediate parent)

#### 3.2.2 Merge Direction

When a user merges, they should choose a direction: **merge left, right, up, or down**. The merge target is the adjacent pane in that direction.

Rules:
- A merge is only valid between two panes that **share a complete border**. Partial borders (e.g., a small pane next to two stacked panes) are not mergeable.
- The menu should only show merge directions that are geometrically valid.

#### 3.2.3 Merge Into Empty vs Occupied

| Merging Pane | Neighbor Pane | Result |
|-------------|---------------|--------|
| Empty | Empty | Merge succeeds. Resulting pane is empty. |
| Empty | Occupied | Merge succeeds. Resulting pane keeps the occupied content. |
| Occupied | Empty | Merge succeeds. Resulting pane keeps the occupied content. |
| Occupied | Occupied | **Merge BLOCKED.** Flash both panes with a warning color (e.g., `--sd-orange` border pulse for 800ms). Show a toast/notification: "Cannot merge two occupied panes. Close one first." |

#### 3.2.4 Triple-Split Merge

Merging a child of a triple-split should:
1. Remove that child from the triple-split
2. Collapse the triple-split to a binary split with the remaining two children
3. This uses the existing `REMOVE_TRIPLE_SPLIT_CHILD` reducer action (fully implemented, currently unwired)

---

## 4. Spawning Applets

### 4.1 Spawn Into Empty Pane

Clicking an applet from the Applets submenu when the current pane is **empty** should:
1. Replace `appType: 'empty'` with the selected app type
2. Set `loadState: 'HOT'` (render immediately)
3. The pane now shows the applet

### 4.2 Spawn Into Occupied Pane

Clicking an applet from the Applets submenu when the current pane is **occupied** should:
1. **NOT silently overwrite** the existing app
2. Show a notification: "This pane already has content. Split it first to add another applet."
3. The action is rejected — existing content is preserved

### 4.3 Current Bug

`SPAWN_APP` currently overwrites any existing app without warning. `loadState` was set to `'COLD'`, causing the new app to render as a blank EmptyPane. The COLD issue is fixed (now HOT), but the overwrite protection is still missing.

---

## 5. Flip

### 5.1 Binary Split Flip

Toggles the split direction between `vertical` and `horizontal`. Children swap from side-by-side to stacked or vice versa.

- Available when parent is `type: 'split'`
- Uses `FLIP_SPLIT` action

### 5.2 Triple-Split Flip

Toggles the triple-split direction. Three columns become three rows or vice versa.

- Available when parent is `type: 'triple-split'`
- Uses `FLIP_TRIPLE_SPLIT` action
- **Currently unwired** — the menu dispatches `FLIP_SPLIT` (which rejects triple-splits) instead of detecting parent type and dispatching the correct action

### 5.3 Required Fix

The Flip menu item should detect the parent type and dispatch the appropriate action:
- Parent is `split` → `FLIP_SPLIT`
- Parent is `triple-split` → `FLIP_TRIPLE_SPLIT`

---

## 6. Swap

### 6.1 Behavior

1. User clicks "Swap With..." on pane A
2. All other panes show a swap target overlay
3. User clicks pane B
4. Contents of A and B are exchanged (appType, config, label, etc.)
5. Swap is blocked if either pane is locked or has `chrome: false`

### 6.2 Current State

Fully implemented and wired. Works correctly.

---

## 7. Tabs

### 7.1 Add Tab

Creates a tabbed container wrapping the current pane, with a new empty tab added.

- If pane is already inside a tabbed container, adds a new tab to that container
- If pane is standalone, wraps it in a new tabbed container

### 7.2 Tab Operations

- **Close Tab** — removes a tab. If last tab, replaces with empty pane.
- **Reorder Tabs** — drag tabs to reorder within the tab bar.
- **Switch Tab** — click to activate.
- Tabs do NOT count toward split depth.

---

## 8. Resize

### 8.1 Binary Split Divider

- Drag to resize. Minimum pane size enforced.
- Double-click to reset to 50/50.
- Snap-to-center feedback when near 50%.
- Slides-over detection when a collapsed pane is dragged further outward.

### 8.2 Triple-Split Dividers

- Two independent dividers, each controlling the boundary between adjacent children.
- Same minimum pane size enforcement.
- Slides-over detection on middle pane when at minimum size.

### 8.3 Current Bug

Triple-split resize may not be working correctly. The divider drag handlers use `isVert` (recently renamed from `isHorizontal`). Code audit confirms the rename is complete and correct, but user reports the triple-split acts as a non-resizable unit. Needs investigation — possible that the divider hit area is too small or the mouse events aren't propagating.

---

## 9. Maximize / Restore

- **Maximize** — hides all other panes, the selected pane fills the entire shell body.
- **Restore** — returns to previous layout. Triggered by Escape key or restore button.
- Only one pane can be maximized at a time.

---

## 10. Close

- Closing an occupied pane replaces it with an empty pane (type: 'empty').
- The pane slot remains in the tree — only its content is removed.
- Closing is blocked for locked panes and chrome:false panes.

---

## 11. Empty Pane UX

### 11.1 FAB (Floating Action Button)

Empty panes show a centered `+` button (FAB). Clicking it opens a menu with:
- **Split** submenu — Left/Right, Top/Bottom, Vertical x3, Horizontal x3, (Flip, Merge when available)
- **Tabs** submenu — Add Tab
- **Applets** submenu — lists all registered app types

### 11.2 Right-Click Fallback

Right-click anywhere on an empty pane opens the same menu at the cursor position.

### 11.3 No "Right-Click To..." Text

Empty panes show only the FAB button. No instructional text. The `+` is self-explanatory.

---

## 12. Occupied Pane Chrome

### 12.1 Title Bar (30px)

Left to right:
1. **Drag handle** (⠿) — drag to move pane via drop zones
2. **Hamburger menu** (☰) — opens pane menu (see 12.2)
3. **Lock icon** (if locked)
4. **App icon** (from registry)
5. **Label** — truncated with ellipsis. Notification dot if applicable.
6. **Audio mute toggle**
7. **Bus mute cycle**
8. **Maximize** (when not maximized) or **Restore** (when maximized)
9. **Close** (✕) — only when not maximized

### 12.2 Hamburger Menu Structure

```
Split           ▸  Left / Right
                   Top / Bottom
                   ─────────────
                   Vertical ×3
                   Horizontal ×3
                   ─────────────
                   Flip Split        (when parent is split/triple-split)
                   Merge Pane        (when merge-eligible neighbor exists)

Tabs            ▸  Add Tab

Applets         ▸  terminal
                   text-pane
                   text-editor
                   tree-browser
                   settings
                   (dynamic from registry)

─────────────────
Swap With...
Maximize
```

### 12.3 Visual States

| State | Border | Title Bar BG | Font Weight |
|-------|--------|-------------|-------------|
| Unfocused | `--sd-border-subtle` | `--sd-glass-bg` | 400 |
| Focused | `--sd-border-focus` | `--sd-surface` | 500 |
| Governance alert | `--sd-orange` | `--sd-glass-bg` | 400 |
| Re-engagement | Animated glow (500ms) | — | — |

---

## 13. Notifications and Feedback

### 13.1 Merge Blocked (two occupied panes)

When a user attempts to merge two occupied panes:
1. Both panes flash with `--sd-orange` border pulse animation (800ms)
2. A toast notification appears: "Cannot merge two occupied panes. Close one first."

### 13.2 Spawn Blocked (occupied pane)

When a user attempts to spawn an applet into an occupied pane:
1. A toast notification appears: "This pane already has content. Split it first."

### 13.3 Split Depth Exceeded

When a user attempts to split beyond `MAX_SPLIT_DEPTH`:
1. The split action is silently rejected
2. A ledger event `SPLIT_DEPTH_EXCEEDED` is logged

---

## 14. Known Bugs (as of 2026-03-11)

| # | Bug | Root Cause | Fix Status |
|---|-----|-----------|------------|
| 1 | Triple-split not resizable | Under investigation — divider hit area or event propagation | OPEN |
| 2 | SPAWN_APP overwrites occupied panes silently | No occupancy check in `lifecycle.ts:SPAWN_APP` | OPEN |
| 3 | Merge unavailable for triple-split children | `canMerge` only checks `parent?.type === 'split'` | OPEN |
| 4 | Flip dispatches wrong action for triple-splits | Always dispatches `FLIP_SPLIT`, never `FLIP_TRIPLE_SPLIT` | OPEN |
| 5 | `REMOVE_TRIPLE_SPLIT_CHILD` unwired | Reducer handler exists, no UI dispatch | OPEN |
| 6 | Merge doesn't check both-occupied conflict | No guard against merging two occupied panes | OPEN |
| 7 | Merge has no directional choice | Always merges with sibling, no L/R/U/D selection | OPEN |

---

## 15. Reducer Actions Reference

### Layout Actions

| Action | Wired? | Description |
|--------|--------|-------------|
| `SPLIT` | Yes | Binary split a pane |
| `MERGE` | Yes (binary only) | Collapse a binary split, keep one child |
| `TRIPLE_SPLIT` | Yes | Triple-split a pane |
| `REMOVE_TRIPLE_SPLIT_CHILD` | **No** | Remove one child from triple-split, collapse to binary |
| `FLIP_SPLIT` | Yes | Toggle binary split direction |
| `FLIP_TRIPLE_SPLIT` | **No** | Toggle triple-split direction |
| `UPDATE_RATIO` | Yes | Resize binary split divider |
| `UPDATE_TRIPLE_SPLIT_RATIOS` | Yes | Resize triple-split dividers |
| `MOVE_APP` | Yes | Drag-drop move via drop zones |
| `SET_SWAP_PENDING` | Yes | Initiate swap mode |
| `SWAP_CONTENTS` | Yes | Execute swap between two panes |

### Lifecycle Actions

| Action | Wired? | Description |
|--------|--------|-------------|
| `SPAWN_APP` | Yes (via Applets submenu) | Load an app into a pane |
| `CLOSE_APP` | Yes | Close app, revert to empty pane |
| `OPEN_PANE` | **No** | Open content in a pane |
| `MINIMIZE_PANE` | **No** | Minimize a pane |
| `SET_LOAD_STATE` | Programmatic | Set COLD/WARM/HOT state |
| `WARM_KERNEL` | **No** | Pre-warm a kernel service |
| `SAVE_WORKSPACE` | **No** | Persist workspace to storage |
| `LOAD_WORKSPACE` | **No** | Restore workspace from storage |

### Tab Actions

| Action | Wired? | Description |
|--------|--------|-------------|
| `ADD_TAB` | Yes | Add a new tab |
| `CLOSE_TAB` | Yes | Remove a tab |
| `REORDER_TAB` | Yes | Drag to reorder |
| `SET_ACTIVE_TAB` | Yes | Switch active tab |

### Branch Actions

| Action | Wired? | Description |
|--------|--------|-------------|
| `REPARENT_TO_BRANCH` | **No** | Move between layout/float/pinned/spotlight |
| `SET_Z_ORDER` | **No** | Reorder float panes |
| `FOCUS_FLOAT_PANE` | Yes | Bring float pane to top |
| `ADD_SPOTLIGHT` | **No** | Show spotlight overlay |
| `REMOVE_SPOTLIGHT` | Yes | Dismiss spotlight |
| `TRIGGER_SLIDES_OVER` | Yes | Float a collapsed pane |
| `RETRACT_SLIDES_OVER` | Yes | Dock a slides-over pane |

### Focus / Chrome Actions

| Action | Wired? | Description |
|--------|--------|-------------|
| `SET_FOCUS` | Yes | Set focused pane |
| `MAXIMIZE` | Yes | Maximize a pane |
| `RESTORE` | Yes | Restore from maximized |
| `SET_AUDIO_MUTE` | Yes | Toggle audio mute |
| `SET_BUS_MUTE` | Yes | Cycle bus mute level |
| `LOG_EVENT` | Yes | Log to event ledger |

### Undo

| Action | Wired? | Description |
|--------|--------|-------------|
| `LAYOUT_UNDO` | **No** | Undo last structural change |
| `LAYOUT_REDO` | **No** | Redo last structural change |

---

## 16. Implementation Priority

| Priority | Item | Task |
|----------|------|------|
| P0 | Fix triple-split resize | Investigate divider hit area |
| P0 | Wire `REMOVE_TRIPLE_SPLIT_CHILD` to menu | Merge for triple-split children |
| P0 | Fix Flip for triple-splits | Detect parent type, dispatch correct action |
| P1 | Guard SPAWN_APP against occupied panes | Add occupancy check + notification |
| P1 | Guard MERGE against two-occupied conflict | Flash + notification |
| P2 | Directional merge (L/R/U/D) | Geometry check for shared complete borders |
| P2 | Wire undo/redo (Ctrl+Z / Ctrl+Shift+Z) | TASK-024 |
| P2 | FAB polish | Already built, needs visual refinement |
| P3 | Wire `REPARENT_TO_BRANCH` ("Pop Out as Float") | Post-freeform canvas |
| P3 | Freeform canvas node type | TASK-020/021/022 |

---

*This spec reflects the current state of the codebase as of 2026-03-11 and incorporates all user feedback from the Q88N live session. Implementation tasks should reference this document.*
