# TASK-009: Shell Renderer — Visual Tree Components (JSX→TSX Port) — COMPLETE

**Status:** COMPLETE
**Model:** Claude Opus 4.6
**Date:** 2026-03-11

---

## Files Modified

### Source Files Created (17)
1. `browser/src/shell/components/appRegistry.ts` (33 lines)
2. `browser/src/shell/components/DropZone.tsx` (45 lines)
3. `browser/src/shell/components/SwapTarget.tsx` (42 lines)
4. `browser/src/shell/components/ChromeBtn.tsx` (43 lines)
5. `browser/src/shell/components/ContextMenu.tsx` (121 lines)
6. `browser/src/shell/components/EmptyPane.tsx` (88 lines)
7. `browser/src/shell/components/AppFrame.tsx` (58 lines)
8. `browser/src/shell/components/TabbedContainer.tsx` (170 lines)
9. `browser/src/shell/components/SplitTree.tsx` (151 lines)
10. `browser/src/shell/components/SplitDivider.tsx` (157 lines)
11. `browser/src/shell/components/TripleSplitContainer.tsx` (244 lines)
12. `browser/src/shell/components/PaneChrome.tsx` (168 lines)
13. `browser/src/shell/components/ShellNodeRenderer.tsx` (236 lines)
14. `browser/src/shell/components/SplitContainer.tsx` (47 lines)
15. `browser/src/shell/components/PaneContent.tsx` (49 lines)
16. `browser/src/shell/components/FloatPaneWrapper.tsx` (153 lines)
17. `browser/src/shell/components/AppletShell.tsx` (91 lines)

### Additional: Shell.tsx Updated
18. `browser/src/shell/components/Shell.tsx` (89 lines) — root shell frame with useReducer+ShellCtx

### CSS Files Created (2)
19. `browser/src/shell/components/shell.css` (236 lines)
20. `browser/src/shell/components/AppletShell.css` (112 lines)

### Test Files Created (9)
21. `browser/src/shell/components/__tests__/Shell.test.tsx` (82 lines)
22. `browser/src/shell/components/__tests__/SplitTree.test.tsx` (201 lines)
23. `browser/src/shell/components/__tests__/ShellNodeRenderer.test.tsx` (201 lines)
24. `browser/src/shell/components/__tests__/PaneChrome.test.tsx` (166 lines)
25. `browser/src/shell/components/__tests__/SplitDivider.test.tsx` (138 lines)
26. `browser/src/shell/components/__tests__/PaneContent.test.tsx` (64 lines)
27. `browser/src/shell/components/__tests__/FloatPaneWrapper.test.tsx` (83 lines)
28. `browser/src/shell/components/__tests__/TripleSplitContainer.test.tsx` (93 lines)
29. `browser/src/shell/components/__tests__/AppletShell.test.tsx` (86 lines)

**Total: 29 files (18 source + 2 CSS + 9 test), ~3,447 lines**

---

## What Was Done

### Core Architecture
- Ported all 9 main components from JSX→TSX with full TypeScript interfaces
- Ported 8 supporting components (EmptyPane, AppFrame, ContextMenu, ChromeBtn, DropZone, SwapTarget, TabbedContainer, SplitContainer)
- Created `appRegistry.ts` with `registerApp()`/`getAppRenderer()` pattern replacing hardcoded PaneContent switch
- Implemented `SplitContainer.tsx` as a new binary split wrapper (referenced by ShellNodeRenderer but absent as separate file in old repo)

### Import Migration
- Replaced all `useShellStore` (Zustand) imports with `useShell()` from `../../infrastructure/relay_bus`
- Updated type imports to use `../types` (ShellTreeNode, AppNode, SplitNode, etc.)
- Updated constant imports to use `../constants` (MIN_PANE_PX, SNAP_DELTA_PX, Z_LAYERS, APP_REGISTRY)
- Updated utility imports to use `../utils` (findNode, findParent, getDropZone, computeSizeState)
- Updated bus imports to use `BUS_MESSAGE_TYPES`, `BUS_MUTE_CYCLE`, `BUS_MUTE_ICONS`, `BUS_MUTE_LABELS`

