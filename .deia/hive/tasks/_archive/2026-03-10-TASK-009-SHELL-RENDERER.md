# TASK-009: Shell Renderer — Visual Tree Components (JSX→TSX Port)

## Objective

Port the shell renderer components from `simdecisions-2/src/components/shell/` to `browser/src/shell/components/`. These are the visual layer that renders the pane layout tree: recursive split rendering, pane chrome (title bar + controls), floating panes, dividers, drag-drop zones, and the root Shell frame. All JSX files convert to TSX during port.

## Dependencies

- **TASK-008 (Shell Core)** must be complete. Renderer reads `ShellState` from the reducer and dispatches actions. Imports types, constants, and utils from `browser/src/shell/`.
- **TASK-005 (Relay Bus)** must be complete. Components use `useShell()` for bus access and dispatch.
- **TASK-007 (EGG System)** must be complete. PaneContent routes app types defined in EGG configs.

## Source Files

Port from `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\`:

| Source Path | Dest Path | Lines | JSX/TSX | What It Does |
|-------------|-----------|-------|---------|-------------|
| `Shell.tsx` | `components/Shell.tsx` | 64 | TSX | Root shell frame: MenuBar + ShellTabBar + SplitTree body |
| `SplitTree.tsx` | `components/SplitTree.tsx` | 172 | TSX | Recursive split renderer with react-resizable-panels, context menu, max depth enforcement |
| `ShellNodeRenderer.jsx` | `components/ShellNodeRenderer.tsx` | 267 | JSX→TSX | Node type router: dispatches to SplitContainer/TripleSplit/Tabbed/PaneChrome. Drag-drop state, load states, ResizeObserver |
| `TripleSplitContainer.jsx` | `components/TripleSplitContainer.tsx` | 253 | JSX→TSX | 3-way split with independent dividers, slides-over detection, ratio management |
| `SplitDivider.jsx` | `components/SplitDivider.tsx` | 148 | JSX→TSX | Draggable divider: ratio adjustment, min-size clamping, snap-to-center, slides-over trigger |
| `PaneChrome.jsx` | `components/PaneChrome.tsx` | 161 | JSX→TSX | Title bar: drag handle, lock icon, label, notification dot, mute buttons, maximize/close |
| `PaneContent.tsx` | `components/PaneContent.tsx` | 75 | TSX | Routes pane content to app components by appType |
| `FloatPaneWrapper.jsx` | `components/FloatPaneWrapper.tsx` | 151 | JSX→TSX | Draggable + resizable float pane, slides-over retract on click-outside/Escape |
| `AppletShell.tsx` | `components/AppletShell.tsx` | 39 | TSX | Applet lifecycle wrapper: notification modal, shortcuts popup |

**Total source: ~1,330 lines across 9 components.**

### CSS Files

| Source Path | Dest Path | Lines |
|-------------|-----------|-------|
| `shell.css` | `components/shell.css` | (check old repo) |
| `AppletShell.css` | `components/AppletShell.css` | (check old repo) |

### Supporting Components (check if needed)

These are referenced by the main components. Port only what's needed:

| Component | Referenced By | Action |
|-----------|--------------|--------|
| `EmptyPane` | ShellNodeRenderer, FloatPaneWrapper | Port — renders empty pane placeholder |
| `AppFrame` | ShellNodeRenderer, FloatPaneWrapper | Port — app component loader based on appType |
| `ContextMenu` | SplitTree | Port — right-click context menu |
| `ChromeBtn` | PaneChrome | Port — icon button component |
| `PaneMenu` | PaneChrome | Port — dropdown menu for pane actions |
| `DropZone` | ShellNodeRenderer | Port — visual drop target overlay |
| `SwapTarget` | ShellNodeRenderer | Port — swap mode overlay |
| `TabbedContainer` | ShellNodeRenderer | Port — tab group renderer |
| `SplitContainer` | ShellNodeRenderer | Port — binary split wrapper (may be same as SplitTree) |

Check if these exist as separate files. If they're small inline components (< 50 lines), fold them into the parent. If larger, create separate files. The bee should read the imports in each source file and track down all referenced components.

## Port Rules

### 1. JSX → TSX Conversion

For each JSX file:
- Add TypeScript props interfaces
- Type all state hooks: `useState<DropZone>(null)`
- Type all refs: `useRef<HTMLDivElement>(null)`
- Type all event handlers
- Type all callback props
- Remove prop-types imports if present

### 2. Import Updates

| Old Import | New Import |
|------------|-----------|
| `./shell.context` (useShell) | `../../infrastructure/relay_bus` |
| `./shell.utils` | `../utils` |
| `./shell.constants` | `../constants` |
| `./shell.reducer` | `../reducer` or `../types` |
| `dragDropUtils` | `../utils` or inline |

### 3. PaneContent — App Registry Pattern

The old `PaneContent` hardcodes app type → component mapping. Implement a registry pattern:

```typescript
// browser/src/shell/components/appRegistry.ts

