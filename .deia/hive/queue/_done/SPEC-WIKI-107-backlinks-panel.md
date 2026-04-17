---
id: WIKI-107
priority: P2
model: sonnet
role: bee
depends_on:
  - WIKI-106
---
# SPEC-WIKI-107: Backlinks Panel Component

## Priority
P2

## Model Assignment
sonnet

## Depends On
- WIKI-106

## Intent
Add a backlinks panel to WikiPane showing pages that link to the current page. Fetches from the backlinks API endpoint. Clicking a backlink navigates to that page.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/WikiPane.tsx` — from WIKI-106
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/wiki/routes.py` — backlinks endpoint from WIKI-104

## Acceptance Criteria
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/BacklinksPanel.tsx`
- [ ] BacklinksPanel component:
  - Accepts `path` prop
  - Fetches backlinks from `/api/wiki/pages/{path}/backlinks`
  - Renders list of linking pages
  - On click: calls `onNavigate(backlink.path)`
- [ ] WikiPane updated:
  - Layout changed to three columns: tree | content | backlinks
  - Backlinks panel receives current path
  - Backlinks panel hidden if no backlinks
- [ ] Backlinks list shows:
  - Page title
  - Page path (smaller text)
  - Click navigates to that page
- [ ] At least 3 component tests:
  - BacklinksPanel fetches and renders backlinks
  - Clicking backlink calls onNavigate
  - Panel hidden when no backlinks
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Backlinks panel should be collapsible (optional enhancement if time permits)
- Use CSS variables for styling
- TDD: tests first
- No stubs
- No git operations

## Smoke Test
```bash
# Ensure pages with backlinks exist
curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"core","title":"Core","content":"# Core Concepts"}'

curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"intro","title":"Intro","content":"See [[core]] for basics."}'

curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"advanced","title":"Advanced","content":"Building on [[core]], we..."}'

# In browser: navigate to "core" page
# Verify backlinks panel shows "Intro" and "Advanced"
# Click a backlink
# Verify navigation to that page
```

Expected: Backlinks panel renders, clicking navigates.
