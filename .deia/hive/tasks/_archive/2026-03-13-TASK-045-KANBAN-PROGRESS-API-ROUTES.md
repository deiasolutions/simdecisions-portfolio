# TASK-045: Kanban + Progress API Routes (HiveNode)

## Objective
Add HiveNode FastAPI routes for kanban board management and progress/stage tracking. Reads from `feature-inventory.db` (backlog + stage_log tables). Enables kanban-pane and progress-pane primitives to read/write workflow state.

## Context
This task depends on TASK-044 (schema migration). The DB schema now supports:
- `backlog.kanban_column` — workflow state
- `backlog.stage` + `backlog.stage_status` — current dev cycle stage
- `stage_log` table — append-only timeline of stage transitions

**Auth:** All routes use `verify_jwt_or_local()` — local bypasses auth, cloud requires JWT.

**Files:** Follow existing route patterns in `hivenode/routes/` (FastAPI router, Pydantic schemas, auth dependency).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\health.py` (route structure example)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\ledger_routes.py` (DB access pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\auth\jwt.py` (auth helpers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` (DB schema + queries)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\kanban-pane-v03.jsx` (expected data shape)

## Deliverables

### File Structure
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\kanban_routes.py` (kanban board routes)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\progress_routes.py` (progress/stage routes)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` to include both routers

### Kanban Routes (`kanban_routes.py`)

**GET /api/kanban/items**
- Query params: `?type=work|bug&priority=P0|P1|P2|P3&column=icebox|backlog|...&graduated=true|false`
- Returns: List of backlog items + bugs with kanban metadata
  ```json
  {
    "items": [
      {
        "id": "BL-001",
        "type": "work",
        "title": "...",
        "priority": "P1",
        "category": "enhancement",
        "column": "in_progress",
        "stage": "BUILD",
        "stage_status": "active",
        "assigned_to": null,
        "feature_id": null,
        "notes": "...",
        "tags": [],
        "graduated": false,
        "created_at": "2026-03-10T12:00:00"
      }
    ]
  }
  ```
- Joins backlog + bugs (union query)
- Filters by query params
- Includes `graduated` flag (true if `feature_id` is not null)

**POST /api/kanban/move**
- Body: `{ "item_id": "BL-001", "to_column": "review" }`
- Updates `backlog.kanban_column` or `bugs.kanban_column` (add column to bugs table if needed)
- Validates column is one of 5 allowed values
- Returns: `{ "success": true, "item_id": "BL-001", "column": "review" }`

**GET /api/kanban/columns**
- Returns: Column definitions (currently hardcoded, future: user-customizable)
  ```json
  {
    "columns": [
      { "id": "icebox", "label": "Icebox", "color": "#6b7a8d", "icon": "❄" },
      { "id": "backlog", "label": "Backlog", "color": "#e89b3f", "icon": "▫" },
      { "id": "in_progress", "label": "In Progress", "color": "#4a90d9", "icon": "▸" },
      { "id": "review", "label": "Review", "color": "#a07cdc", "icon": "◎" },
      { "id": "done", "label": "Done", "color": "#3fb8a9", "icon": "✓" }
    ]
  }
  ```

**POST /api/kanban/columns** (future: user-customizable columns)
- Body: `{ "columns": [...] }` — save custom column config
- For now: return `501 Not Implemented` with message "Custom columns not yet supported"

### Progress Routes (`progress_routes.py`)

**GET /api/progress/items**
- Query params: `?filter=all|active|failed|done`
- Returns: Backlog items with stage timeline data
  ```json
  {
    "items": [
      {
        "id": "BL-001",
        "type": "work",
        "title": "...",
        "priority": "P1",
        "stages": [
          {
            "stage": "SPEC",
            "status": "done",
            "started_at": "2026-03-08T10:00:00",
            "ended_at": "2026-03-09T14:00:00",
            "notes": null
          },
          {
            "stage": "BUILD",
            "status": "active",
            "started_at": "2026-03-09T14:30:00",
            "ended_at": null,
            "notes": null
          },
          {
            "stage": "TEST",
            "status": "pending",
            "started_at": null,
            "ended_at": null,
            "notes": null
          }
        ],
        "notes": "..."
      }
    ]
  }
  ```
- Joins `backlog` with `stage_log` (LEFT JOIN, group by item_id)
- Filters by `filter` param:
  - `active` — items with at least one stage.status='active'
  - `failed` — items with at least one stage.status='failed'
  - `done` — items where all stages.status='done'
  - `all` — no filter

**GET /api/progress/stages/:item_id**
- Returns: Full stage history for one item (from `stage_log`)
  ```json
  {
    "item_id": "BL-001",
    "stages": [
      {
        "stage": "SPEC",
        "status": "done",
        "started_at": "2026-03-08T10:00:00",
        "ended_at": "2026-03-09T14:00:00",
        "notes": "Initial spec completed"
      }
    ]
  }
  ```
- Ordered by `created_at ASC`

**POST /api/progress/stage**
- Body: `{ "item_id": "BL-001", "stage": "BUILD", "status": "active", "notes": null }`
- Inserts row in `stage_log` with timestamp
- If `status='active'`, ends any previous active stage for same item (sets `ended_at`)
- Updates `backlog.stage` and `backlog.stage_status`
- Returns: `{ "success": true, "item_id": "BL-001", "stage": "BUILD", "status": "active" }`

### Shared Code
- [ ] Pydantic schemas for request/response validation
- [ ] Auth dependency: `verify_jwt_or_local` from `hivenode.auth.jwt`
- [ ] DB connection helper (similar to ledger_routes pattern)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - GET /api/kanban/items with no results returns empty array
  - POST /api/kanban/move with invalid column returns 400
  - GET /api/progress/items filters correctly (active/failed/done)
  - POST /api/progress/stage with status=active ends previous active stage
  - All routes reject requests without JWT in cloud mode
  - All routes accept requests in local mode (bypass auth)
- [ ] Test coverage:
  - `test_kanban_items_get()` — filters, graduated flag
  - `test_kanban_move()` — valid + invalid columns
  - `test_kanban_columns_get()` — returns 5 columns
  - `test_progress_items_get()` — filters, stage aggregation
  - `test_progress_stages_get()` — single item history
  - `test_progress_stage_post()` — stage transitions, auto-end active
  - `test_auth_local_bypass()` — local mode skips JWT
  - `test_auth_cloud_requires_jwt()` — cloud mode enforces JWT
  - ~20 tests total

## Constraints
- No file over 500 lines (split schemas into separate file if needed)
- CSS: N/A (no frontend code)
- No stubs — every route fully implemented
- Follow FastAPI route patterns in existing `hivenode/routes/` files
- All DB queries parameterized (no SQL injection)
- Return JSON with consistent error format: `{ "error": "message" }`

## Dependencies
- **BLOCKS:** TASK-046 (kanban-pane), TASK-047 (progress-pane) — both need these routes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260313-TASK-045-RESPONSE.md`

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
