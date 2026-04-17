# TASK-BL110: Status System Alignment

## Objective

Align the build status system between hivenode backend (build_monitor.py) and the frontend kanban/build-monitor UI so that status values are consistent, transitions are valid, and the UI reflects actual build state.

## Context

The build monitor (`hivenode/routes/build_monitor.py`) tracks task lifecycle states (pending, claimed, running, done, failed, etc.). The kanban pane and build monitor UI need to display these states consistently. Currently there may be mismatches between backend status values and what the frontend expects/displays.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (backend state machine)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor_liveness.py` (liveness ping)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\useKanban.ts` (frontend state display)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx` (kanban rendering)

## Files You May Modify

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — Add status enum/constants if not present
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\useKanban.ts` — Align status mapping
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_state_transition.py` — Add alignment tests

## Files You Must NOT Modify

- `hivenode/routes/build_monitor_liveness.py`
- `hivenode/routes/build_monitor_claims.py`
- `hivenode/routes/build_monitor_slots.py`
- Any file in `engine/`
- Any adapter files
- Any shell files

## Deliverables

- [ ] Define a shared status enum/constants (backend-side) with all valid states
- [ ] Ensure frontend kanban maps ALL backend states to display values
- [ ] Ensure state transitions are validated (no invalid jumps)
- [ ] Add status color mapping in frontend (using `var(--sd-*)` CSS variables)
- [ ] Tests verifying status alignment between backend and frontend expectations

## Build Verification

```bash
python -m pytest tests/hivenode/routes/test_build_monitor_state_transition.py -q
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/kanban-pane --reporter=verbose
```

## Minimum Tests

8 tests (status enum coverage, transition validation, frontend mapping)

## Model

sonnet

## Response Template

Use the 8-section response template from BOOT.md.

## Rules

- No stubs — every function complete
- No hardcoded colors — use `var(--sd-*)` only
- Max 500 lines per file
- TDD: write tests first
