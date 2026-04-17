# SPEC-HHPANES-003: Settings Backend Persistence

## Priority
P1

## Depends On
HHPANES-001, HHPANES-002

## Model Assignment
sonnet

## Objective

Persist settings changes to the hivenode backend so settings survive across devices and sessions. Currently settings are in-memory or localStorage only. Need round-trip to hivenode API for durable cross-device settings with offline fallback.

## Files to Read First

- browser/src/primitives/settings/settingsStore.ts
- browser/src/primitives/settings/types.ts
- hivenode/routes/__init__.py
- hivenode/main.py

## Acceptance Criteria

- [ ] Settings save triggers API call to hivenode backend
- [ ] API endpoint exists: POST /api/user/settings (or equivalent)
- [ ] API accepts partial updates (patch semantics, not full replace)
- [ ] Settings load on app init fetches from backend
- [ ] Offline fallback: localStorage cache used if backend unreachable, sync on reconnect
- [ ] Conflict resolution: server wins (last-write-wins)
- [ ] All existing settings tests still pass
- [ ] New tests cover save/load/offline round-trip

## Smoke Test

- [ ] Login, change a setting — confirm network request to backend
- [ ] Reload page — confirm setting persisted from backend
- [ ] Disconnect network, change setting, reconnect — confirm sync to backend

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- If storage_adapter service does not exist, stand it up for this use case