type AppRenderer = React.ComponentType<{ paneId: string; isActive: boolean; config: Record<string, unknown> }>;

const registry = new Map<string, AppRenderer>();

export function registerApp(appType: string, renderer: AppRenderer): void {
  registry.set(appType, renderer);
}

export function getAppRenderer(appType: string): AppRenderer | undefined {
  return registry.get(appType);
}
```

PaneContent calls `getAppRenderer(node.appType)` instead of hardcoded switch. This lets future tasks register their app components (SDEditor registers as `'text-editor'`, etc.) without modifying PaneContent.

### 4. External Dependencies

These npm packages are needed (add to `browser/package.json`):
- `react-resizable-panels` — SplitTree uses Panel, PanelGroup, PanelResizeHandle
- `react-draggable` — FloatPaneWrapper drag behavior
- `react-resizable` — FloatPaneWrapper resize behavior

Check if they're already in `package.json` from TASK-005. If not, add them.

### 5. Drag-Drop Data Transfer

The drag system uses `dataTransfer.setData('hhs/node-id', nodeId)` format. Keep this convention. The `canPaneAcceptDrop()` utility checks node's `accepts` array against the dragged app type.

### 6. CSS Rules

- All CSS uses `var(--sd-*)` custom properties
- No hex, no rgb, no named colors
- Theme CSS is in `shell-themes.css` from TASK-008
- Component CSS uses class prefix: `hhp-` (HiveHostPane)
- Animations: `hhp-reengage` (500ms), `hhp-notif-pulse` (2s), `hhp-gov-glow` (2s) — defined in shell-themes.css
- Chrome states: `.hhp-focused`, `.hhp-reengage`, `.hhp-gov-glow`

### 7. Load State Rendering

ShellNodeRenderer enforces load states:
- `COLD` — don't mount component at all (null)
- `WARM` — mount but render invisible (`display: none` or `visibility: hidden`)
- `HOT` — normal visible rendering

### 8. Shell.tsx — Root Frame

The old Shell.tsx references `MenuBar`, `ShellTabBar`, `TerminalStatusBar`. For now:
- Import `SplitTree` and `PaneContent` from local
- `MenuBar` and `ShellTabBar` — create minimal placeholder components (just a div with the class) if they don't exist yet. These will be fleshed out in future tasks.
- Do NOT import from `stores/shellStore` (old Zustand pattern). Use `useShell()` from relay_bus and `useReducer` with the shell reducer from TASK-008.

### 9. useReducer + Context Integration

The shell uses `useReducer(shellReducer, INITIAL_STATE)` at the root, then provides dispatch via `ShellCtx`. TASK-005 already provides `ShellCtx` with the bus. Extend it:

```typescript
// In Shell.tsx
const [state, dispatch] = useReducer(shellReducer, INITIAL_STATE);
const bus = useMemo(() => new MessageBus(dispatch), [dispatch]);
```

The bus is created with the reducer's dispatch. This is already the pattern from TASK-005. Shell.tsx wires them together.

## File Structure

```
browser/src/shell/components/
├── Shell.tsx                   -- Root shell frame
├── SplitTree.tsx               -- Recursive split renderer
├── ShellNodeRenderer.tsx       -- Node type router
├── TripleSplitContainer.tsx    -- 3-way split
├── SplitDivider.tsx            -- Draggable divider
├── PaneChrome.tsx              -- Pane title bar + controls
├── PaneContent.tsx             -- App content router
├── FloatPaneWrapper.tsx        -- Floating pane container
├── AppletShell.tsx             -- Applet lifecycle wrapper
├── EmptyPane.tsx               -- Empty pane placeholder
├── AppFrame.tsx                -- App component loader
├── ContextMenu.tsx             -- Right-click menu
├── DropZone.tsx                -- Visual drop target overlay
├── TabbedContainer.tsx         -- Tab group renderer
├── appRegistry.ts              -- App type → component registry
├── shell.css                   -- Shell component styles
└── AppletShell.css             -- Applet wrapper styles
```

```
browser/src/shell/components/__tests__/
├── Shell.test.tsx
├── SplitTree.test.tsx
├── ShellNodeRenderer.test.tsx
├── TripleSplitContainer.test.tsx
├── SplitDivider.test.tsx
├── PaneChrome.test.tsx
├── PaneContent.test.tsx
├── FloatPaneWrapper.test.tsx
├── AppletShell.test.tsx
```

## Test Requirements

### Port Existing Tests

Port these test files from old repo, fixing imports:
- `SplitTree.test.tsx` (309 lines)
- `Shell.test.tsx` (179 lines)
- `PaneContent.test.tsx` (179 lines)
- `FloatPaneWrapper.test.tsx` (238 lines)
- `ContextMenu.test.tsx` (86 lines)
- `triple-split.test.js` → `TripleSplitContainer.test.tsx` (161 lines)
- `chrome-false.test.jsx` → fold into `PaneChrome.test.tsx` (153 lines)
- `slides-over.test.js` → fold into `FloatPaneWrapper.test.tsx` or `SplitDivider.test.tsx` (316 lines)

All tests use vitest + @testing-library/react. Mock `useShell()` to provide bus + dispatch.

### New Tests

**ShellNodeRenderer.test.tsx:**
- [ ] Routes APP node to PaneChrome
- [ ] Routes SPLIT node to SplitContainer
- [ ] Routes TRIPLE_SPLIT to TripleSplitContainer
- [ ] Routes TABBED to TabbedContainer
- [ ] COLD load state renders nothing
- [ ] WARM load state renders invisible
- [ ] HOT load state renders visible
- [ ] Drag-over shows DropZone overlay
- [ ] Drop dispatches MOVE_APP action

**SplitDivider.test.tsx:**
- [ ] Drag adjusts ratio
- [ ] Min-size clamping enforced
- [ ] Snap-to-center at 50% ± SNAP_DELTA_PX
- [ ] Double-click resets to 50%
- [ ] Slides-over detection on collapsed pane drag

**PaneChrome.test.tsx:**
- [ ] Renders title bar with label
- [ ] chrome:false renders no title bar
- [ ] Lock icon shows when locked
- [ ] Mute button cycles through mute levels
- [ ] Notification dot pulses on warn/error/info
- [ ] Close button dispatches CLOSE_APP
- [ ] Maximize button dispatches MAXIMIZE

**AppletShell.test.tsx:**
- [ ] Renders children
- [ ] Notification modal triggered by notify
- [ ] Shortcuts popup triggered by showShortcuts

**Minimum: 70+ tests (ported + new).**

## Source Files to Read First

Components:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\Shell.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\SplitTree.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\ShellNodeRenderer.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\TripleSplitContainer.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\SplitDivider.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\PaneChrome.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\PaneContent.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\FloatPaneWrapper.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\AppletShell.tsx`

