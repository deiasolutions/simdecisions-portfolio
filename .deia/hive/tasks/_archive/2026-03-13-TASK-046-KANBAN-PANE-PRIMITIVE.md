# TASK-046: Kanban Pane Primitive (React)

## Objective
Port kanban-pane-v03.jsx design to production React primitive. Replaces mock data with HiveNode API calls. Register as appType `kanban`. Full feature parity with spec: accordion columns, filters, drag-drop, mobile responsive, settings sheet.

## Context
This is the first project management primitive for ShiftCenter. It replaces the mock kanban spec with a real, API-backed kanban board. Users can:
- View backlog items + bugs in workflow columns (icebox → backlog → in_progress → review → done)
- Filter by type, priority, graduated status
- Drag-drop cards between columns (desktop) or use mobile move sheet
- Customize column order/labels (future: saved to HiveNode)
- See which items have graduated to feature inventory (✓ badge)

**Design:** Follow the spec exactly — accordion columns, colorblind-accessible palette, triple redundancy (shape + color + border). Mobile-first with bottom sheet patterns.

**Dependencies:** TASK-045 (API routes) must complete first.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\kanban-pane-v03.jsx` (full spec to port)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\index.ts` (primitive registration pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (custom hook pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` (adapter registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\constants.ts` (message bus constants)

## Deliverables

### File Structure
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\index.ts` — export main component
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx` — main component (port of spec)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\useKanban.ts` — custom hook for API + state
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\types.ts` — TypeScript interfaces
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\kanbanAdapter.tsx` — adapter for shell integration
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` to register `kanban` appType

### Component Structure (KanbanPane.tsx)
Port from spec with these changes:
- [ ] Replace `MOCK_DATA` with `useKanban()` hook that fetches from `/api/kanban/items`
- [ ] Replace `DEFAULT_COLUMNS` with data from `/api/kanban/columns`
- [ ] Replace all hardcoded colors with CSS variables (`var(--sd-*)`)
- [ ] Drag-drop `onDrop` handler calls `POST /api/kanban/move` then refetches data
- [ ] Settings sheet column edits call `POST /api/kanban/columns` (returns 501 for now — show user message)
- [ ] Mobile move sheet calls `POST /api/kanban/move` on selection

**CSS Variables Mapping (use EXISTING vars from `browser/src/shell/shell-themes.css`):**
```css
/* These vars EXIST — use them directly */
DS.bg.root        → var(--sd-bg)
DS.bg.card        → var(--sd-surface)
DS.bg.cardSel     → var(--sd-surface-hover)
DS.bg.border      → var(--sd-border)
DS.text.pri       → var(--sd-text-primary)
DS.text.sec       → var(--sd-text-secondary)
DS.text.dim       → var(--sd-text-muted)           /* --sd-text-dim does NOT exist */
DS.text.mute      → var(--sd-text-muted)
DS.accent         → var(--sd-accent)
```

**NEW semantic CSS variables — MUST be added to `shell-themes.css`:**

Add these to the `.hhp-root` block (and corresponding values in each theme variant):

```css
/* Kanban column colors */
--sd-col-icebox:       #6b7a8d;    /* depth: same, light: #8899aa, mono: #777, hc: #aaa */
--sd-col-backlog:      #e89b3f;    /* depth: same, light: #c57b1f, mono: #999, hc: #ff8800 */
--sd-col-in-progress:  #4a90d9;    /* depth: same, light: #2a70b9, mono: #aaa, hc: #44aaff */
--sd-col-review:       #a07cdc;    /* depth: same, light: #7b5cb6, mono: #bbb, hc: #cc88ff */
--sd-col-done:         #3fb8a9;    /* depth: same, light: #1f9889, mono: #ccc, hc: #00ff88 */

/* Priority colors */
--sd-pri-p0:           var(--sd-red);
--sd-pri-p1:           var(--sd-orange);
--sd-pri-p2:           var(--sd-cyan);
--sd-pri-p3:           var(--sd-text-muted);

/* Type colors */
--sd-type-work:        var(--sd-purple);
--sd-type-bug:         var(--sd-red);
```

Map spec names to CSS:
```css
DS.type.work.color → var(--sd-type-work)
DS.type.bug.color  → var(--sd-type-bug)
DS.pri.P0.color    → var(--sd-pri-p0)
DS.pri.P1.color    → var(--sd-pri-p1)
DS.pri.P2.color    → var(--sd-pri-p2)
DS.pri.P3.color    → var(--sd-pri-p3)
DS.col.icebox.color      → var(--sd-col-icebox)
DS.col.backlog.color     → var(--sd-col-backlog)
DS.col.in_progress.color → var(--sd-col-in-progress)
DS.col.review.color      → var(--sd-col-review)
DS.col.done.color        → var(--sd-col-done)
```

### Theme Variables (shell-themes.css)
- [ ] Add the 12 new semantic CSS variables listed above to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
- [ ] Add to `.hhp-root` (default theme), `.hhp-root[data-theme="depth"]`, `.hhp-root[data-theme="light"]`, `.hhp-root[data-theme="monochrome"]`, `.hhp-root[data-theme="high-contrast"]`
- [ ] Priority vars (`--sd-pri-*`) reference existing color vars via `var()` — no new hex values needed
- [ ] Type vars (`--sd-type-*`) reference existing color vars via `var()` — no new hex values needed
- [ ] Column vars (`--sd-col-*`) need new hex values per theme (see mapping above for default theme, use appropriate values for light/mono/hc)

### Custom Hook (useKanban.ts)
```typescript
export function useKanban() {
  const [items, setItems] = useState<KanbanItem[]>([]);
  const [columns, setColumns] = useState<Column[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch items from /api/kanban/items
  const fetchItems = async (filters?: FilterParams) => { ... };

  // Move item to column
  const moveItem = async (itemId: string, toColumn: string) => {
    await fetch('/api/kanban/move', { ... });
    await fetchItems(); // refetch
  };

  // Fetch columns from /api/kanban/columns
  const fetchColumns = async () => { ... };

  useEffect(() => {
    fetchItems();
    fetchColumns();
  }, []);

  return { items, columns, loading, error, fetchItems, moveItem };
}
```

### Adapter (kanbanAdapter.tsx)
- [ ] Register as `appType: 'kanban'`
- [ ] No special relay_bus subscriptions (read-only for now)
- [ ] Future: subscribe to `KANBAN_ITEM_UPDATED` events from sync engine

### Types (types.ts)
```typescript
export interface KanbanItem {
  id: string;
  type: 'work' | 'bug';
  title: string;
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  category?: string;
  column: string;
  stage?: string;
  stage_status?: string;
  assigned_to?: string | null;
  feature_id?: string | null;
  notes?: string;
  tags?: string[];
  graduated: boolean;
  created_at: string;
}

export interface Column {
  id: string;
  label: string;
  color: string;
  icon: string;
}

export interface FilterParams {
  types?: Set<string>;
  priorities?: Set<string>;
  query?: string;
  showGraduated?: boolean;
}
```

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Empty state (no items) renders correctly
  - Network error shows error message
  - Drag-drop to invalid column is rejected
  - Mobile move sheet dismisses on background tap
  - Filtering by multiple criteria works (AND logic)
  - Search query matches title, id, notes, tags
  - Settings sheet add/rename/reorder/delete columns
  - Graduated items show ✓ badge
- [ ] Test coverage:
  - `test_kanban_render_empty()`
  - `test_kanban_fetch_items()`
  - `test_kanban_move_item()`
  - `test_kanban_filters()`
  - `test_kanban_search()`
  - `test_kanban_settings_sheet()`
  - `test_kanban_mobile_move_sheet()`
  - `test_kanban_drag_drop()`
  - `test_kanban_graduated_badge()`
  - `test_kanban_css_variables()` — no hardcoded colors
  - ~15 tests total

## Constraints
- No file over 500 lines (split into components if needed)
- CSS: `var(--sd-*)` only — NO hardcoded colors
- No stubs — every component fully implemented
- Follow primitive patterns in `browser/src/primitives/`
- Use TypeScript strict mode
- Mobile-first responsive design (breakpoint: 700px)

## Dependencies
- **DEPENDS ON:** TASK-045 (API routes must exist)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260313-TASK-046-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