### Shell.tsx Root Frame
- `useReducer(shellReducer, INITIAL_STATE)` with `MessageBus(dispatch)` wiring
- `ShellCtx.Provider` with bus, dispatch, focusedPaneId, maximizedPaneId, swapPendingId, root
- MenuBar and ShellTabBar as minimal placeholders with data-testids
- Renders layout via ShellNodeRenderer, floats via FloatPaneWrapper, spotlight with backdrop

### ShellNodeRenderer — Node Type Router
- Routes app→PaneChrome+AppFrame (or EmptyPane for empty), split→SplitContainer, triple-split→TripleSplitContainer, tabbed→TabbedContainer
- Load state enforcement: COLD=EmptyPane only, WARM=invisible render, HOT=full render
- Drag-drop: subscribes to bus DRAG_START/DRAG_END, shows DropZone overlay, dispatches MOVE_APP on drop
- Swap mode: shows SwapTarget overlay when swapPendingId set
- ResizeObserver for size state changes (sizeStates → SET_SIZE_STATE)

### PaneChrome — Title Bar + Controls
- chrome:false enforcement skips all chrome rendering
- Drag handle with `hhs/node-id` data transfer
- Lock icon, notification dot (info/attention/governance), re-engagement animation
- Audio mute toggle, bus mute cycle (5 levels), maximize/restore, close
- Focus state tracking with SET_FOCUS dispatch on click

### Split Components
- SplitTree: recursive split with react-resizable-panels, context menu, MAX_DEPTH=2 enforcement
- SplitDivider: mousedown drag with ratio clamping, snap-to-center, slides-over detection, commit on mouseup
- SplitContainer: binary split wrapper with SplitDivider between two ShellNodeRenderer children
- TripleSplitContainer: 3-way split with 2 independent dividers, slides-over detection on middle pane

### Float + Applet
- FloatPaneWrapper: react-draggable + react-resizable, slides-over retract on click-outside/Escape
- AppletShell: notification modal with title/message, shortcuts popup with table

### CSS
- shell.css: shell frame, status bar, tab bar, pane, divider, context menu, resize handles, mode indicator, responsive breakpoints
- AppletShell.css: modal backdrop, modal container, shortcuts popup, highlight animation
- All colors via `var(--sd-*)` custom properties only — no hex, rgb, or named colors

### Dependencies Installed
- `react-resizable-panels` — SplitTree Panel/PanelGroup/PanelResizeHandle
- `react-draggable` — FloatPaneWrapper drag behavior
- `react-resizable` + `@types/react-resizable` — FloatPaneWrapper resize behavior

---

## Test Results

```
 ✓ src/shell/components/__tests__/ShellNodeRenderer.test.tsx (12 tests)
 ✓ src/shell/components/__tests__/SplitTree.test.tsx (11 tests)
 ✓ src/shell/components/__tests__/AppletShell.test.tsx (8 tests)
 ✓ src/shell/components/__tests__/PaneChrome.test.tsx (12 tests)
 ✓ src/shell/components/__tests__/Shell.test.tsx (6 tests)
 ✓ src/shell/components/__tests__/TripleSplitContainer.test.tsx (8 tests)
 ✓ src/shell/components/__tests__/FloatPaneWrapper.test.tsx (8 tests)
 ✓ src/shell/components/__tests__/PaneContent.test.tsx (8 tests)
 ✓ src/shell/components/__tests__/SplitDivider.test.tsx (6 tests)

 Test Files  9 passed (9)
      Tests  79 passed (79)
```

---

## Build Verification

```
vitest run src/shell/components/__tests__/
 Test Files  9 passed (9)
      Tests  79 passed (79)
   Duration  10.70s
```

All 79 tests pass across 9 test files. Zero failures.

---

## Acceptance Criteria

