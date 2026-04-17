---
id: WIKI-101
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-WIKI-101: Database Schema and Tables

## Priority
P1

## Model Assignment
sonnet

## Depends On
(none)

## Intent
Create the wiki database tables (`wiki_pages`, `wiki_edit_log`) using SQLAlchemy Core, matching the existing inventory store pattern. Include idempotent migration and init_engine function. This is the foundation — all other wiki specs depend on it.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/inventory/store.py` — follow this exact pattern for SQLAlchemy Core table definitions, MetaData, init_engine, and idempotent migration
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-WIKI-V1.md` — lines 62-168 for canonical schema (adapt to SQLAlchemy Core, not raw SQL)

## Acceptance Criteria
- [ ] Directory created: `hivenode/wiki/` with `__init__.py`
- [ ] File created: `hivenode/wiki/store.py` containing:
  - `metadata = MetaData()` (wiki-specific, not shared)
  - `wiki_pages` table with columns: id (Text PK, UUID string), workspace_id (Text, not null), path (Text, not null), title (Text, not null), content (Text, not null), summary (Text), page_type (Text, default 'doc'), tags (Text, JSON string), frontmatter (Text, JSON string), outbound_links (Text, JSON string), version (Integer, default 1), is_current (Integer, default 1), previous_version_id (Text), created_at (Text, not null), updated_at (Text, not null), created_by (Text), updated_by (Text), is_deleted (Integer, default 0), deleted_at (Text)
  - `wiki_edit_log` table with columns: id (Text PK), page_id (Text, not null), workspace_id (Text, not null), operation (Text, not null), previous_content_hash (Text), new_content_hash (Text), diff_summary (Text), edited_by (Text), edited_at (Text, not null), event_id (Text)
  - Indexes on: workspace_id, path, page_type, page_id (edit_log), edited_at (edit_log)
  - `init_engine(db_url: str)` function that creates engine, runs `metadata.create_all()`, and returns engine
  - Idempotent `_migrate_schema(engine)` function that adds missing columns (same pattern as inventory store)
- [ ] File created: `hivenode/wiki/__init__.py` (empty or minimal)
- [ ] Test file created: `tests/hivenode/wiki/test_wiki_schema.py` with at least 6 tests:
  - Tables created successfully on fresh SQLite
  - All wiki_pages columns exist with correct types
  - All wiki_edit_log columns exist with correct types
  - Indexes created correctly
  - init_engine is idempotent (calling twice doesn't error)
  - _migrate_schema adds missing columns gracefully
- [ ] All tests pass with `python -m pytest tests/hivenode/wiki/test_wiki_schema.py -v`
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use SQLAlchemy Core (NOT ORM). Follow the inventory/store.py pattern exactly.
- Use Text type for all string columns (SQLite + PostgreSQL compatible).
- Use Integer for boolean-like columns (SQLite compatible: 0/1 not true/false).
- Use Text for JSON columns (store as JSON strings, not JSONB — SQLite compatible).
- Use Text for UUID columns (store as UUID strings, not native UUID type).
- Do NOT add VECTOR columns or GIN indexes — those are PostgreSQL-only features deferred to later.
- Do NOT reference a `users` table with foreign keys — keep this self-contained.
- TDD: write tests first, then implementation.
- No stubs. Every function complete.
- No git operations.

## Smoke Test
```bash
python -m pytest tests/hivenode/wiki/test_wiki_schema.py -v
```

Expected: All 6+ tests pass.
