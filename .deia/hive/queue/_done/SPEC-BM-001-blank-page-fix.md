## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-BM-001-blank-page-fix: Fix build-monitor set loading as blank page

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Loading `http://localhost:5173/?set=build-monitor` shows a completely blank page despite the set file having valid JSON layout, all appTypes registered in apps/index.ts (build-data-service, build-dashboard, tree-browser), and both backend and vite running. The set has `auth: required` but useEggInit.ts skips auth gating on localhost. Investigate why the page renders blank. Possible causes: 1) The deeply nested split layout (4 levels deep) fails to render, 2) The build-data-service or build-dashboard component throws an error on mount that crashes the React tree, 3) The eggToShell parser fails on the layout structure, 4) A CSS issue makes all panes 0 height. Check the browser console for errors, trace the set loading pipeline (useEggInit -> eggToShell -> ShellNodeRenderer), and fix the root cause.

## Files to Read First

- browser/sets/build-monitor.set.md
- browser/src/apps/index.ts
- browser/src/apps/buildMonitorAdapter.tsx
- browser/src/apps/buildDataService.tsx
- browser/src/apps/buildDashboardStrip.tsx
- browser/src/shell/useEggInit.ts
- browser/src/shell/eggToShell.ts
- browser/src/shell/components/ShellNodeRenderer.tsx

## Acceptance Criteria

- [ ] Loading `http://localhost:5173/?set=build-monitor` renders the 4-column build monitor layout
- [ ] The build-data-service pane connects to backend and starts receiving data
- [ ] The build-dashboard strip shows pipeline stage counts
- [ ] The 4 tree-browser panes (Active, Queue, Build Log, Completed) render with headers and search boxes
- [ ] No JavaScript errors in the browser console during page load
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)

## Smoke Test

- [ ] Open `http://localhost:5173/?set=build-monitor` — verify 4-column layout renders with headers visible
- [ ] Open browser DevTools console — verify no errors

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- Do not restructure the set layout unless the current structure is fundamentally incompatible with the shell renderer

## Triage History
- 2026-04-12T18:52:40.063857Z — requeued (empty output)
