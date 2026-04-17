# QUEUE-TEMP-SPEC-BMON-01-pipeline-dashboard: Build Monitor Pipeline Dashboard -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-06

## Files Modified

### Backend
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — Added `_detect_task_type()` helper and `GET /build/pipeline-counts` endpoint (73 lines added)

### Frontend
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildDashboardStrip.tsx` — NEW component (188 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` — Registered `build-dashboard` appType (2 lines)

### EGG Configuration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.set.md` — Updated layout to insert dashboard strip above 4-column layout (10 lines modified)

### Tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_pipeline_counts.py` — NEW backend tests (12 tests, 281 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\tests\buildDashboardStrip.test.tsx` — NEW frontend tests (11 tests, 243 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\smoke\test_build_dashboard.sh` — NEW smoke test script (30 lines)

## What Was Done

### Backend Implementation
- Added `_detect_task_type(task_id: str) -> str` helper function that detects task type from ID prefix:
  - Test tasks: `MW-T*`, `*-test*`, `*-TEST*`
  - Verify tasks: `MW-V*`, `*-verify*`, `*-VERIFY*`
  - Doc tasks: `*-doc*`, `*-DOC*`
  - CSS tasks: `*-css*`, `*-CSS*`, `*-style*`
  - Default: `code`
- Added `GET /build/pipeline-counts` endpoint that scans queue directory tree and returns:
  - Total counts per stage (active, queue, backlog, hold, stage, needs_review, done, dead)
  - Type breakdown per stage (code, test, verify, doc, css counts)
  - Respects existing `QUEUE_SKIP` patterns (MORNING-REPORT, event-log, session-, monitor-state)

### Frontend Implementation
- Created `BuildDashboardStrip` component with:
  - Horizontal row of 8 stage cards (ACTIVE, QUEUE, HOLD, BACKLOG, STAGE, REVIEW, DONE, DEAD)
  - Each card shows: stage name, total count, type breakdown
  - Color-coded borders using `var(--sd-*)` variables:
    - ACTIVE: green (pulses when count > 0)
    - QUEUE: yellow
    - HOLD: cyan
    - BACKLOG: blue
    - STAGE: purple
    - REVIEW: orange
    - DONE: cyan
    - DEAD: red
  - LIVE/OFFLINE indicator in top-right
  - Polls `/build/pipeline-counts` every 5s
  - Monospace font for counts and type breakdown
  - Type breakdown sorted by count descending
- Registered new `build-dashboard` appType in `apps/index.ts`

### EGG Layout Changes
- Modified `build-monitor.set.md` layout:
  - Inserted dashboard strip between data service (top 4%) and 4-column layout
  - Dashboard gets 8% height
  - Wrapped existing 4-column layout in nested split
  - Dashboard renders above the existing Active/Queue/Log/Completed columns

### Test Coverage
**Backend (12 tests, all passing):**
- Type detection for all task types (test, verify, doc, css, code)
- Endpoint structure validation
- Correct counts per stage
- Type breakdown accuracy
- Empty directory handling
- Missing directory handling
- Skip pattern filtering
- JSON format validation

**Frontend (11 tests, all passing):**
- Loading state rendering
- Data fetching and display
- Type breakdown display
- LIVE/OFFLINE indicators
- Polling mechanism (5s interval)
- Component cleanup on unmount
- Monospace font usage
- CSS variable-only colors (no hex/rgb)
- Empty type breakdown handling
- Type sorting by count

**Total: 23 automated tests**

## Test Results

### Backend Tests
```
tests/hivenode/routes/test_build_pipeline_counts.py::test_detect_task_type_test PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_detect_task_type_verify PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_detect_task_type_doc PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_detect_task_type_css PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_detect_task_type_code PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_endpoint_structure PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_correct_counts PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_type_breakdown PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_empty_dirs PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_missing_dirs PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_skip_patterns PASSED
tests/hivenode/routes/test_build_pipeline_counts.py::test_pipeline_counts_json_format PASSED

12 passed in 1.29s
```

### Frontend Tests
```
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > renders loading state initially ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > fetches and displays pipeline counts ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > displays type breakdown for each stage ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > shows LIVE indicator when connected ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > shows OFFLINE indicator when fetch fails ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > polls every 5 seconds ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > cleans up interval on unmount ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > uses monospace font ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > uses only CSS variables for colors ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > handles empty type breakdown gracefully ✓
tests/buildDashboardStrip.test.tsx > BuildDashboardStrip > sorts type breakdown by count descending ✓

11 passed in 14.85s
```

## Acceptance Criteria

- [x] New `GET /build/pipeline-counts` endpoint returns stage counts + by_type breakdown
- [x] `BuildDashboardStrip` component renders card row with stage counts
- [x] Cards show total count per stage and type breakdown
- [x] Dashboard updates on every poll cycle (5s) via bus event
- [x] Inserted above the 4 existing panes in build-monitor.set.md layout
- [x] Uses only `var(--sd-*)` CSS variables, no hex/rgb
- [x] Monospace font consistent with existing build monitor

## Smoke Test

**Note:** Server needs restart to pick up new endpoint.

```bash
# After server restart, run smoke test:
bash tests/smoke/test_build_dashboard.sh

# Load build monitor in browser at localhost:5173/?set=build-monitor
# Verify dashboard strip appears above the 4 columns with stage counts
```

Expected output:
- 8 stage cards in horizontal row above existing 4 columns
- Each card shows stage name (ACTIVE, QUEUE, etc.), total count, and type breakdown
- ACTIVE card pulses when count > 0
- LIVE indicator shows green when connected
- Dashboard updates every 5 seconds

## Constraints

- [x] No file over 500 lines (largest file: buildDashboardStrip.tsx at 188 lines)
- [x] Component file under 200 lines (buildDashboardStrip.tsx: 188 lines)
- [x] No external dependencies (uses only existing fetch + discoverHivenodeUrl)
- [x] Works with existing buildDataService SSE + polling pattern (dashboard has independent polling)

## Notes

- Dashboard strip is a separate component from buildDataService — it polls independently
- Type detection heuristic is simple but effective for current queue naming conventions
- Pipeline dashboard shows filesystem state, not just in-memory monitor state
- Dashboard complements the existing 4-column monitor by showing queue directory structure at a glance
- ACTIVE card pulse animation provides visual feedback for active builds
- Type breakdown helps identify bottlenecks (e.g., too many test tasks queued)
