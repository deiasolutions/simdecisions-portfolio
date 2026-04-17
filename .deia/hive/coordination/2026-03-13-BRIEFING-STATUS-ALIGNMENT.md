# BRIEFING: Status System Alignment

**Date:** 2026-03-13
**From:** Q33NR
**For:** Q33N (to break into tasks)
**Priority:** P1 — prerequisite for kanban pane, progress pane, and PM dashboard

---

## Objective

Unify four separate status tracking systems into one coherent model so that:
1. Backlog items (BL-xxx) and bugs (BUG-xxx) can appear on the kanban board
2. Items in `in_progress` track which dev cycle stage they're in
3. Features (FE-xxx) that graduate from the pipeline show in `done`
4. The progress/Gantt pane can read stage timestamps from the same source
5. HiveNode API routes can serve this data to both kanban and progress panes

---

## The Four Systems Today

### 1. Kanban Columns (kanban-pane-v03.jsx)
```
icebox → backlog → in_progress → review → done
```
- Represents workflow state
- Currently mock data only — not connected to any DB
- Cards have: id, type (work/bug), title, priority, column, notes, tags

### 2. Dev Cycle Stages (progress-pane-v01.jsx)
```
SPEC → IR → VAL → BUILD → TEST
```
- Each stage has status: `done | active | pending | failed | blocked`
- Each stage has start/end timestamps
- Represents which development phase an item is in
- Currently mock data only — timestamps would come from ledger.db

### 3. Feature Inventory (inventory.py → feature-inventory.db)
```
features: BUILT | SPECCED | BROKEN | REMOVED
backlog:  (no status column — just id, title, category, priority, source, notes)
bugs:     OPEN | ASSIGNED | FIXED | WONTFIX
```
- The `backlog` table has NO column assignment and NO stage tracking
- Features only track final build state, not pipeline progress
- No relationship between backlog items and features

### 4. DEIA Task Lifecycle (.deia/processes/)
```
queue → claimed → buzz → archive
```
- Tracks dispatch state of task files, not development progress
- Lives in file system (task files), not DB

---

## Proposed Unified Model

### Schema Changes to `feature-inventory.db`

**Add to `backlog` table:**
```sql
ALTER TABLE backlog ADD COLUMN kanban_column TEXT NOT NULL DEFAULT 'backlog';
ALTER TABLE backlog ADD COLUMN stage TEXT DEFAULT NULL;
ALTER TABLE backlog ADD COLUMN stage_status TEXT DEFAULT NULL;
ALTER TABLE backlog ADD COLUMN assigned_to TEXT DEFAULT NULL;
ALTER TABLE backlog ADD COLUMN feature_id TEXT DEFAULT NULL;
```

**New `stage_log` table** (append-only, feeds progress/Gantt pane):
```sql
CREATE TABLE stage_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id     TEXT NOT NULL,          -- BL-xxx or BUG-xxx
    item_type   TEXT NOT NULL,          -- 'backlog' or 'bug'
    stage       TEXT NOT NULL,          -- SPEC, IR, VAL, BUILD, TEST
    status      TEXT NOT NULL,          -- done, active, pending, failed, blocked
    started_at  TEXT,                   -- ISO timestamp
    ended_at    TEXT,                   -- ISO timestamp (null if active)
    notes       TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_stage_item ON stage_log(item_id);
```

### Status Mapping

| Kanban Column | When | Stage |
|---------------|------|-------|
| `icebox` | Item exists but not prioritized | No stages |
| `backlog` | Prioritized, not started | No stages yet |
| `in_progress` | Active development | SPEC/IR/VAL/BUILD/TEST (one active) |
| `review` | Code complete, awaiting verification | TEST stage active or done |
| `done` | Graduated to feature inventory | All stages done, feature_id set |

### Graduation Flow

