# TASK-008: Shell Core — Reducer, Utils, Constants (JS→TS Port)

## Objective

Port the shell state machine from `simdecisions-2/src/services/shell/` to `browser/src/shell/`. This is the pane layout engine: split, merge, tab, focus, mute, drag-drop zones, undo/redo, workspaces, load states, and the 4-branch root system (layout/float/pinned/spotlight). All files convert from JS to TypeScript during port.

## Dependencies

- **TASK-005 (Relay Bus)** — must be complete. Bus mute constants already ported. MessageBus dispatch used by reducer for LOG_EVENT.
- **TASK-006 (Gate Enforcer)** — must be complete. Browser-side `BrowserGateEnforcer` called for governance checks in reducer actions.
- **TASK-007 (EGG System)** — must be complete. Node types defined in `browser/src/eggs/types.ts`. Import canonical types from there and extend with shell-specific runtime types.

## Source Files

Port from `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\shell\`:

| Source Path | Lines | What It Does |
|-------------|-------|-------------|
| `shell.reducer.js` | 665 | Main reducer: 50+ action types, withUndo helper, 4-branch tree, load states, workspaces, ledger |
| `shell.utils.js` | 436 | Tree operations: findNode, replaceNode, removeNode, getDropZone, makeEmpty, uid (all branch-aware, immutable) |
| `shell.constants.js` | 246 | NODE_TYPES, LOAD_STATES, BRANCH_TYPES, Z_LAYERS, KERNEL_SERVICES, MIN_PANE_PX, SNAP_DELTA_PX, UNDO_LIMIT, THEMES, SHELL_CSS |
| `shell.context.js` | 187 | **Already ported as TASK-005** — skip, import from relay_bus |

Test file:
| Source Path | Lines | What It Does |
|-------------|-------|-------------|
| `__tests__/shell.reducer.test.js` | 1,433 | 60+ test cases: tree ops, branches, focus, maximize, pane state, lifecycle, workspaces, undo/redo, ledger |

## Port Rules

### 1. Modularize the Reducer (665 lines → under 500 per file)

The old `shell.reducer.js` is 665 lines — over the 500-line limit. Split into:

```
browser/src/shell/
├── reducer.ts              -- Main shellReducer switch + INITIAL_STATE + withUndo helper (~200 lines)
├── actions/
│   ├── layout.ts           -- SPLIT, MERGE, FLIP_SPLIT, TRIPLE_SPLIT, UPDATE_TRIPLE_SPLIT_RATIOS,
│   │                          REMOVE_TRIPLE_SPLIT_CHILD, FLIP_TRIPLE_SPLIT, UPDATE_RATIO,
│   │                          ADD_TAB, CLOSE_TAB, REORDER_TAB, SET_ACTIVE_TAB, MOVE_APP (~250 lines)
│   ├── branch.ts           -- REPARENT_TO_BRANCH, SET_Z_ORDER, FOCUS_FLOAT_PANE,
│   │                          ADD_SPOTLIGHT, REMOVE_SPOTLIGHT, TRIGGER_SLIDES_OVER,
│   │                          RETRACT_SLIDES_OVER (~150 lines)
│   └── lifecycle.ts        -- SPAWN_APP, CLOSE_APP, OPEN_PANE, MINIMIZE_PANE, WARM_KERNEL,
│                              SET_LOAD_STATE, SET_SIZE_STATE, SAVE_WORKSPACE, LOAD_WORKSPACE,
│                              SET_SWAP_PENDING, SWAP_CONTENTS (~200 lines)
```

The main `reducer.ts` imports action handlers and delegates:
```typescript
import { handleLayout } from './actions/layout';
import { handleBranch } from './actions/branch';
import { handleLifecycle } from './actions/lifecycle';

export function shellReducer(state: ShellState, action: ShellAction): ShellState {
  switch (action.type) {
    // Layout actions
    case 'SPLIT': case 'MERGE': case 'ADD_TAB': /* ... */
      return handleLayout(state, action);
    // Branch actions
    case 'REPARENT_TO_BRANCH': case 'SET_Z_ORDER': /* ... */
      return handleBranch(state, action);
    // Lifecycle actions
    case 'SPAWN_APP': case 'CLOSE_APP': /* ... */
      return handleLifecycle(state, action);
    // Inline handlers for simple actions
    case 'SET_FOCUS': return { ...state, focusedPaneId: action.paneId, ... };
    // ...
    default: return state;
  }
}
```

### 2. Type the State and Actions

Create `browser/src/shell/types.ts` with:

```typescript
import { NodeType } from '../eggs/types';

