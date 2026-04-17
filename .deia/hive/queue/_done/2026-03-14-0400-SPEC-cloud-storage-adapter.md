# SPEC: HIVENODE-E2E Wave 2 — Cloud Storage Adapter

## Priority
P1

## Objective
Wire the cloud:// volume adapter to Railway's storage so cloud:// reads and writes actually work. Full context in `docs/specs/SPEC-HIVENODE-E2E-001.md` Section 5.

## Context
The local hivenode calls the cloud hivenode's `/storage/*` routes over HTTPS for cloud:// operations. The cloud adapter is a client of the cloud hivenode.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` — Section 5 (Cloud Storage Adapter)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` — volume registry
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\` — existing adapters
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — hivenode config

## Acceptance Criteria
- [ ] CloudStorageAdapter class implements BaseStorageAdapter interface
- [ ] read(), write(), list(), stat(), delete() methods call cloud hivenode over HTTPS
- [ ] Authentication: ra96it JWT included in all requests
- [ ] Offline behavior: VOLUME_OFFLINE error when cloud is unreachable
- [ ] Write queue: writes queued in `~/.shiftcenter/sync_queue/` when offline
- [ ] Queue flushes when cloud comes back online
- [ ] Adapter registered in volume registry for `cloud://` scheme
- [ ] 10+ tests (mock cloud endpoint)
- [ ] No file over 500 lines

## Model Assignment
sonnet

## Constraints
- Cloud adapter is a CLIENT — it calls the remote hivenode's storage routes
- Do NOT modify existing home:// or local:// adapters
- Mock the cloud endpoint in tests (can't hit real Railway in CI)