```
BL-xxx in backlog (kanban_column='backlog')
  → moves to in_progress, stage=SPEC
  → SPEC done → stage=IR (or skip for bugs)
  → IR done → stage=VAL
  → VAL done → stage=BUILD
  → BUILD done → stage=TEST, kanban_column='review'
  → TEST done → kanban_column='done'
  → inventory.py add --id FE-xxx ... → feature_id='FE-xxx'
  → Item graduated, visible in done column with ✓
```

### Inventory CLI Changes

```bash
# Move item to kanban column
python _tools/inventory.py backlog move BL-097 --column in_progress

# Set dev cycle stage
python _tools/inventory.py backlog stage BL-097 --stage BUILD --status active

# Complete a stage (auto-timestamps)
python _tools/inventory.py backlog stage BL-097 --stage BUILD --status done

# Graduate to feature
python _tools/inventory.py backlog graduate BL-097 --feature-id FE-051
```

### HiveNode API Routes (prerequisite: BL-010)

```
GET  /api/kanban/items           → all backlog + bug items with column assignment
POST /api/kanban/move            → move item to column
GET  /api/kanban/columns         → column definitions (customizable per user)
POST /api/kanban/columns         → add/rename/reorder columns

GET  /api/progress/items         → items with stage_log data
GET  /api/progress/stages/:id    → stage history for one item
POST /api/progress/stage         → update stage status
```

---

## Task Breakdown (for Q33N)

### TASK-A: Schema migration + inventory CLI (BEE, Sonnet)
- Add `kanban_column`, `stage`, `stage_status`, `assigned_to`, `feature_id` to backlog table
- Create `stage_log` table
- Add CLI subcommands: `backlog move`, `backlog stage`, `backlog graduate`
- Migrate existing 97 backlog items: all start in `backlog` column
- Tests: schema validation, move operations, stage transitions, graduation flow
- ~15 tests

### TASK-B: HiveNode kanban + progress API routes (BEE, Sonnet)
- GET/POST routes for kanban items, columns, moves
- GET/POST routes for progress stages
- Read from feature-inventory.db
- Tests: route handlers, validation, error cases
- ~20 tests
- **Depends on:** TASK-A (schema must exist first)

### TASK-C: Kanban pane primitive (BEE, Sonnet)
- Port kanban-pane-v03.jsx design to real React primitive
- Replace mock data with HiveNode API calls
- Adapter pattern (like terminal, drawing-canvas)
- Register as appType `kanban`
- CSS: all var(--sd-*), no hardcoded colors
- Tests: rendering, filtering, column operations, drag-drop
- ~15 tests
- **Depends on:** TASK-B (API routes must exist)

### TASK-D: Progress pane primitive (BEE, Sonnet)
- Port progress-pane-v01.jsx design to real React primitive
- Replace mock data with HiveNode API calls
- Adapter pattern, register as appType `progress`
- CSS: all var(--sd-*)
- Tests: rendering, filtering, stage display, timeline
- ~10 tests
- **Depends on:** TASK-B (API routes must exist)

---

## Dependency Chain

```
TASK-A (schema + CLI)
  ↓
TASK-B (API routes)
  ↓
TASK-C (kanban pane)  ←  can run parallel with TASK-D
TASK-D (progress pane)
```

---

## Existing Backlog Items This Subsumes or Blocks

| BL ID | Title | Relationship |
|-------|-------|-------------|
| BL-010 | Kanban pane HiveNode API routes | **Subsumed by TASK-B** |
| BL-071 | Kanban pane primitive | **Subsumed by TASK-C** |
| BL-083 | PM Dashboard Auto-Rollup | **Blocked by this work** — needs stage data |
| BL-011 | Progress/Gantt pane prototype | **Subsumed by TASK-D** |

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\kanban-pane-v03.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\progress-pane-v01.jsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\` (existing route patterns)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` (adapter registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\appRegistry.ts`

## Model Assignment

All tasks: **Sonnet** (medium complexity, established patterns)
