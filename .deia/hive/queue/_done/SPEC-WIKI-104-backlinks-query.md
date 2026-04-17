---
id: WIKI-104
priority: P2
model: sonnet
role: bee
depends_on:
  - WIKI-103
---
# SPEC-WIKI-104: Backlinks Query API

## Priority
P2

## Model Assignment
sonnet

## Depends On
- WIKI-103

## Intent
Add backlinks query endpoint. Given a page path, return all pages that link to it. Uses the outbound_links JSONB field to find references.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/routes.py` — from WIKI-103
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/store.py` — tables
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-WIKI-V1.md` — lines 490-492 for backlinks API

## Acceptance Criteria
- [ ] Route added to `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/routes.py`:
  - `GET /api/wiki/pages/{path}/backlinks` — returns list of pages that link to this path
- [ ] Query uses JSONB operator to search outbound_links array
- [ ] Returns only current, non-deleted pages
- [ ] Response includes page summary (id, path, title, updated_at)
- [ ] At least 4 tests:
  - Page with backlinks returns correct list
  - Page with no backlinks returns empty list
  - Backlinks only include current versions (not old versions)
  - Backlinks exclude deleted pages
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- PostgreSQL JSONB query: `outbound_links @> '["target-path"]'`
- SQLite fallback: use `json_extract` or Python filter
- TDD: tests first
- No stubs
- No git operations

## Smoke Test
```bash
# Create two pages, one linking to the other
curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"page-a","title":"Page A","content":"See [[page-b]]"}'

curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"page-b","title":"Page B","content":"This is page B."}'

# Check backlinks
curl http://127.0.0.1:8420/api/wiki/pages/page-b/backlinks
```

Expected: Returns page-a in the backlinks list.