/** Shell-specific node types extending EGG types. */
export enum ShellNodeType {
  APP = 'app',              // Leaf node (maps to EGG's PANE)
  SPLIT = 'split',          // 2-way split
  TRIPLE_SPLIT = 'triple-split', // 3-way split (shell-only, not in EGG layout)
  TABBED = 'tabbed',        // Tab container (maps to EGG's TAB_GROUP)
  BRANCHES = 'branches',    // Root container (shell-only runtime type)
}

/** Load states for pane lifecycle. */
export enum LoadState {
  COLD = 'COLD',   // Registered but not instantiated
  WARM = 'WARM',   // State initialized, invisible
  HOT = 'HOT',     // Visible and active
}

/** Branch types for 4-branch root. */
export enum BranchType {
  LAYOUT = 'layout',
  FLOAT = 'float',
  PINNED = 'pinned',
  SPOTLIGHT = 'spotlight',
}

/** App node — leaf in the pane tree. */
export interface AppNode {
  type: ShellNodeType.APP;
  id: string;
  appType: string;
  appConfig: Record<string, unknown>;
  label: string;
  audioMuted: boolean;
  busMute: MuteLevel;
  notification: 'warn' | 'error' | 'info' | null;
  locked: boolean;
  chrome: boolean;
  meta: Record<string, unknown>;
  accepts: string[];
  loadState: LoadState;
  sizeStates: Record<string, unknown> | null;
  defaultState: unknown;
  currentSizeState: string | null;
}

/** Split node — binary split container. */
export interface SplitNode {
  type: ShellNodeType.SPLIT;
  id: string;
  direction: 'horizontal' | 'vertical';
  ratio: number;
  children: [ShellTreeNode, ShellTreeNode];
}

/** Triple split node — 3-way split container. */
export interface TripleSplitNode {
  type: ShellNodeType.TRIPLE_SPLIT;
  id: string;
  direction: 'horizontal' | 'vertical';
  ratios: [number, number, number];
  children: [ShellTreeNode, ShellTreeNode, ShellTreeNode];
}

/** Tabbed node — tab container. */
export interface TabbedNode {
  type: ShellNodeType.TABBED;
  id: string;
  children: ShellTreeNode[];
  activeIndex: number;
}

/** Any node in the pane tree. */
export type ShellTreeNode = AppNode | SplitNode | TripleSplitNode | TabbedNode;

/** Branches root — 4-branch container. */
export interface BranchesRoot {
  type: ShellNodeType.BRANCHES;
  layout: ShellTreeNode;
  float: AppNode[];
  pinned: AppNode[];
  spotlight: AppNode | null;
}

/** Full shell state. */
export interface ShellState {
  root: BranchesRoot;
  focusedPaneId: string | null;
  maximizedPaneId: string | null;
  swapPendingId: string | null;
  workspaces: Workspace[];
  ledger: LedgerEvent[];
  lastFocusedByAppType: Record<string, string>;
  settingsRegistry: Record<string, PaneSettings>;
  past: ShellState[];
  future: ShellState[];
}

// ... plus ShellAction discriminated union, Workspace, LedgerEvent, PaneSettings types
```

Import `MuteLevel` from `'../infrastructure/relay_bus'` (already ported in TASK-005).

### 3. Node Types — Import from TASK-007, Extend Locally

Check what TASK-007 delivered in `browser/src/eggs/types.ts`. The EGG system defines layout node types (PANE, SPLIT, TAB_GROUP, etc.). The shell extends these with runtime-only types:

- `TRIPLE_SPLIT` — shell-only (EGGs define binary splits; triple-split is a reducer optimization)
- `BRANCHES` — shell-only root container type (not in EGG layouts)

Import EGG types where they overlap, define shell-specific types in `shell/types.ts`. Add a mapping function:

```typescript
/** Map EGG NodeType to ShellNodeType for inflation. */
export function eggNodeToShellNode(eggType: NodeType): ShellNodeType {
  switch (eggType) {
    case NodeType.PANE: return ShellNodeType.APP;
    case NodeType.SPLIT: return ShellNodeType.SPLIT;
    case NodeType.TAB_GROUP: return ShellNodeType.TABBED;
    default: return ShellNodeType.APP;
  }
}
```

### 4. Constants — Split CSS from Logic

`shell.constants.js` has 174 lines of inline CSS (`SHELL_CSS`). Extract to:

- `browser/src/shell/shell-themes.css` — theme CSS (all `var(--sd-*)` overrides, animations)
- `browser/src/shell/constants.ts` — pure TS constants

Constants to define in `constants.ts`:
```typescript
export const MIN_PANE_PX = 150;
export const SNAP_DELTA_PX = 10;
export const IDLE_MS = 3000;
export const UNDO_LIMIT = 20;
export const LEDGER_CAP = 1000;

