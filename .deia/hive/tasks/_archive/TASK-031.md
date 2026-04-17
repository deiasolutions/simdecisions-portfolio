# TASK-031: Token Tracking Schema Migration (tokens up/down)

**Assigned to:** BEE-SONNET
**Model:** Sonnet
**Date:** 2026-03-12
**Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Section 10.1)
**Parent:** SPEC-HIVENODE-E2E-001 Wave 2

---

## Objective

Add `cost_tokens_up` and `cost_tokens_down` columns to the Event Ledger schema. Update LLM_CALL event emission to populate them. Update cost aggregation to report directional costs.

LLM vendors charge different rates for input (prompt) and output (completion) tokens — often 3-5x more for output. The Event Ledger must track these separately as first-class columns, not buried in payload JSON.

---

## Schema Migration (Section 10.1)

Add two new columns to the `events` table:

```sql
ALTER TABLE events ADD COLUMN cost_tokens_up INTEGER;    -- input/prompt tokens
ALTER TABLE events ADD COLUMN cost_tokens_down INTEGER;  -- output/completion tokens
```

The existing `cost_tokens` column remains as total (up + down) for backward compatibility.

---

## What to Change

### 1. `hivenode/ledger/schema.py`

**Add to CREATE TABLE:**
```python
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    actor TEXT,
    timestamp TEXT NOT NULL,
    payload TEXT,
    cost_usd REAL,
    cost_carbon_kg REAL,
    cost_tokens INTEGER,
    cost_tokens_up INTEGER,      # NEW
    cost_tokens_down INTEGER,    # NEW
    intent TEXT,
    parent_id INTEGER,
    session_id TEXT,
    content_hash TEXT,
    source TEXT
);
```

**Add migration function:**
```python
def migrate_schema(db_path: str):
    """Apply schema migrations to existing DBs."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if cost_tokens_up column exists
    cursor.execute("PRAGMA table_info(events)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'cost_tokens_up' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN cost_tokens_up INTEGER")

    if 'cost_tokens_down' not in columns:
        cursor.execute("ALTER TABLE events ADD COLUMN cost_tokens_down INTEGER")

    conn.commit()
    conn.close()
```

Call `migrate_schema()` on every DB connection init (in `__init__` or at startup).

### 2. `hivenode/ledger/writer.py`

**Update `write_event()` signature:**

```python
def write_event(
    event_type: str,
    actor: str = None,
    payload: dict = None,
    cost_usd: float = None,
    cost_carbon_kg: float = None,
    cost_tokens: int = None,
    cost_tokens_up: int = None,      # NEW
    cost_tokens_down: int = None,    # NEW
    intent: str = None,
    parent_id: int = None,
    session_id: str = None,
    content_hash: str = None,
    source: str = None,
) -> int:
    # Store cost_tokens_up and cost_tokens_down in INSERT
```

### 3. `hivenode/llm/cost.py`

**Update `emit_llm_event()` to pass directional tokens:**

Already has `input_tokens` and `output_tokens` internally. Pass them to `write_event()`:

```python
ledger_writer.write_event(
    event_type='LLM_CALL',
    actor=actor,
    payload={...},
    cost_usd=total_cost_usd,
    cost_carbon_kg=carbon_kg,
    cost_tokens=input_tokens + output_tokens,
    cost_tokens_up=input_tokens,       # NEW
    cost_tokens_down=output_tokens,    # NEW
    session_id=session_id,
)
```

### 4. `hivenode/ledger/aggregation.py`

**Update all aggregation functions to return directional data:**

```python
def get_total_cost(db_path: str) -> dict:
    # Query: SUM(cost_usd), SUM(cost_tokens), SUM(cost_tokens_up), SUM(cost_tokens_down)
    return {
        "usd": total_usd,
        "tokens": total_tokens,
        "tokens_up": total_tokens_up,      # NEW
        "tokens_down": total_tokens_down,  # NEW
        "carbon": total_carbon_kg,
    }

def aggregate_cost_by_model(db_path: str) -> dict:
    # GROUP BY model, SUM directional tokens
    return {
        "claude-sonnet-4-5": {
            "tokens": 300000,
            "tokens_up": 250000,      # NEW
            "tokens_down": 50000,     # NEW
            "usd": 10.50,
            "carbon": 0.015,
        },
        ...
    }

# Update all other aggregate_cost_by_* functions similarly
```

### 5. `hivenode/ledger/reader.py`

**Ensure event read-back includes new columns:**

```python
def read_event(event_id: int, db_path: str) -> dict:
    # SELECT ... including cost_tokens_up, cost_tokens_down
    return {
        "id": ...,
        "cost_tokens_up": row['cost_tokens_up'],    # NEW
        "cost_tokens_down": row['cost_tokens_down'], # NEW
        ...
    }
```

