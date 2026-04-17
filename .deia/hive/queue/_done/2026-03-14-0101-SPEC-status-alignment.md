# SPEC: BL-110 Status System Alignment

## Priority
P1

## Objective
Unify all inventory statuses across the platform to a single canonical set: backlog, queued, in_progress, review, done, blocked, deferred, cancelled.

## Context
The feature inventory CLI (`_tools/inventory.py`) and database (`docs/feature-inventory.db`) currently use inconsistent status values across features, bugs, and backlog items. Some use "complete", others "done", others "shipped". This spec standardizes everything.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` — CLI tool
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\feature-inventory.db` — SQLite DB (read schema only, do NOT modify data without backup)

## Acceptance Criteria
- [ ] inventory.py validates status values against the canonical set: backlog, queued, in_progress, review, done, blocked, deferred, cancelled
- [ ] Invalid status values are rejected with a clear error message listing valid options
- [ ] `inventory.py add` accepts `--status` flag with validation
- [ ] `inventory.py update` (if it exists) validates status on update
- [ ] `inventory.py stats` groups by canonical statuses
- [ ] `inventory.py export-md` uses canonical statuses in the markdown output
- [ ] A migration function normalizes existing DB entries: "complete"→"done", "shipped"→"done", "open"→"backlog", "pending"→"queued", "wip"→"in_progress"
- [ ] Migration creates a backup before modifying (`docs/feature-inventory.db.bak`)
- [ ] 8+ tests covering validation, migration, and stats grouping
- [ ] WARNING: The backlog DB was recently wiped. Before ANY DB modification, verify item count. If count < 50, STOP and report — do NOT proceed with migration.

## Model Assignment
haiku

## Constraints
- Do NOT delete or modify existing DB data without creating a backup first
- If the DB has fewer than 50 backlog items, STOP and report without modifying
- Migration is idempotent — running it twice produces the same result
- No file over 500 lines