export const KERNEL_SERVICES = [
  'event-ledger', 'governance-dashboard', 'four-vector',
  'threat-scanner', 'approval-queue',
] as const;

export const Z_LAYERS = {
  LAYOUT: 1,
  FLOAT_START: 10,
  PINNED_START: 100,
  SPOTLIGHT: 1000,
} as const;

export const THEMES = [
  { id: 'full-color', label: 'Full Color' },
  { id: 'depth', label: 'Depth' },
  { id: 'light', label: 'Light' },
  { id: 'monochrome', label: 'Monochrome' },
  { id: 'high-contrast', label: 'High Contrast' },
] as const;
```

Do NOT re-export BUS_MUTE_CYCLE, BUS_MUTE_LABELS, BUS_MUTE_ICONS, BUS_MESSAGE_TYPES — those are already in `infrastructure/relay_bus/constants.ts` (TASK-005). Import from there if needed.

### 5. Utils — Port with TypeScript, Keep Branch-Aware

`shell.utils.js` (436 lines) is under the limit. Port as `browser/src/shell/utils.ts` with:
- Full TypeScript types on all functions
- Import `ShellTreeNode`, `AppNode`, `BranchesRoot`, etc. from `./types`
- `uid()` — already ported in TASK-005 (`import { uid } from '../infrastructure/relay_bus'`). Import, don't duplicate.
- `makeEmpty()` — returns typed `AppNode`
- All tree ops typed: `findNode(root: BranchesRoot, id: string): ShellTreeNode | null`
- `getDropZone()` returns typed union: `'center' | 'left' | 'right' | 'top' | 'bottom'`
- All operations remain immutable

### 6. volumeStorage Dependency

The reducer calls `writeVolume()` for workspace persistence. Create a minimal interface:

```typescript
// browser/src/shell/volumeStorage.ts
export interface VolumeStorage {
  writeVolume(key: string, data: unknown): void;
  readVolume(key: string): unknown | null;
}

let _storage: VolumeStorage | null = null;

export function setVolumeStorage(storage: VolumeStorage): void {
  _storage = storage;
}