Supporting components (read to determine scope):
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\EmptyPane.tsx` (or .jsx)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\AppFrame.tsx` (or .jsx)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\ContextMenu.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\TabbedContainer.tsx` (or .jsx)

CSS files:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\shell.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\AppletShell.css`

Tests (port all primary tests):
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\SplitTree.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\Shell.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\PaneContent.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\FloatPaneWrapper.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\ContextMenu.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\triple-split.test.js`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\chrome-false.test.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\__tests__\slides-over.test.js`

Also check TASK-008 output for:
- `ShellState`, `ShellTreeNode`, `AppNode` types in `shell/types.ts`
- `shellReducer`, `INITIAL_STATE` exports from `shell/reducer.ts`
- `findNode`, `makeEmpty`, `getDropZone` from `shell/utils.ts`
- Constants from `shell/constants.ts`

## What NOT to Build

- No shell reducer or utils (TASK-008)
- No shell constants (TASK-008)
- No relay bus (TASK-005)
- No gate enforcer (TASK-006)
- No EGG system (TASK-007)
- No SDEditor or other app components (TASK-010 + future)
- No MenuBar implementation (placeholder only — future task)
- No ShellTabBar implementation (placeholder only — future task)
- No TerminalStatusBar (future task)
- No Zustand stores — use useReducer + context pattern

