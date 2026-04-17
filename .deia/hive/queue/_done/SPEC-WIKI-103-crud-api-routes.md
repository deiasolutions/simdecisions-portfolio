---
id: WIKI-103
priority: P1
model: sonnet
role: bee
depends_on:
  - WIKI-101
  - WIKI-102
---
# SPEC-WIKI-103: Wiki CRUD API Routes

## Priority
P1

## Model Assignment
sonnet

## Depends On
- WIKI-101
- WIKI-102

## Intent
Implement CRUD API routes for wiki pages: create, read, update, delete, list. On save, automatically parse wikilinks and frontmatter. Support versioning on update (new row, old marked is_current=false). No backlinks query yet — that's next spec.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/store.py` — tables from WIKI-101
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/parser.py` — parsers from WIKI-102
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/efemera/routes.py` — reference for FastAPI route pattern
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/main.py` — where routes get mounted

## Acceptance Criteria
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/routes.py`
- [ ] Routes implemented:
  - `POST /api/wiki/pages` — create new page
  - `GET /api/wiki/pages` — list all current pages (is_current=true, is_deleted=false)
  - `GET /api/wiki/pages/{path}` — get single page by path
  - `PUT /api/wiki/pages/{path}` — update page (creates new version)
  - `DELETE /api/wiki/pages/{path}` — soft delete (is_deleted=true)
  - `GET /api/wiki/pages/{path}/history` — get all versions for a path
- [ ] On POST/PUT: parse frontmatter, parse wikilinks, store both in JSONB fields
- [ ] On PUT: create new row with version+1, mark old row is_current=false, link via previous_version_id
- [ ] Request/response models in `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/schemas.py`
- [ ] Routes mounted in `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/main.py`
- [ ] At least 8 integration tests:
  - Create page, verify stored
  - Get page by path
  - List pages
  - Update page, verify new version created
  - Update page, verify old version marked not current
  - Delete page, verify soft delete
  - Get history, verify all versions returned
  - Create page with frontmatter and wikilinks, verify parsed
- [ ] No file over 500 lines (split routes.py and schemas.py if needed)

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Follow FastAPI pattern from efemera/routes.py
- Use Pydantic models for request/response validation
- workspace_id should come from auth context (for now, accept as header or use default UUID)
- TDD: tests first
- No stubs
- No git operations

## Smoke Test
```bash
# Start hivenode in background
python -m uvicorn hivenode.main:app --host 127.0.0.1 --port 8420 &

# Run tests
cd hivenode && python -m pytest wiki/tests/test_routes.py -v

# Manual check
curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"test","title":"Test Page","content":"# Test\n\nSee [[other-page]] for details."}'

curl http://127.0.0.1:8420/api/wiki/pages/test
```

Expected: Page created, wikilinks parsed and stored in outbound_links field.
