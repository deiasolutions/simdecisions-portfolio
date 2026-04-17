# SPEC-WIKI-101: Database Schema and Tables -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-07

## Files Modified

- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/__init__.py` (created, 75 bytes)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/store.py` (created, 214 lines)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/tests/hivenode/wiki/test_wiki_schema.py` (created, 321 lines)

## What Was Done

- Created `hivenode/wiki/` module directory with `__init__.py`
- Created `hivenode/wiki/store.py` with:
  - `metadata = MetaData()` (wiki-specific metadata)
  - `wiki_pages` table with 19 columns (id, workspace_id, path, title, content, summary, page_type, tags, frontmatter, outbound_links, version, is_current, previous_version_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at)
  - `wiki_edit_log` table with 10 columns (id, page_id, workspace_id, operation, previous_content_hash, new_content_hash, diff_summary, edited_by, edited_at, event_id)
  - 5 indexes: ix_wiki_pages_workspace, ix_wiki_pages_path, ix_wiki_pages_type, ix_wiki_edit_log_page, ix_wiki_edit_log_time
  - `init_engine(db_url: str)` function that creates engine, runs create_all, runs migration, returns engine
  - `get_engine()` function that returns current engine or raises if not initialized
  - `reset_engine()` function for tests
  - `_migrate_schema(engine)` idempotent migration function that adds missing columns to existing tables
  - Helper functions: `_now()`, `_row_to_dict()`, `_rows_to_dicts()`
- Created `tests/hivenode/wiki/test_wiki_schema.py` with 13 tests:
  - `test_tables_created_on_fresh_db` — verifies both tables are created
  - `test_wiki_pages_columns_exist` — verifies all 19 columns exist
  - `test_wiki_pages_column_types` — verifies Text and Integer types (SQLite/PostgreSQL compatible)
  - `test_wiki_pages_nullability` — verifies NOT NULL constraints on required columns
  - `test_wiki_edit_log_columns_exist` — verifies all 10 columns exist
  - `test_wiki_edit_log_column_types` — verifies Text types
  - `test_wiki_edit_log_nullability` — verifies NOT NULL constraints
  - `test_indexes_created` — verifies all 5 indexes exist
  - `test_init_engine_idempotent` — verifies calling init_engine twice doesn't error
  - `test_migrate_schema_adds_missing_columns` — verifies migration is idempotent
  - `test_insert_wiki_page_basic` — verifies INSERT works on wiki_pages
  - `test_insert_wiki_edit_log_basic` — verifies INSERT works on wiki_edit_log
  - `test_default_values_applied` — verifies server defaults (page_type='doc', version=1, is_current=1, is_deleted=0)

## Test Results

All 13 tests passed:
```
tests/hivenode/wiki/test_wiki_schema.py::test_tables_created_on_fresh_db PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_wiki_pages_columns_exist PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_wiki_pages_column_types PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_wiki_pages_nullability PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_wiki_edit_log_columns_exist PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_wiki_edit_log_column_types PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_wiki_edit_log_nullability PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_indexes_created PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_init_engine_idempotent PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_migrate_schema_adds_missing_columns PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_insert_wiki_page_basic PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_insert_wiki_edit_log_basic PASSED
tests/hivenode/wiki/test_wiki_schema.py::test_default_values_applied PASSED

13 passed in 0.43s
```

## Compliance

- ✅ TDD: Tests written first, then implementation
- ✅ SQLAlchemy Core (NOT ORM) pattern followed exactly from inventory/store.py
- ✅ Text type for all strings (SQLite + PostgreSQL compatible)
- ✅ Integer type for booleans (0/1, SQLite compatible)
- ✅ Text type for JSON columns (not JSONB, SQLite compatible)
- ✅ Text type for UUID columns (not native UUID, SQLite compatible)
- ✅ Idempotent migration function (_migrate_schema)
- ✅ No VECTOR columns (deferred to later, PostgreSQL-only)
- ✅ No GIN indexes on JSON columns (deferred to later, PostgreSQL-only)
- ✅ No foreign key references to users table (self-contained)
- ✅ No file over 500 lines (store.py: 214 lines, test_wiki_schema.py: 321 lines)
- ✅ No stubs — all functions fully implemented
- ✅ No git operations performed
- ✅ All acceptance criteria met

## Schema Design Notes

**wiki_pages table:**
- Primary key: `id` (Text, UUID string)
- Required fields: workspace_id, path, title, content, created_at, updated_at
- Optional fields: summary, created_by, updated_by, deleted_at
- JSON fields stored as Text: tags, frontmatter, outbound_links
- Versioning: version (Integer), is_current (Integer 0/1), previous_version_id (Text)
- Soft delete: is_deleted (Integer 0/1), deleted_at (Text)
- Server defaults: page_type='doc', version=1, is_current=1, is_deleted=0

**wiki_edit_log table:**
- Primary key: `id` (Text, UUID string)
- Required fields: page_id, workspace_id, operation, edited_at
- Optional fields: previous_content_hash, new_content_hash, diff_summary, edited_by, event_id
- Links to page via page_id (no foreign key constraint for self-containment)
- Links to event ledger via event_id (optional)

**Indexes:**
1. ix_wiki_pages_workspace — query by workspace
2. ix_wiki_pages_path — query by path
3. ix_wiki_pages_type — filter by page_type
4. ix_wiki_edit_log_page — get edit history for a page
5. ix_wiki_edit_log_time — sort edits chronologically

## Next Steps

This schema is ready for:
- SPEC-WIKI-102: Wikilink parser
- SPEC-WIKI-103: CRUD API routes
- SPEC-WIKI-104: Backlinks query
- SPEC-WIKI-105: WikiPane primitive
- SPEC-WIKI-106: Markdown viewer
- SPEC-WIKI-107: Backlinks panel
- SPEC-WIKI-108: EGG integration

All dependent specs can now build on this foundation.

## Smoke Test Command

```bash
python -m pytest tests/hivenode/wiki/test_wiki_schema.py -v
```

Expected: All 13 tests pass.
Actual: ✅ All 13 tests passed in 0.43s.
