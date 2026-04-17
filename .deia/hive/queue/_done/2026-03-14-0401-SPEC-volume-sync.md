# SPEC: HIVENODE-E2E Wave 3 — Volume Sync Engine

## Priority
P1

## Objective
Build bidirectional sync between home:// and cloud:// volumes. Full context in `docs/specs/SPEC-HIVENODE-E2E-001.md` Section 6.

## Context
Bidirectional sync using content_hash comparison. Sync log in SQLite. Conflict resolution: last-write-wins with both versions preserved.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` — Section 6 (Volume Sync)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\` — existing sync directory
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py`

## Acceptance Criteria
- [ ] Sync log table in SQLite: path, content_hash, source_volume, target_volume, status, timestamps
- [ ] Compare content_hash to determine sync direction
- [ ] Conflict resolution: last-write-wins by timestamp, loser saved as `.conflict.<timestamp>.<ext>`
- [ ] Event Ledger logs: SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT
- [ ] Sync triggers: on file write, periodic (configurable interval), manual, on reconnect
- [ ] Exclusions: .git/, node_modules/, __pycache__/, patterns from sync_ignore
- [ ] 10+ tests including conflict scenarios
- [ ] No file over 500 lines

## Model Assignment
sonnet

## Constraints
- Depends on cloud storage adapter being functional
- Do NOT modify existing storage adapters
- Sync is bidirectional — neither volume is "primary"
