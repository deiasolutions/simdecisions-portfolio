# RCA-001: Backlog Database Wipe — 2026-03-13

**Date:** 2026-03-13
**Severity:** Data loss (recovered)
**Author:** Q33NR (Claude Opus) × Q88N (Dave)
**Status:** RESOLVED — root cause identified, data recovered

---

## 1. What Happened

On 2026-03-13, the backlog table in `docs/feature-inventory.db` (SQLite) was found empty
twice during a Q33NR session. The first wipe lost ~118 rows. After recovery, the table was
wiped a second time within minutes. Features table (55→57 rows) survived both wipes. Bugs
table was partially lost.

---

## 2. Timeline

| Time (approx) | Event |
|----------------|-------|
| ~13:00 | Q33NR session begins. Backlog has ~95 items. |
| 13:00–13:30 | Q33NR adds BL-087 through BL-096 (files54), BL-111 through BL-117 (files55). All confirmed via CLI output. |
| 13:31 | Q33NR runs `inventory.py export-md`. Markdown export succeeds with all 118 items. |
| ~13:43 | Q33NR queries backlog — table is empty. DB last-modified timestamp: 13:43. |
| ~13:45 | Q33NR runs recovery script from markdown. 118 items restored. |
| ~14:00 | BEE-SONNET session (separate Claude instance) commits `e17195e` — TASK-042 through TASK-049. This commit includes TASK-044 which refactored `_tools/inventory.py` into `inventory.py` + `inventory_db.py`. |
| ~14:07 | Q33NR queries backlog again — table is empty a second time. DB last-modified: 14:07. Features now at 57 (up from 55 — bee added 2). |
| ~14:15 | Bees stopped. Q33NR runs second recovery. 103 items restored from git history + source files. |

---

## 3. Root Cause

**Concurrent SQLite writes from two Claude sessions on a OneDrive-synced file.**

### The Mechanism

1. The SQLite database (`docs/feature-inventory.db`) is stored on OneDrive.
2. SQLite uses WAL (Write-Ahead Logging) mode. WAL creates a `-wal` journal file alongside
   the main `.db` file.
3. Two Claude Code sessions (Q33NR and BEE-SONNET) were running simultaneously, both
   writing to the same database file.
4. OneDrive syncs individual files independently. When Session B (BEE-SONNET) wrote to the
   database and synced, OneDrive replaced Session A's (Q33NR's) version of the `.db` file
   with Session B's version. Session B's version did not contain Session A's writes because
   Session B had loaded its copy of the database before Session A made its changes.
5. The WAL file from Session A was orphaned — it referenced transactions against a database
   state that no longer existed on disk.
6. On next connect, SQLite saw a clean database (Session B's version) with no pending WAL
   transactions. Session A's backlog inserts were gone.

### Why Features Survived

Session B (BEE-SONNET) also wrote to the features table (added 2 new features). Its version
of the features table was a superset of Session A's. Session A had not added any features, so
no feature data was lost in the overwrite.

### Why Backlog Did Not Survive

Session B's copy of the database predated Session A's backlog inserts. When Session B's
database was synced over Session A's, all of Session A's backlog rows disappeared. Session B
had not read or written to the backlog table, so its version had whatever state existed before
Session A began working.

### Contributing Factor: TASK-044

TASK-044 (part of the BEE-SONNET batch) refactored `inventory.py` into two files and ran
schema migrations. This involved multiple database connections, reads, and writes — increasing
the window during which OneDrive could sync a stale version of the file.

---

## 4. Recovery

### Attempt 1 (failed — wiped again by ongoing bee session)
- Parsed `FEATURE-INVENTORY.md` (markdown export from 13:31) back into the database.
- Restored 118 items.
- Wiped again when bee session synced its copy.

### Attempt 2 (successful)
- Bees confirmed stopped.
- Extracted pre-bee-commit markdown from git: `git show e17195e^:docs/FEATURE-INVENTORY.md`
- Parsed 95 rows from git history (old format: `| ID | P | Category | Title | Source |`).
- Re-added 10 items from files54 source (`BACKLOG-ENTRIES-2026-03-13-FILES54.md`).
- Re-added 7 items from files55 source (`BACKLOG-ENTRIES-2026-03-13-FILES55.md`).
- Added BL-118 from bee recall file.
- Restored icebox status for BL-011, BL-024, BL-025.
- Restored 3 bugs.
- Final: 104 backlog items, 57 features, 3 bugs.

### Data permanently lost
- **Notes field** for the original 95 items from git. The pre-bee markdown format
  (`| ID | P | Category | Title | Source |`) did not include the notes column. Notes added
  during the Q33NR session (files54/files55 entries, icebox annotations) were re-entered
  from source files. Notes on older items (BL-001 through BL-074) that existed before this
  session are gone from the DB — they may exist in earlier markdown exports or git history.

---

## 5. Prevention

### Immediate
- Created `docs/feature-inventory.db.bak` as a snapshot after recovery.

### Recommended

| # | Action | Effort |
|---|--------|--------|
| 1 | **Add `import-backlog-md` command to inventory.py** that can rebuild the backlog table from the markdown export. Makes recovery a one-liner instead of a custom script. | S |
| 2 | **Run `export-md` after every batch of DB writes.** The markdown file is tracked in git and survives OneDrive sync issues. It is the durable backup. | Process |
| 3 | **Move the `.db` file out of OneDrive** to a local-only path (e.g., `.deia/local/`). Reference it via environment variable. OneDrive cannot corrupt what it cannot sync. | M |
| 4 | **Never run concurrent sessions that write to the same SQLite DB on OneDrive.** If bees need DB access, route through a single coordinator or use hivenode API instead of direct SQLite. | Process |
| 5 | **Add a pre-write integrity check** to `_connect()`: on connect, verify the backlog table is not unexpectedly empty. If it was non-empty last export but is now empty, refuse to write and warn. | S |

---

## 6. Lessons

- SQLite on OneDrive is not safe for concurrent writes. WAL mode does not help when the
  underlying filesystem silently replaces files.
- The markdown export (`FEATURE-INVENTORY.md`) is the true backup, not the `.db` file.
  Always export after writes. Always commit after export.
- Multiple Claude Code sessions writing to the same file is a race condition. The hive
  dispatch system should treat the inventory DB as a shared resource with exclusive access.

---

*Filed by Q33NR — 2026-03-13*