export function getVolumeStorage(): VolumeStorage | null {
  return _storage;
}
```

The actual storage implementation comes in a future task. For now, the reducer calls `getVolumeStorage()?.writeVolume(...)` — no-op if not configured.

### 7. Governance Integration

The reducer should check `BrowserGateEnforcer` for actions that modify pane state. Import from TASK-006 delivery:

```typescript
import { BrowserGateEnforcer } from '../infrastructure/gate_enforcer';
```

The `isLocked()` helper already blocks operations on locked panes. Add a governance check for structural actions (SPLIT, MERGE, SPAWN_APP, CLOSE_APP, MOVE_APP):
- Call `gateEnforcer.checkAction(agentId, actionType)` if a gate enforcer is configured
- If result is BLOCK → return state unchanged (log to ledger)
- If no gate enforcer configured → proceed normally (standalone mode)

The gate enforcer is optional — the reducer works without it.

### 8. Test Modularization

The old `shell.reducer.test.js` is 1,433 lines. Split into:

```
browser/src/shell/__tests__/
├── reducer.test.ts           -- Core: INITIAL_STATE, default case, SET_FOCUS, MAXIMIZE/RESTORE,
│                                SET_AUDIO_MUTE, SET_BUS_MUTE, SET_LABEL, SET_APP_STATE,
│                                SET_NOTIFICATION, SET_LOCKED, LOG_EVENT, REGISTER_PANE_SETTINGS (~300 lines)
├── reducer.layout.test.ts    -- SPLIT, MERGE, ADD_TAB, CLOSE_TAB, REORDER_TAB, SET_ACTIVE_TAB,
│                                MOVE_APP, FLIP_SPLIT, TRIPLE_SPLIT, UPDATE_RATIO (~400 lines)
├── reducer.branch.test.ts    -- REPARENT_TO_BRANCH, SET_Z_ORDER, FOCUS_FLOAT_PANE,
│                                ADD_SPOTLIGHT, REMOVE_SPOTLIGHT, TRIGGER_SLIDES_OVER,
│                                RETRACT_SLIDES_OVER (~300 lines)
├── reducer.lifecycle.test.ts -- SPAWN_APP, CLOSE_APP, OPEN_PANE, MINIMIZE_PANE, WARM_KERNEL,
│                                SET_LOAD_STATE, SET_SIZE_STATE, SAVE_WORKSPACE, LOAD_WORKSPACE,
│                                SWAP_CONTENTS (~300 lines)
├── reducer.undo.test.ts      -- LAYOUT_UNDO, LAYOUT_REDO, undo stack behavior, UNDO_LIMIT (~200 lines)
├── utils.test.ts             -- findNode, findParent, replaceNode, removeNodeFromTree,
│                                makeEmpty, getDropZone, computeSizeState, collectAppIds,
│                                getNodeDepth, validateTripleSplit, resetLoadStates (~300 lines)
├── constants.test.ts         -- All constant values, enum membership (~50 lines)
├── types.test.ts             -- Type guard tests, node creation, state shape (~100 lines)
```

## File Structure

```
browser/src/shell/
├── index.ts                -- Public exports
├── types.ts                -- ShellState, ShellTreeNode, AppNode, ShellAction, enums
├── constants.ts            -- MIN_PANE_PX, UNDO_LIMIT, Z_LAYERS, THEMES, KERNEL_SERVICES
├── shell-themes.css        -- Theme CSS extracted from SHELL_CSS (all var(--sd-*))
├── utils.ts                -- Tree operations (branch-aware, immutable)
├── reducer.ts              -- Main shellReducer + INITIAL_STATE + withUndo
├── volumeStorage.ts        -- VolumeStorage interface + getter/setter
├── actions/
│   ├── layout.ts           -- Layout action handlers
│   ├── branch.ts           -- Branch action handlers
│   └── lifecycle.ts        -- Lifecycle action handlers
└── __tests__/
    ├── reducer.test.ts
    ├── reducer.layout.test.ts
    ├── reducer.branch.test.ts
    ├── reducer.lifecycle.test.ts
    ├── reducer.undo.test.ts
    ├── utils.test.ts
    ├── constants.test.ts
    └── types.test.ts
