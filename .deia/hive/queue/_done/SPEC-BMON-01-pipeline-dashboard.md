# SPEC: Build Monitor Pipeline Dashboard

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective
Add a compact dashboard strip to the build-monitor EGG that shows card-style counts of specs in each pipeline stage, broken down by type. This goes ABOVE the existing 4-column layout (active bees, queue, build log, completed).

## Design

### Dashboard Layout
A horizontal strip of cards, each showing:
- Stage name (e.g. "ACTIVE", "QUEUE", "BACKLOG", "DONE", "FAILED")
- Total count in that stage
- Breakdown by type (code, test, verify, spec, css, etc.)

### Data Source
The `buildDataService.tsx` already connects to `/build/status` and gets the full `BuildStatusResponse`. Extend it to:
1. Add a new bus event: `build:dashboard-updated`
2. Compute stage counts from the existing response fields:
   - ACTIVE: `data.active.length` (break down by model or task prefix)
   - QUEUE: `data.runner_queue.length`
   - FEEDER: `data.feeder_queue.length`
   - DONE: `data.completed.length`
   - FAILED: `data.failed.length`
3. Also scan the filesystem counts from a new endpoint (see below)

### New Endpoint: GET /build/pipeline-counts
Add to `build_monitor.py`. Scans the queue directory tree and returns counts:
```json
{
  "active": 5,
  "queue": 8,
  "backlog": 4,
  "hold": 4,
  "stage": 8,
  "needs_review": 4,
  "done": 356,
  "dead": 26,
  "by_type": {
    "active": {"code": 3, "test": 1, "verify": 1},
    "queue": {"code": 5, "test": 2, "doc": 1},
    "backlog": {"code": 2, "test": 1, "verify": 1}
  }
}
```

Type detection heuristic from task ID prefix:
- `MW-T*`, `*-test*`, `*-TEST*` → test
- `MW-V*`, `*-verify*`, `*-VERIFY*` → verify
- `*-doc*`, `*-DOC*` → doc
- `*-css*`, `*-CSS*`, `*-style*` → css
- Everything else → code

### Component: BuildDashboardStrip
New appType: `build-dashboard`. Register in appRegistry.

Renders a row of cards using `var(--sd-*)` colors:
- Each card: stage name, big number, small type breakdown below
- Active cards pulse with `var(--sd-green)`
- Failed cards use `var(--sd-red)`
- Queue/backlog use `var(--sd-yellow)`
- Done uses `var(--sd-cyan)`

### EGG Layout Change
Modify `build-monitor.set.md`: insert the dashboard strip between the data service (top 4%) and the 4-column layout. Dashboard gets ~8% height, columns get the rest.

## Key Files
- `browser/src/apps/buildDataService.tsx` — add dashboard bus event
- `browser/src/apps/buildDashboardStrip.tsx` — NEW component
- `browser/src/apps/index.ts` — register new appType
- `hivenode/routes/build_monitor.py` — new /build/pipeline-counts endpoint
- `eggs/build-monitor.set.md` — layout update

## Acceptance Criteria
- [ ] New `GET /build/pipeline-counts` endpoint returns stage counts + by_type breakdown
- [ ] `BuildDashboardStrip` component renders card row with stage counts
- [ ] Cards show total count per stage and type breakdown
- [ ] Dashboard updates on every poll cycle (5s) via bus event
- [ ] Inserted above the 4 existing panes in build-monitor.set.md layout
- [ ] Uses only `var(--sd-*)` CSS variables, no hex/rgb
- [ ] Monospace font consistent with existing build monitor

## Smoke Test
```bash
# Check new endpoint
curl -s http://127.0.0.1:8420/build/pipeline-counts | python -c "import sys,json; d=json.loads(sys.stdin.buffer.read().decode('utf-8')); print(d)"

# Load build monitor in browser at localhost:5173/?set=build-monitor
# Verify dashboard strip appears above the 4 columns with stage counts
```

## Constraints
- No file over 500 lines
- Component file under 200 lines (it's a display-only strip)
- No external dependencies
- Must work with existing buildDataService SSE + polling pattern