### 6. `hivenode/routes/ledger_routes.py`

**Update `/ledger/cost` response model:**

```python
# In schemas.py or inline Pydantic model
class CostResponse(BaseModel):
    usd: float
    tokens: int
    tokens_up: int      # NEW
    tokens_down: int    # NEW
    carbon: float
    cost_up_usd: float = None      # NEW (optional breakdown)
    cost_down_usd: float = None    # NEW (optional breakdown)
```

Update route handler to return directional data from aggregation.

### 7. `hivenode/schemas.py`

**Add new fields to response models** (if using centralized schemas).

---

## Files to Read First

**Ledger schema:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\schema.py` (current schema — 14 columns, needs 2 more)

**Ledger writer:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` (write_event function signature)

**Ledger reader:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\reader.py` (event read-back)

**Cost aggregation:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\aggregation.py` (cost aggregation — get_total_cost, aggregate_cost_by_*)

**LLM cost tracking:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\llm\cost.py` (emit_llm_event — already has input_tokens/output_tokens)

**Routes and schemas:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\ledger_routes.py` (/ledger/cost endpoint)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` (response models)

**Existing tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\ledger\test_schema.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\ledger\test_writer.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\ledger\test_aggregation.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\llm\test_cost.py`

---

## Test Requirements (~12 tests)

Update existing test files AND add new tests.

### test_schema.py (update + 2 new tests)

1. Update `test_schema_has_correct_columns()` to check for 16 columns (was 14)
2. New: `test_migrate_schema_adds_new_columns()` — run migration, verify columns exist
3. New: `test_migrate_schema_idempotent()` — run migration twice, no error

### test_writer.py (update + 2 new tests)

1. Update existing tests to pass `cost_tokens_up` and `cost_tokens_down`
2. New: `test_write_event_with_directional_tokens()` — write event with both, verify stored
3. New: `test_write_event_backward_compatible()` — write event without directional tokens (NULL), verify no error

### test_aggregation.py (update + 3 new tests)

1. Update existing tests to check `tokens_up` and `tokens_down` in response
2. New: `test_get_total_cost_returns_directional_tokens()` — verify tokens_up, tokens_down
3. New: `test_aggregate_by_model_includes_directional_tokens()` — verify per-model breakdown
4. New: `test_aggregation_handles_null_directional_tokens()` — old events with NULL tokens_up/down don't break aggregation

### test_cost.py (update + 2 new tests)

1. Update `test_emit_llm_event()` to verify `cost_tokens_up` and `cost_tokens_down` are populated
2. New: `test_emit_llm_event_directional_sum()` — verify `cost_tokens == cost_tokens_up + cost_tokens_down`

### Integration test (3 new tests)

In `tests/hivenode/test_e2e.py` or new file `tests/hivenode/ledger/test_cost_e2e.py`:

1. Write LLM_CALL event with directional tokens → query `/ledger/cost` → verify response includes tokens_up, tokens_down
2. Write multiple events → aggregate by model → verify directional breakdown
3. Mix old events (NULL tokens_up/down) with new events → verify aggregation handles both

Run with: `python -m pytest tests/hivenode/ledger/ -v`

---

## Constraints

- No file over 500 lines.
- TDD — update existing tests first (to fail on new fields), then implement changes.
- **Backward compatibility REQUIRED:** Old events with NULL `cost_tokens_up`/`cost_tokens_down` must not break aggregation queries. Handle NULL as 0 in SUM().
- No stubs.
- Migration must be idempotent (safe to run multiple times).

---

## Definition of Done

- [x] `schema.py` modified (CREATE TABLE has 2 new columns, migration function added)
- [x] `writer.py` modified (write_event accepts and stores cost_tokens_up, cost_tokens_down)
- [x] `cost.py` modified (emit_llm_event passes directional tokens)
- [x] `aggregation.py` modified (all functions return tokens_up, tokens_down)
- [x] `reader.py` modified (event read-back includes new columns)
- [x] `ledger_routes.py` modified (/ledger/cost response includes directional data)
- [x] `schemas.py` modified (response models include new fields)
- [x] Migration function tested (idempotent, adds columns correctly)
- [x] 12 tests written/updated and passing (`python -m pytest tests/hivenode/ledger/ -v`)
- [x] Backward compatibility verified (old events with NULL don't break aggregation)
- [x] No existing tests broken by changes

---

## Response File

Write your response to:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260312-TASK-031-RESPONSE.md`

Use the standard 8-section format from BOOT.md Rule 10.

---

**End of TASK-031.**
