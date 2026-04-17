# SPEC: Volume Sync home:// <-> cloud:// End-to-End

## Priority
P1

## Objective
Verify bidirectional sync between local hivenode (home://) and cloud hivenode (cloud://) works.

## Context
Files to read first:
- SPEC-HIVENODE-E2E-001.md Section 6 (Volume Sync)
- `hivenode/storage/sync/` (if it exists from overnight build)
- `hivenode/storage/adapters/`

## Acceptance Criteria
- [ ] On file write to home://, change queued for push to cloud://
- [ ] On file write to cloud://, change queued for push to home:// on next connect
- [ ] Periodic sync every 5 minutes (configurable)
- [ ] Manual sync via 8os sync CLI command
- [ ] On hivenode startup, pull changes from cloud since last sync
- [ ] Conflict resolution: last-write-wins, both versions preserved (.conflict file)
- [ ] sync_log.db tracks all sync operations
- [ ] Event Ledger logs SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT events
- [ ] Offline queue: writes to offline volume queued, flushed on reconnect
- [ ] 10+ tests including conflict scenarios

## Smoke Test
- [ ] Write file on local hivenode -> appears on cloud after sync
- [ ] Write file on cloud -> appears on local after sync
- [ ] Write same file on both before sync -> conflict file created, latest wins

## Depends On
- w3-06-cloud-adapter-e2e

## Model Assignment
sonnet
