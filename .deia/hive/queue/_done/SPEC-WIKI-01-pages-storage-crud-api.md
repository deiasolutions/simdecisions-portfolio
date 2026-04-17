# SPEC-WIKI-01: Wiki Pages Storage and CRUD API

## Priority
P2

## Model Assignment
sonnet

## Depends On
LEDGER-01

## Intent
Create wiki pages storage schema and basic CRUD API for markdown pages with wikilink support. This is foundation layer - storage, API, and wikilink parsing only. No editor UI, no compilation services, just the data layer.

## Files to Read First
.deia/BOOT.md
hivenode/main.py
hivenode/routes/__init__.py

## Acceptance Criteria
- [ ] `wiki_pages` table created with fields: id, workspace_id, path, title, slug, content, summary, page_type, tags (JSONB), frontmatter (JSONB), outbound_links (JSONB), version, is_current, previous_version_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at
- [ ] `wiki_edit_log` table created with fields: id, page_id, workspace_id, operation, previous_content_hash, new_content_hash, diff_summary, edited_by, edited_at, event_id
- [ ] Proper indexes on workspace_id, path, page_type, tags (GIN), outbound_links (GIN)
- [ ] Wikilink parser function that extracts all `[[link]]` patterns from markdown content
- [ ] On page save, automatically parse and store outbound_links from content
- [ ] CRUD API routes: POST /api/wiki/pages, GET /api/wiki/pages, GET /api/wiki/pages/{path}, PUT /api/wiki/pages/{path}, DELETE /api/wiki/pages/{path}
- [ ] GET /api/wiki/pages/{path}/backlinks endpoint that queries outbound_links to find pages linking to this path
- [ ] Page versioning: PUT creates new version, marks old as is_current=false, links via previous_version_id
- [ ] Frontmatter parser that extracts YAML header from markdown content
- [ ] All operations emit events to ledger (PAGE_CREATED, PAGE_UPDATED, PAGE_DELETED, PAGE_LINKED)
- [ ] At least 6 unit tests for wikilink parsing (including edge cases)
- [ ] At least 4 integration tests for CRUD endpoints
- [ ] At least 2 tests for backlinks functionality
- [ ] Schema compatible with PostgreSQL and SQLite
- [ ] No file over 500 lines

## Constraints
- This spec implements ONLY storage and API layer
- UI components are NOT in scope
- Wiki compilation services are NOT in scope
- Notebook support is NOT in scope
- Search functionality is NOT in scope (basic list/get only)
- Use FastAPI for routes following existing hivenode patterns
- Use SQLAlchemy Core (not ORM)
- All file paths absolute
- No stubs
- No git operations

## Smoke Test
After completion:
1. POST create a wiki page with content containing `[[another-page]]`
2. GET the page - verify outbound_links contains "another-page"
3. POST create "another-page"
4. GET backlinks for "another-page" - verify first page appears
5. PUT update first page - verify new version created, old marked is_current=false
6. GET page history - verify both versions present
7. Check event ledger - verify PAGE_CREATED and PAGE_UPDATED events emitted