## Constraints

- TypeScript strict mode
- React 18+
- All files under 500 lines
- No stubs — every component fully implemented
- All CSS uses `var(--sd-*)` — no hex, no rgb, no named colors
- Class prefix: `hhp-` for pane chrome, shell layout classes
- Test with vitest + @testing-library/react
- JSX→TSX: full TypeScript props interfaces on every component
- Immutable state updates (no direct mutation of reducer state in components)

## Deliverables

### Source Files
- [ ] `browser/src/shell/components/Shell.tsx`
- [ ] `browser/src/shell/components/SplitTree.tsx`
- [ ] `browser/src/shell/components/ShellNodeRenderer.tsx`
- [ ] `browser/src/shell/components/TripleSplitContainer.tsx`
- [ ] `browser/src/shell/components/SplitDivider.tsx`
- [ ] `browser/src/shell/components/PaneChrome.tsx`
- [ ] `browser/src/shell/components/PaneContent.tsx`
- [ ] `browser/src/shell/components/FloatPaneWrapper.tsx`
- [ ] `browser/src/shell/components/AppletShell.tsx`
- [ ] `browser/src/shell/components/EmptyPane.tsx`
- [ ] `browser/src/shell/components/AppFrame.tsx`
- [ ] `browser/src/shell/components/ContextMenu.tsx`
- [ ] `browser/src/shell/components/DropZone.tsx`
- [ ] `browser/src/shell/components/TabbedContainer.tsx`
- [ ] `browser/src/shell/components/appRegistry.ts`
- [ ] `browser/src/shell/components/shell.css`
- [ ] `browser/src/shell/components/AppletShell.css`

### Test Files
- [ ] `browser/src/shell/components/__tests__/Shell.test.tsx`
- [ ] `browser/src/shell/components/__tests__/SplitTree.test.tsx`
- [ ] `browser/src/shell/components/__tests__/ShellNodeRenderer.test.tsx`
- [ ] `browser/src/shell/components/__tests__/TripleSplitContainer.test.tsx`
- [ ] `browser/src/shell/components/__tests__/SplitDivider.test.tsx`
- [ ] `browser/src/shell/components/__tests__/PaneChrome.test.tsx`
- [ ] `browser/src/shell/components/__tests__/PaneContent.test.tsx`
- [ ] `browser/src/shell/components/__tests__/FloatPaneWrapper.test.tsx`
- [ ] `browser/src/shell/components/__tests__/AppletShell.test.tsx`

**26 deliverables total (17 source + 9 test).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-009-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
