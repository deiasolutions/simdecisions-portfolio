# TRIAGE ESCALATION: WIKI-101

**Date:** 2026-04-12 19:02:40 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-WIKI-101-database-schema-tables.active-divergent.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-09T15:50:45.789481Z — requeued (empty output)
- 2026-04-12T18:52:40.103924Z — requeued (empty output)
- 2026-04-12T18:57:40.166446Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-WIKI-101-database-schema-tables.active-divergent.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

---
id: WIKI-101
priority: P1
model: sonnet
role: bee
depends_on: []
---
# SPEC-WIKI-101: Wiki Database Schema and Tables

## Priority
P1

## Model Assignment
sonnet

## Depends On
none

## Intent
Create database tables for wiki system: `wiki_pages` and `wiki_edit_log`. Schema must support both SQLite (local dev) and PostgreSQL (production), with proper indexes and constraints. This is pure schema work — no routes, no parsing, just tables.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/inventory/store.py` — reference for SQLAlchemy Core pattern
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/efemera/store.py` — another table example
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-WIKI-V1.md` — lines 64-168 for schema definition

## Acceptance Criteria
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/store.py`
- [ ] `wiki_pages` table defined with columns:
  - id (UUID primary key)
  - workspace_id (UUID not null)
  - path (VARCHAR 500)
  - title (VARCHAR 255)
  - slug (VARCHAR 255 computed from title)
  - content (TEXT)
  - summary (VARCHAR 500)
  - page_type (VARCHAR 50 default 'doc')
  - tags (JSONB default [])
  - frontmatter (JSONB default {})
  - outbound_links (JSONB default [])
  - version (INTEGER default 1)
  - is_current (BOOLEAN default TRUE)
  - previous_version_id (UUID references wiki_pages)
  - created_at, updated_at (TIMESTAMPTZ)
  - created_by, updated_by (UUID)
  - is_deleted (BOOLEAN default FALSE)
  - deleted_at (TIMESTAMPTZ)
- [ ] Unique constraint on (workspace_id, path, version)
- [ ] Indexes on: workspace_id, path, page_type, tags (GIN), outbound_links (GIN)
- [ ] `wiki_edit_log` table defined with columns:
  - id, page_id, workspace_id, operation, previous_content_hash, new_content_hash, diff_summary, edited_by, edited_at, event_id
- [ ] Indexes on: page_id, edited_at DESC
- [ ] `init_engine()` function creates tables if not exist
- [ ] Tables compatible with both SQLite and PostgreSQL
- [ ] At least 6 tests verifying table creation and constraints
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use SQLAlchemy Core (not ORM) — follow pattern from inventory/store.py
- JSONB fields work on both PG and SQLite (SQLAlchemy handles it)
- Computed column (slug) uses database-native approach (generated column or trigger)
- TDD: tests first
- No stubs
- No git operations

## Smoke Test
```bash
# Run from repo root
cd hivenode && python -m pytest wiki/tests/test_store.py -v
```

Expected: All tests pass, tables created in test DB, constraints enforced.

## Triage History
- 2026-04-09T15:50:45.789481Z — requeued (empty output)
- 2026-04-12T18:52:40.103924Z — requeued (empty output)
- 2026-04-12T18:57:40.166446Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
