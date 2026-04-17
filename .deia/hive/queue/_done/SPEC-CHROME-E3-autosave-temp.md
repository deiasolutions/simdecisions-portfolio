# CHROME-E3: Autosave to Temp Storage

## Objective
Implement autosave to temp storage (localStorage + cloud object storage). 30-60 second timer + structural change trigger. 7-day TTL. Hivenode cleanup job (runs on boot + every 24 hours). Browser-side localStorage cleanup on app load.

## Build Type
**New build** — No autosave mechanism exists. Both browser-side (autosave.ts) and backend (temp_cleanup.py) are new. localStorage and cloud save targets are new.

## Problem Analysis
The shell autosaves on a timer and on every structural layout change. Two targets: localStorage (immediate, survives refresh) and cloud (async, survives device loss). Each pane serializes its own content state. Temp files have a 7-day TTL. Hivenode cleans expired cloud temp files. Browser cleans expired localStorage entries on load.

## Files to Read First
- browser/src/shell/components/Shell.tsx
- browser/src/shell/types.ts
- docs/specs/ADR-SC-CHROME-001-v3.md

## Files to Modify
- browser/src/shell/autosave.ts — NEW: autosave logic (timer, structural trigger)
- browser/src/shell/__tests__/autosave.test.ts — NEW tests
- hivenode/routes/temp_cleanup.py — NEW: background cleanup job
- tests/hivenode/test_temp_cleanup.py — NEW tests

## Deliverables
- [ ] Autosave timer: 30-60 seconds, saves layout + per-pane content
- [ ] Structural change trigger: saves immediately on split/merge/dock/etc
- [ ] localStorage save: temp://eggs/{eggId}/{userId}/layout.json
- [ ] Cloud save: async via named volume cloud://
- [ ] 7-day TTL on all temp files
- [ ] Hivenode cleanup: runs on boot + every 24h, deletes expired temp files
- [ ] Browser cleanup: checks TTLs on app load, deletes expired localStorage

## Acceptance Criteria
- [ ] Layout autosaved to localStorage within 60 seconds of change
- [ ] Structural action triggers immediate save
- [ ] Temp file includes TTL timestamp
- [ ] Expired temp files cleaned by hivenode job
- [ ] Expired localStorage cleaned on app load

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/shell/__tests__/autosave.test.ts
- [ ] Test: timer fires autosave after interval
- [ ] Test: structural action triggers immediate save
- [ ] Test: saved data includes TTL timestamp
- [ ] Test: expired localStorage entries deleted on load
- [ ] Test file: tests/hivenode/test_temp_cleanup.py
- [ ] Test: cleanup job deletes files with expired TTL
- [ ] Test: cleanup job skips files with valid TTL
- [ ] All tests pass
- [ ] Minimum 7 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/__tests__/autosave — tests pass
- [ ] cd hivenode && python -m pytest tests/hivenode/test_temp_cleanup.py -v — tests pass

## Constraints
- No file over 500 lines
- No stubs
- localStorage saves must be synchronous (reliability)
- Cloud saves must be async (non-blocking)

## Depends On
- SPEC-CHROME-A6 (dirty tracking provides dirty flags)

## Model Assignment
sonnet

## Priority
P2
