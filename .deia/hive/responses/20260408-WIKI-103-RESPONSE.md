# WIKI-103: Wiki CRUD API Routes -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-08

## Files Modified

### Created Files
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/routes.py` (425 lines)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/schemas.py` (66 lines)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/tests/test_routes.py` (315 lines)

### Modified Files
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/main.py` (added wiki router import and mount, added wiki store initialization in lifespan)

## What Was Done

### Routes Implementation
Created all 6 required API routes in `hivenode/wiki/routes.py`:
1. **POST /api/wiki/pages** - Create new wiki page
2. **GET /api/wiki/pages** - List all current pages (is_current=true, is_deleted=false)
3. **GET /api/wiki/pages/{path}** - Get single page by path
4. **PUT /api/wiki/pages/{path}** - Update page (creates new version)
5. **DELETE /api/wiki/pages/{path}** - Soft delete page
6. **GET /api/wiki/pages/{path}/history** - Get all versions for a path

### Automatic Parsing
- On POST/PUT: automatically parse frontmatter using `parse_frontmatter()` from parser.py
- On POST/PUT: automatically parse wikilinks using `parse_wikilinks()` from parser.py
- Both parsed results stored in JSONB fields (frontmatter, outbound_links)
- Extract page_type and tags from frontmatter if present

### Versioning System
- On PUT: creates new row with version+1
- Marks old row as is_current=false
- Links new version to old via previous_version_id
- Preserves original created_at and created_by fields
- History endpoint returns all versions ordered by version DESC (newest first)

### Request/Response Models
Created Pydantic schemas in `hivenode/wiki/schemas.py`:
- CreatePageRequest (path, title, content, summary)
- UpdatePageRequest (title, content, summary)
- PageResponse (all page fields)
- ListPagesResponse (pages array + total count)
- PageHistoryResponse (versions array + total count)
- DeletePageResponse (path + deleted boolean)

### Integration Tests
Created 9 comprehensive integration tests in `hivenode/wiki/tests/test_routes.py`:
1. Create page basic
2. Create page with frontmatter and wikilinks (verify parsing)
3. Get page by path
4. Get page not found (404)
5. List pages
6. Update page creates new version
7. Update page marks old version not current
8. Delete page soft delete
9. Get history all versions

All tests use in-memory SQLite database and FastAPI TestClient.

### Route Mounting
- Imported wiki_router in `hivenode/main.py`
- Mounted with `app.include_router(wiki_router)`
- Initialized wiki store in lifespan (follows same pattern as inventory/relay stores)

### Design Pattern
- Follows FastAPI + SQLAlchemy Core pattern from entities/routes.py
- Uses `verify_jwt_or_local` dependency for auth (local mode bypass, cloud mode requires JWT)
- Uses DEFAULT_WORKSPACE_ID constant ("00000000-0000-0000-0000-000000000000") as specified
- All database operations use SQLAlchemy Core (not ORM) matching store.py pattern
- Proper error handling with HTTPException 404 for not found cases

## Test Results
```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
hivenode/wiki/tests/test_routes.py::TestCreatePage::test_create_page_basic PASSED [ 11%]
hivenode/wiki/tests/test_routes.py::TestCreatePage::test_create_page_with_frontmatter_and_links PASSED [ 22%]
hivenode/wiki/tests/test_routes.py::TestGetPage::test_get_page_by_path PASSED [ 33%]
hivenode/wiki/tests/test_routes.py::TestGetPage::test_get_page_not_found PASSED [ 44%]
hivenode/wiki/tests/test_routes.py::TestListPages::test_list_pages PASSED [ 55%]
hivenode/wiki/tests/test_routes.py::TestUpdatePage::test_update_page_creates_new_version PASSED [ 66%]
hivenode/wiki/tests/test_routes.py::TestUpdatePage::test_update_page_marks_old_version_not_current PASSED [ 77%]
hivenode/wiki/tests/test_routes.py::TestDeletePage::test_delete_page_soft_delete PASSED [ 88%]
hivenode/wiki/tests/test_routes.py::TestGetPageHistory::test_get_history_all_versions PASSED [100%]

============================== 9 passed in 2.18s
```

## Acceptance Criteria

✅ File created: `routes.py` (425 lines - under 500 line limit)
✅ Routes implemented: All 6 endpoints (POST, GET list, GET single, PUT, DELETE, GET history)
✅ On POST/PUT: parse frontmatter and wikilinks, store both in JSONB fields
✅ On PUT: create new row with version+1, mark old row is_current=false, link via previous_version_id
✅ Request/response models in `schemas.py` (66 lines)
✅ Routes mounted in `main.py`
✅ At least 8 integration tests: 9 tests created and passing
✅ No file over 500 lines: routes.py (425), schemas.py (66), test_routes.py (315)

## Constraints Verified

✅ EXECUTE mode: Wrote code immediately without entering plan mode
✅ Followed FastAPI pattern from entities/routes.py
✅ Used SQLAlchemy Core (not ORM) matching store.py pattern
✅ Used Pydantic models for request/response validation
✅ workspace_id: used default UUID as specified
✅ TDD: Wrote tests first, then implementation
✅ No stubs: Every function fully implemented
✅ No git operations: Did not run any git commands

## Smoke Test

Command: `cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter && python -m pytest hivenode/wiki/tests/test_routes.py -v`

Result: **All 9 tests pass** ✅

Expected behavior achieved: Routes create, read, update, delete, list wiki pages with automatic wikilink/frontmatter parsing and versioning.

## Notes

- Routes are ready for integration with frontend wiki UI
- Backlinks query endpoint is NOT implemented (that's for next spec as noted in Intent)
- All versioning logic works correctly (tested via history endpoint)
- Soft delete prevents deleted pages from appearing in list/get endpoints
- Frontmatter parsing extracts page_type and tags automatically
- Wikilink parsing supports both `[[link]]` and `[[link|display]]` formats
