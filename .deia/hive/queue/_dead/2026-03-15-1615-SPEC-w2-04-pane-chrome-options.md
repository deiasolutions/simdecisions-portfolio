# SPEC: Pane chrome options — pin, collapse, configurable close

## Priority
P0.74999

## Model Assignment
sonnet

## Objective
Add EGG-configurable pane chrome options to the shell primitive. Three new per-pane options:
- `chromeClose` (boolean) — show/hide close X button on pane header
- `chromePin` (boolean) — show pin toggle button; when pinned, pane stays visible and sibling pane collapses
- `chromeCollapsible` (boolean) — pane can collapse to a thin vertical icon strip (~34px wide) with an expand button

These options are declared per-pane in the EGG layout config and read by the shell pane renderer.

## Backlog Reference
BL-151 (supersedes BL-024 and BL-025)

## Acceptance Criteria
- [ ] EGG schema supports `chromeClose`, `chromePin`, `chromeCollapsible` per pane
- [ ] eggInflater reads and passes chrome options to shell panes
- [ ] PaneChrome component renders optional close X, pin toggle, collapse toggle
- [ ] Pin toggle: when active, sibling pane collapses; pane gets full width
- [ ] Collapse: pane shrinks to ~34px vertical icon strip with expand button
- [ ] Collapsed strip shows pane icon (from EGG config) and expand arrow
- [ ] Expand button restores pane to previous size
- [ ] All chrome buttons use `var(--sd-*)` CSS variables only
- [ ] Tests written and passing (TDD)
- [ ] Existing browser tests still pass

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1615-SPEC-w2-04-pane-chrome-options", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1615-SPEC-w2-04-pane-chrome-options", "files": ["path/to/file1.py", "path/to/file2.py"]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.

## Key Files (likely touched)
- `browser/src/shell/components/Shell.tsx` — pane rendering
- `browser/src/shell/components/shell.css` — pane chrome styles
- `browser/src/shell/eggToShell.ts` — EGG layout → shell config
- `browser/src/eggs/eggInflater.ts` — EGG inflation
- `docs/specs/SPEC-EGG-SCHEMA-v1.md` — schema docs
- New: `browser/src/shell/components/PaneChrome.tsx`
- New: `browser/src/shell/components/__tests__/PaneChrome.test.tsx`