```

## Test Requirements

### Port and Split Existing Tests

Port `shell.reducer.test.js` (1,433 lines), splitting into the test files listed above. Fix imports:
- `shell.utils` → `../utils`
- `shell.constants` → `../constants`
- `shell.context` → `../../infrastructure/relay_bus`
- Mock `volumeStorage` with `vi.mock('../volumeStorage')`

### Coverage Requirements

**reducer.test.ts:**
- [ ] INITIAL_STATE has correct shape and defaults
- [ ] Unknown action returns state unchanged
- [ ] SET_FOCUS updates focusedPaneId and lastFocusedByAppType
- [ ] MAXIMIZE / RESTORE set/clear maximizedPaneId
- [ ] SET_AUDIO_MUTE, SET_BUS_MUTE, SET_LABEL, SET_APP_STATE, SET_NOTIFICATION, SET_LOCKED — all no-undo
- [ ] LOG_EVENT appends, caps at LEDGER_CAP
- [ ] REGISTER_PANE_SETTINGS updates registry

**reducer.layout.test.ts:**
- [ ] SPLIT creates binary split (horizontal, vertical)
- [ ] SPLIT enforces max depth 2
- [ ] SPLIT pushes to undo
- [ ] MERGE collapses split, keeps correct child
- [ ] ADD_TAB converts pane to tabbed, adds tab to existing
- [ ] CLOSE_TAB removes tab, collapses if empty
- [ ] REORDER_TAB moves tab position
- [ ] SET_ACTIVE_TAB sets index (no undo)
- [ ] MOVE_APP handles all 5 zones (center/left/right/top/bottom)
- [ ] FLIP_SPLIT toggles direction
- [ ] TRIPLE_SPLIT creates 3-way, enforces depth
- [ ] UPDATE_TRIPLE_SPLIT_RATIOS adjusts ratios
- [ ] UPDATE_RATIO resizes binary split

**reducer.branch.test.ts:**
- [ ] REPARENT_TO_BRANCH moves between layout↔float↔pinned↔spotlight
- [ ] REPARENT preserves appType, config, label
- [ ] SET_Z_ORDER reorders float array
- [ ] FOCUS_FLOAT_PANE moves to top of float
- [ ] ADD_SPOTLIGHT / REMOVE_SPOTLIGHT manage spotlight pane
- [ ] TRIGGER_SLIDES_OVER ejects to float with slidesOver flag
- [ ] RETRACT_SLIDES_OVER returns to layout as new split

**reducer.lifecycle.test.ts:**
- [ ] SPAWN_APP sets appType, config, loadState=COLD
- [ ] CLOSE_APP replaces with empty
- [ ] OPEN_PANE transitions COLD/WARM → HOT
- [ ] MINIMIZE_PANE transitions HOT → WARM
- [ ] WARM_KERNEL transitions COLD → WARM for kernel services only
- [ ] SET_LOAD_STATE updates and logs
- [ ] SAVE_WORKSPACE saves tree snapshot
- [ ] LOAD_WORKSPACE restores tree, resets loadStates
- [ ] SWAP_CONTENTS exchanges pane contents

**reducer.undo.test.ts:**
- [ ] Structural actions push to past
- [ ] LAYOUT_UNDO restores previous, pushes to future
- [ ] LAYOUT_REDO restores next, pushes to past
- [ ] UNDO_LIMIT caps past stack
- [ ] New structural action clears future

**utils.test.ts:**
- [ ] makeEmpty returns valid AppNode with all defaults
- [ ] findNode finds in layout, float, pinned, spotlight
- [ ] findParent returns direct parent
- [ ] replaceNode creates new tree (immutable)
- [ ] removeNodeFromTree collapses parent split
- [ ] getNodeDepth counts split ancestors
- [ ] getDropZone maps mouse position to zone
- [ ] collectAppIds returns all leaf IDs across branches
- [ ] validateTripleSplit checks 3 children, ratios sum to 1.0
- [ ] resetLoadStates sets all to HOT

**Minimum: 80+ tests.**

## Source Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\shell\shell.reducer.js`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\shell\shell.utils.js`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\shell\shell.constants.js`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\shell\__tests__\shell.reducer.test.js`

Also check TASK-005, TASK-006, TASK-007 outputs for:
- `uid()` export path from relay_bus
- `MuteLevel` type from relay_bus
- `BrowserGateEnforcer` import path from gate_enforcer
- `NodeType` enum from eggs/types.ts
- `configEggCache` import path

## What NOT to Build

- No shell renderer components (TASK-009)
- No PaneChrome, SplitDivider, FloatPaneWrapper (TASK-009)
- No AppletShell or AppFrame (TASK-009)
- No actual volume storage implementation (just the interface)
- No context (already ported as relay_bus in TASK-005)
- No CSS beyond shell-themes.css (component CSS is TASK-009)
- No React components — this is pure state logic

## Constraints

- TypeScript strict mode
- All files under 500 lines (reducer split into 4 files)
- No stubs — every action handler fully implemented
- All CSS uses `var(--sd-*)` — no hex, no rgb, no named colors
- All tree operations immutable
- Test with vitest
- Import uid from relay_bus, don't duplicate
- Import bus constants from relay_bus, don't duplicate

## Deliverables

### Source Files
- [ ] `browser/src/shell/index.ts`
- [ ] `browser/src/shell/types.ts`
- [ ] `browser/src/shell/constants.ts`
- [ ] `browser/src/shell/shell-themes.css`
- [ ] `browser/src/shell/utils.ts`
- [ ] `browser/src/shell/reducer.ts`
- [ ] `browser/src/shell/volumeStorage.ts`
- [ ] `browser/src/shell/actions/layout.ts`
- [ ] `browser/src/shell/actions/branch.ts`
- [ ] `browser/src/shell/actions/lifecycle.ts`

### Test Files
- [ ] `browser/src/shell/__tests__/reducer.test.ts`
- [ ] `browser/src/shell/__tests__/reducer.layout.test.ts`
- [ ] `browser/src/shell/__tests__/reducer.branch.test.ts`
- [ ] `browser/src/shell/__tests__/reducer.lifecycle.test.ts`
- [ ] `browser/src/shell/__tests__/reducer.undo.test.ts`
- [ ] `browser/src/shell/__tests__/utils.test.ts`
- [ ] `browser/src/shell/__tests__/constants.test.ts`
- [ ] `browser/src/shell/__tests__/types.test.ts`

**18 deliverables total (10 source + 8 test).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-008-RESPONSE.md`

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
