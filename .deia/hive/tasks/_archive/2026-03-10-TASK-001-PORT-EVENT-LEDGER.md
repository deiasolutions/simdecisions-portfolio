# TASK-001: Port Event Ledger to shiftcenter repo

## Objective

Port the Event Ledger (ADR-001) from the old platform repo to `hivenode/ledger/` in the shiftcenter repo. This is the first code in the new repo. Every subsequent service emits to it.

## Context

The Event Ledger is an append-only event log with a 14-column SQLite schema. It was built as TASK-009 in the old repo with 42 passing tests. The code lives at:
- **Old location:** `platform/src/simdecisions/runtime/ledger.py` (writer + schema)
- **Old location:** `platform/src/simdecisions/runtime/cost_tracking.py` (aggregation)
- **Old tests:** `platform/tests/ledger/` (42 tests)

You are porting this to the NEW shiftcenter repo. The new repo is a fresh monorepo. You are writing the first Python code in it.

## Source Schema (ADR-001)

```sql
CREATE TABLE events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
    event_type          TEXT NOT NULL,
    actor               TEXT NOT NULL,
    target              TEXT,
    domain              TEXT,
    signal_type         TEXT CHECK(signal_type IN ('gravity','light','internal')),
    oracle_tier         INTEGER CHECK(oracle_tier BETWEEN 0 AND 4),
    random_seed         INTEGER,
    completion_promise  TEXT,
    verification_method TEXT,
    payload_json        TEXT,
    cost_tokens         INTEGER,
    cost_usd            REAL,
    cost_carbon         REAL
);
```

Indexes on: event_type, actor, domain, timestamp, signal_type, oracle_tier.

Universal entity ID format: `{type}:{id}` (e.g., `agent:BEE-001`, `human:dave`, `system:gate-check`).

## Deliverables

- [ ] `hivenode/ledger/__init__.py` — package init
- [ ] `hivenode/ledger/schema.py` — SQLite schema creation, index creation, WAL mode
- [ ] `hivenode/ledger/writer.py` — append-only write interface (the `ledger_writer` invariant service)
- [ ] `hivenode/ledger/reader.py` — query interface (by event_type, actor, domain, time range)
- [ ] `hivenode/ledger/aggregation.py` — cost tracking aggregation (by task, by actor, by flight/sprint)
- [ ] `hivenode/ledger/export.py` — JSON and CSV export with date filtering
- [ ] `tests/hivenode/ledger/test_schema.py` — schema creation, WAL mode, indexes
- [ ] `tests/hivenode/ledger/test_writer.py` — write events, hash chaining, universal entity IDs
- [ ] `tests/hivenode/ledger/test_reader.py` — query by type, actor, domain, time range
- [ ] `tests/hivenode/ledger/test_aggregation.py` — cost rollups by task/actor/sprint
- [ ] `tests/hivenode/ledger/test_export.py` — JSON/CSV export, date filtering
- [ ] `hivenode/__init__.py` — package init
- [ ] `pyproject.toml` — Python project config (if not already present)
- [ ] `pytest.ini` — pytest config (if not already present)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 40 tests (matching old repo coverage)
- [ ] Edge cases: empty ledger queries, invalid entity IDs, concurrent writes (WAL mode), large payload_json, cost_carbon = 0.0 vs None

## Constraints

- Python 3.13
- SQLite only (no PostgreSQL yet — that's a future task)
- No file over 500 lines
- No external dependencies beyond stdlib + pytest
- Hash chaining: each event's hash includes the previous event's hash (tamper-evident)
- Every write returns the event ID
- WAL mode enabled by default for concurrent read access
- All timestamps in ISO 8601 UTC

## What NOT to Port

- Do NOT port the FastAPI routes (those come later when the API layer is built)
- Do NOT port the PostgreSQL cloud sync (future task)
- Do NOT port the keeper integration (future task)
- Do NOT create any frontend code

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-001-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- pytest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
