# TASK-016: Tree Browser Primitive (P-07)

## Objective

Build a reusable tree browser primitive at `browser/src/primitives/tree-browser/`. This is a generic, recursive tree view component that serves as the foundation for chat history sidebars, file explorers, branch navigators, and any hierarchical data display.

## Context

No tree browser exists in the old repo — Sidebar.tsx is a flat nav, FileBrowserApp.tsx is a flat file list, BranchExplorer.tsx is a flat branch list. This is a new primitive, not a port.

The tree browser must work in two modes:
1. **Flat list mode** — chat history sidebar (conversations as flat items with timestamps, search/filter)
2. **Nested tree mode** — file explorer (folders with expand/collapse, nested children)

Both modes use the same component with different data shapes. A flat list is just a tree with no children.

### Use Cases

| Product | Use Case | Mode |
|---------|----------|------|
| Chat (chat.egg.md) | Conversation history sidebar | Flat list |
| IDE (ide.egg.md) | File explorer sidebar | Nested tree |
| IDE (ide.egg.md) | Git branch explorer | Flat list with badges |
| Design (design.egg.md) | Layer/component tree | Nested tree with drag |
| All products | Settings tree | Nested tree |

### Integration with Shell

The tree browser is a **pane primitive** — it registers as appType `'tree-browser'` in the app registry. EGG configs place it in split layouts (typically left side, 250px width). It communicates with other panes via the relay bus:

- Publishes: `tree-browser:select` (nodeId, meta) when a node is selected
- Publishes: `tree-browser:action` (nodeId, actionId) when an action fires via FAB/command palette
- Subscribes: `tree-browser:refresh` to reload data
- Subscribes: `tree-browser:select-node` to programmatically select a node

### Interaction Model — SPEC-PANE-INTERACTION-001

**NO native right-click context menus anywhere.** Follow these rules:

- **Click/tap** on a node: selects it, publishes `tree-browser:select` on the bus
- **Actions** on a selected node: triggered via FAB (floating action button) or command palette through the bus. The tree browser does NOT render its own action menu — it publishes the selected node's available actions on the bus and the shell's FAB/command palette system handles display.
- **Long-press on mobile**: publishes `tree-browser:long-press` (nodeId, actions[]) on the bus. The shell's action sheet system handles display.
- **Drag-from-tree**: nodes with `draggable: true` can be dragged. On drag start, publish `DRAG_START` on the bus with `{ dataType: 'tree-node', nodeId, meta }`. Drop targets (other panes) handle via existing bus drop protocol.

## Files to Read First

Read these to understand existing patterns:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\appRegistry.ts` (33 lines) — AppRendererProps interface
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\index.ts` — MessageBus API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` — pattern reference for primitive types
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\index.ts` — pattern reference for primitive exports
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — CSS variables to use

## Type Definitions

### types.ts

