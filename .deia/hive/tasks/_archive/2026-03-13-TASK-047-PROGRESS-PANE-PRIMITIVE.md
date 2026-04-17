# TASK-047: Progress Pane Primitive (React)

## Objective
Port progress-pane-v01.jsx design to production React primitive. Replaces mock data with HiveNode API calls. Register as appType `progress`. Shows dev cycle stage timeline (Gantt chart) for backlog items + bugs.

## Context
This primitive visualizes the build pipeline progress for backlog items. It shows which items are in which dev cycle stage (SPEC → IR → VAL → BUILD → TEST), with start/end timestamps displayed as a Gantt timeline. Users can:
- View all items with stage progress bars (desktop: Gantt chart, mobile: card-based stage track)
- Filter by status (all / active / failed)
- See time spent in each stage + overall progress (N/M stages done)
- Identify bottlenecks (items stuck in one stage, failures blocking progress)

**Design:** Follow the spec exactly — Gantt bars with stage labels, timeline axis with NOW marker, mobile horizontal stage track with durations.

**Dependencies:** TASK-045 (API routes) must complete first.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\progress-pane-v01.jsx` (full spec to port)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\index.ts` (primitive registration pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (custom hook pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` (adapter registration)

## Deliverables

### File Structure
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\progress-pane\index.ts` — export main component
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\progress-pane\ProgressPane.tsx` — main component (port of spec)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\progress-pane\useProgress.ts` — custom hook for API + state
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\progress-pane\types.ts` — TypeScript interfaces
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\progressAdapter.tsx` — adapter for shell integration
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` to register `progress` appType

### Component Structure (ProgressPane.tsx)
Port from spec with these changes:
- [ ] Replace `MOCK_ITEMS` with `useProgress()` hook that fetches from `/api/progress/items`
- [ ] Replace all hardcoded colors with CSS variables (`var(--sd-*)`)
- [ ] Time range calculation (`getTimeRange()`) uses real timestamps from API
- [ ] Filters (all/active/failed) send `?filter=` query param to API
- [ ] Desktop: Gantt chart with ItemRow component (horizontal bars)
- [ ] Mobile: MobileStageView component (vertical card layout)
- [ ] Timeline axis shows date ticks + NOW marker

**CSS Variables Mapping (use EXISTING vars from `browser/src/shell/shell-themes.css`):**
```css
/* These vars EXIST — use them directly */
DS.bg.root        → var(--sd-bg)
DS.bg.panel       → var(--sd-surface-alt)
DS.bg.card        → var(--sd-surface)
DS.bg.cardSel     → var(--sd-surface-hover)
DS.bg.border      → var(--sd-border)
DS.text.pri       → var(--sd-text-primary)
DS.text.sec       → var(--sd-text-secondary)
DS.text.dim       → var(--sd-text-muted)           /* --sd-text-dim does NOT exist */
DS.text.mute      → var(--sd-text-muted)
DS.accent         → var(--sd-accent)
```

**These vars are added by TASK-046 (kanban pane) — reuse them:**
```css
DS.type.work.color   → var(--sd-type-work)
DS.type.bug.color    → var(--sd-type-bug)
DS.pri.P0.color      → var(--sd-pri-p0)
DS.pri.P1.color      → var(--sd-pri-p1)
DS.pri.P2.color      → var(--sd-pri-p2)
DS.pri.P3.color      → var(--sd-pri-p3)
```

**NEW stage CSS variables — MUST be added to `shell-themes.css`:**

Add these to the `.hhp-root` block (and corresponding values in each theme variant):

```css
/* Dev cycle stage colors */
--sd-stage-spec:    #4a90d9;    /* depth: same, light: #2a70b9, mono: #999, hc: #44aaff */
--sd-stage-ir:      #a07cdc;    /* depth: same, light: #7b5cb6, mono: #aaa, hc: #cc88ff */
--sd-stage-val:     #e89b3f;    /* depth: same, light: #c57b1f, mono: #bbb, hc: #ff8800 */
--sd-stage-build:   #3fb8a9;    /* depth: same, light: #1f9889, mono: #ccc, hc: #00ff88 */
--sd-stage-test:    #22c55e;    /* depth: same, light: #16a34a, mono: #ddd, hc: #00ff44 */
```

Map spec names to CSS:
```css
DS.stage.SPEC.color  → var(--sd-stage-spec)
DS.stage.IR.color    → var(--sd-stage-ir)
DS.stage.VAL.color   → var(--sd-stage-val)
DS.stage.BUILD.color → var(--sd-stage-build)
DS.stage.TEST.color  → var(--sd-stage-test)
```

### Theme Variables (shell-themes.css)
- [ ] Add the 5 new stage CSS variables listed above to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
- [ ] Add to ALL 5 theme blocks: `.hhp-root`, `depth`, `light`, `monochrome`, `high-contrast`
- [ ] Use the hex values specified in the mapping above for each theme
- [ ] **NOTE:** TASK-046 adds `--sd-type-*` and `--sd-pri-*` vars. If TASK-046 runs first, those will exist. If not, add them here too.

### Custom Hook (useProgress.ts)
```typescript
export function useProgress() {
  const [items, setItems] = useState<ProgressItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch items from /api/progress/items
  const fetchItems = async (filter?: 'all' | 'active' | 'failed' | 'done') => {
    const params = filter ? `?filter=${filter}` : '';
    const res = await fetch(`/api/progress/items${params}`);
    const data = await res.json();
    setItems(data.items);
  };

  // Fetch stage history for one item
  const fetchStageHistory = async (itemId: string) => {
    const res = await fetch(`/api/progress/stages/${itemId}`);
    return await res.json();
  };

  useEffect(() => {
    fetchItems('all');
  }, []);

  return { items, loading, error, fetchItems, fetchStageHistory };
}
```

### Adapter (progressAdapter.tsx)
- [ ] Register as `appType: 'progress'`
- [ ] No special relay_bus subscriptions (read-only for now)
- [ ] Future: subscribe to `STAGE_UPDATED` events from sync engine

### Types (types.ts)
```typescript
export interface ProgressItem {
  id: string;
  type: 'work' | 'bug';
  title: string;
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  stages: StageData[];
  notes?: string;
}

export interface StageData {
  stage: 'SPEC' | 'IR' | 'VAL' | 'BUILD' | 'TEST';
  status: 'done' | 'active' | 'pending' | 'failed' | 'blocked';
  started_at: string | null;
  ended_at: string | null;
  notes?: string | null;
}

export interface TimeRange {
  min: number;
  max: number;
  span: number;
}
```

### Gantt Bar Component
- [ ] `GanttBar` component renders horizontal bar positioned via `left` + `width` percentages
- [ ] Color + opacity based on status (done: 0.8, active: 1, failed: red, pending: no bar)
- [ ] Active stages pulse (CSS animation)
- [ ] Tooltip shows stage label, date range, duration
- [ ] If bar width < 3%, hide stage label (too small to read)

### Time Axis Component
- [ ] `TimeAxis` component renders date ticks (1 per day)
- [ ] NOW marker as vertical line + label
- [ ] Ticks positioned via percentage (`(timestamp - min) / span * 100%`)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Empty state (no items) renders correctly
  - Network error shows error message
  - Filter buttons update API query param
  - Timeline axis handles items spanning multiple weeks
  - NOW marker appears correctly in time range
  - Mobile stage track shows all 5 stages
  - Pending stages (no start time) render as empty
  - Failed stages show red + FAIL label
  - Active stages pulse animation
- [ ] Test coverage:
  - `test_progress_render_empty()`
  - `test_progress_fetch_items()`
  - `test_progress_filters()`
  - `test_progress_time_range()`
  - `test_progress_gantt_bars()`
  - `test_progress_time_axis()`
  - `test_progress_mobile_stage_view()`
  - `test_progress_css_variables()` — no hardcoded colors
  - ~10 tests total

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
  `.deia/hive/responses/20260313-TASK-047-RESPONSE.md`

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