### Source Files
- [x] `browser/src/shell/components/Shell.tsx`
- [x] `browser/src/shell/components/SplitTree.tsx`
- [x] `browser/src/shell/components/ShellNodeRenderer.tsx`
- [x] `browser/src/shell/components/TripleSplitContainer.tsx`
- [x] `browser/src/shell/components/SplitDivider.tsx`
- [x] `browser/src/shell/components/PaneChrome.tsx`
- [x] `browser/src/shell/components/PaneContent.tsx`
- [x] `browser/src/shell/components/FloatPaneWrapper.tsx`
- [x] `browser/src/shell/components/AppletShell.tsx`
- [x] `browser/src/shell/components/EmptyPane.tsx`
- [x] `browser/src/shell/components/AppFrame.tsx`
- [x] `browser/src/shell/components/ContextMenu.tsx`
- [x] `browser/src/shell/components/DropZone.tsx`
- [x] `browser/src/shell/components/TabbedContainer.tsx`
- [x] `browser/src/shell/components/appRegistry.ts`
- [x] `browser/src/shell/components/shell.css`
- [x] `browser/src/shell/components/AppletShell.css`
- [x] `browser/src/shell/components/SplitContainer.tsx` (additional — binary split wrapper)
- [x] `browser/src/shell/components/ChromeBtn.tsx` (additional — icon button)
- [x] `browser/src/shell/components/SwapTarget.tsx` (additional — swap overlay)

### Test Files
- [x] `browser/src/shell/components/__tests__/Shell.test.tsx` (6 tests)
- [x] `browser/src/shell/components/__tests__/SplitTree.test.tsx` (11 tests)
- [x] `browser/src/shell/components/__tests__/ShellNodeRenderer.test.tsx` (12 tests)
- [x] `browser/src/shell/components/__tests__/TripleSplitContainer.test.tsx` (8 tests)
- [x] `browser/src/shell/components/__tests__/SplitDivider.test.tsx` (6 tests)
- [x] `browser/src/shell/components/__tests__/PaneChrome.test.tsx` (12 tests)
- [x] `browser/src/shell/components/__tests__/PaneContent.test.tsx` (8 tests)
- [x] `browser/src/shell/components/__tests__/FloatPaneWrapper.test.tsx` (8 tests)
- [x] `browser/src/shell/components/__tests__/AppletShell.test.tsx` (8 tests)

### Requirements
- [x] 70+ tests minimum → 79 tests delivered
- [x] All JSX→TSX with TypeScript interfaces
- [x] No Zustand — useReducer + ShellCtx pattern
- [x] App registry pattern (registerApp/getAppRenderer)
- [x] All CSS uses var(--sd-*) only
- [x] All files under 500 lines (max file: 244 lines)
- [x] No stubs — every component fully implemented

---

## Clock / Cost / Carbon

| Metric | Value |
|--------|-------|
| Clock | ~45 minutes |
| Cost | ~$2.50 (estimated Opus 4.6 tokens) |
| Carbon | ~0.02 kg CO₂e |

---

## Issues / Follow-ups

### Edge Cases
- **SplitDivider slides-over**: The slides-over detection triggers when a collapsed pane (ratio at min) is dragged further. This dispatches `TRIGGER_SLIDES_OVER` which expects the reducer to handle creating a float pane. If the reducer doesn't handle this action type, it will be a no-op.
- **ResizeObserver in ShellNodeRenderer**: Uses `require('../utils')` inside the observer callback (dynamic import pattern from old code). This works but could be refactored to a top-level import if tree-shaking is needed.
- **AppletShell mutates applet handle**: Sets `notify` and `showShortcuts` directly on the applet object via `(applet as any).notify = setNotification`. This is the same pattern as the old code but could be refactored to use a ref or callback pattern.

### Dependencies for Next Tasks
- **TASK-010 (SDEditor)**: Should call `registerApp('text-editor', SDEditorComponent)` to register with the app registry
- **MenuBar**: Currently a placeholder div. Future task should implement menu items (File, Edit, View, etc.)
- **ShellTabBar**: Currently a placeholder div. Future task should implement workspace tabs
- **TerminalStatusBar**: Not implemented (per task spec — future task)

### Recommended Next Tasks
1. Wire up `registerApp()` calls from app components (SDEditor, terminal, etc.)
2. Implement MenuBar with dropdown menus
3. Implement ShellTabBar with workspace tab management
4. Add keyboard shortcut handlers (Ctrl+\\ for split, Ctrl+T for tab, etc.)