```typescript
/** A node in the tree. Recursive — children make it a folder. */
export interface TreeNodeData {
  id: string;
  label: string;
  icon?: string;                    // CSS class or emoji, rendered by TreeNodeRow
  children?: TreeNodeData[];        // If present, node is expandable
  badge?: TreeBadge | null;
  meta?: Record<string, unknown>;   // Arbitrary data (conversation timestamp, file size, etc.)
  draggable?: boolean;
  droppable?: boolean;              // Can children be dropped here?
  disabled?: boolean;
  actions?: TreeNodeAction[];       // Actions available for this node (published on bus for FAB/palette)
}

export interface TreeBadge {
  text: string;
  type: 'default' | 'active' | 'success' | 'warning';
}

export interface TreeNodeAction {
  id: string;
  label: string;
  icon?: string;
  danger?: boolean;                 // Destructive action flag
}

export interface TreeBrowserProps {
  /** Tree data. Flat list = no children on any node. */
  nodes: TreeNodeData[];
  /** Currently selected node ID. Controlled component. */
  selectedId?: string | null;
  /** Called when a node is clicked. */
  onSelect: (nodeId: string, node: TreeNodeData) => void;
  /** Called when a node is expanded (chevron clicked or arrow right). */
  onExpand?: (nodeId: string) => void;
  /** Called when a node is collapsed. */
  onCollapse?: (nodeId: string) => void;
  /** Called when a node starts being dragged. */
  onDragStart?: (nodeId: string, node: TreeNodeData) => void;
  /** Header text above the tree. */
  header?: string;
  /** Action buttons rendered in the header bar (e.g., "New" button). */
  headerActions?: React.ReactNode;
  /** Placeholder text for search input. Empty string disables search. */
  searchPlaceholder?: string;
  /** Content to render when nodes array is empty. */
  emptyState?: React.ReactNode;
  /** IDs of expanded nodes. Controlled. If omitted, internal state used. */
  expandedIds?: Set<string>;
  /** Indent per nesting level in px. Default: 16. */
  indentPx?: number;
}

/** State returned by useTreeState hook. */
export interface TreeState {
  expandedIds: Set<string>;
  searchQuery: string;
  filteredNodes: TreeNodeData[];
  toggle: (nodeId: string) => void;
  expandAll: () => void;
  collapseAll: () => void;
  setSearchQuery: (query: string) => void;
}

/** Config shape for tree-browser pane in EGG layout. */
export interface TreeBrowserPaneConfig {
  adapter: 'chat-history' | 'filesystem' | 'custom';
  header?: string;
  searchPlaceholder?: string;
  /** For filesystem adapter: root path to list */
  rootPath?: string;
  /** For chat-history adapter: storage key prefix */
  storageKey?: string;
}
```

## Component Architecture

```
browser/src/primitives/tree-browser/
├── types.ts                    — TreeNodeData, TreeBrowserProps, TreeNodeAction, TreeState
├── useTreeState.ts             — Hook: expand/collapse, search/filter, keyboard nav
├── TreeNodeRow.tsx             — Single node row: indent, icon, chevron, label, badge, drag handle
├── TreeBrowser.tsx             — Main container: header bar, search input, scrollable tree body
├── adapters/
│   ├── chatHistoryAdapter.ts   — Reads conversation list from localStorage, returns TreeNodeData[]
│   └── filesystemAdapter.ts    — Reads directory listing (stub until hivenode API wired), returns TreeNodeData[]
├── tree-browser.css            — All styling (var(--sd-*) only)
├── index.ts                    — Public exports
└── __tests__/
    ├── useTreeState.test.ts    — Hook tests
    ├── TreeNodeRow.test.tsx    — Node rendering tests
    ├── TreeBrowser.test.tsx    — Integration tests
    ├── chatHistoryAdapter.test.ts — Chat history adapter tests
    └── filesystemAdapter.test.ts  — Filesystem adapter tests
```

## Component Details

### TreeBrowser.tsx (main container)
- Header bar with title + action buttons (e.g., "New Conversation", "New File")
- Search/filter input (optional, enabled via searchPlaceholder prop)
- Scrollable tree body (overflow-y: auto)
- Empty state when no nodes or all filtered out
- Keyboard navigation: ArrowUp/Down to move selection, ArrowRight to expand, ArrowLeft to collapse, Enter to select, Escape to clear search
- Receives all TreeBrowserProps

### TreeNodeRow.tsx (individual node)
- Renders at correct indent level (depth * indentPx)
- Chevron icon for expandable nodes (rotates 90° when expanded)
- Node icon (optional, from `icon` prop — CSS class applied to a span)
- Label text (truncated with ellipsis if too long)
- Badge (optional, pill-shaped, colored by type)
- Active/selected state (background highlight + left border accent)
- Hover state (subtle background)
- Drag handle (optional, only when draggable=true) — on drag start, calls onDragStart
- Disabled state (reduced opacity, no click handler)
- Recursive: renders children TreeNodeRows when expanded
- NO right-click handler. NO context menu.

### useTreeState.ts (state hook)
- Manages expandedIds set (toggle, expandAll, collapseAll)
- Manages searchQuery string
- Computes filteredNodes: filters tree recursively (keeps parents of matching children)
- Keyboard navigation state (focusedIndex for arrow key movement)
- Controlled vs uncontrolled: uses prop expandedIds if provided, otherwise internal state

### adapters/chatHistoryAdapter.ts
- Reads conversation entries from localStorage key (default: `sd:frank_entries`)
- Groups conversations by date (Today, Yesterday, This Week, Older)
- Returns TreeNodeData[] — date groups as parent nodes, conversations as children (flat within group)
- Each conversation node has `meta: { conversationId, lastMessage, timestamp }`
- Badge shows message count

### adapters/filesystemAdapter.ts
- Takes a root path string
- For MVP: returns a stubbed directory tree (hardcoded sample data)
- Interface ready for hivenode API integration: `async function loadDirectoryTree(rootPath: string): Promise<TreeNodeData[]>`
- File nodes have `meta: { path, size, modified }`
- Folder nodes have children
- Icons: folder emoji for dirs, file emoji for files

## Deliverables

### Source Files (8)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\useTreeState.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\tree-browser.css`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\index.ts`

### Test Files (5)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\useTreeState.test.ts` — 12 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.test.tsx` — 10 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeBrowser.test.tsx` — 12 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\chatHistoryAdapter.test.ts` — 6 tests
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\filesystemAdapter.test.ts` — 5 tests

**Total: 13 deliverables (8 source + 5 test), 45+ tests**

## Test Requirements (~45 tests minimum)

### useTreeState.test.ts (~12 tests)
- [ ] Initializes with all nodes collapsed
- [ ] toggle() expands a collapsed node
- [ ] toggle() collapses an expanded node
- [ ] expandAll() expands every node with children
- [ ] collapseAll() collapses all nodes
- [ ] setSearchQuery filters nodes by label (case insensitive)
- [ ] Search preserves parent nodes of matching children
- [ ] Empty search query shows all nodes
- [ ] Search with no matches returns empty array
- [ ] Controlled expandedIds prop overrides internal state
- [ ] filteredNodes updates when nodes prop changes
- [ ] Search handles special regex characters safely

### TreeNodeRow.test.tsx (~10 tests)
- [ ] Renders label text
- [ ] Renders at correct indent level (depth * indentPx)
- [ ] Shows chevron for nodes with children
- [ ] Hides chevron for leaf nodes
- [ ] Chevron rotates when expanded
- [ ] Calls onSelect when clicked
- [ ] Calls onExpand when chevron clicked on collapsed node
- [ ] Calls onCollapse when chevron clicked on expanded node
- [ ] Renders badge with correct type class
- [ ] Disabled node has reduced opacity and no click handler

### TreeBrowser.test.tsx (~12 tests)
- [ ] Renders header text
- [ ] Renders header action buttons
- [ ] Renders search input when searchPlaceholder is provided
- [ ] Hides search input when searchPlaceholder is empty/undefined
- [ ] Renders all top-level nodes
- [ ] Renders nested children when parent expanded
- [ ] Hides nested children when parent collapsed
- [ ] Shows empty state when nodes array is empty
- [ ] Shows empty state when search filters out all nodes
- [ ] ArrowDown moves selection to next visible node
- [ ] ArrowUp moves selection to previous visible node
- [ ] ArrowRight expands selected node with children

### chatHistoryAdapter.test.ts (~6 tests)
- [ ] Returns empty array when no conversations in localStorage
- [ ] Groups conversations by date (Today, Yesterday, etc.)
- [ ] Each conversation node has correct meta fields
- [ ] Badge shows message count
- [ ] Handles malformed localStorage data gracefully
- [ ] Sorts conversations by timestamp descending within groups

### filesystemAdapter.test.ts (~5 tests)
- [ ] Returns stubbed directory tree for MVP
- [ ] Folder nodes have children array
- [ ] File nodes have no children
- [ ] Nodes have correct meta fields (path, size, modified)
- [ ] loadDirectoryTree returns a Promise

## Constraints

- TypeScript strict mode
- All files under 500 lines
- CSS: `var(--sd-*)` only — no hex, no rgb(), no named colors
- vitest + @testing-library/react
- No external tree library dependencies (build from scratch)
- No stubs — every function fully implemented (filesystem adapter uses sample data, not a stub)
- Keyboard accessible (arrow keys, Enter, Escape)
- All text truncated with CSS ellipsis (no overflow)
- **NO right-click context menus** — actions via bus only (SPEC-PANE-INTERACTION-001)
- **NO ContextMenu component** — do not create one

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-016-RESPONSE.md`

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
