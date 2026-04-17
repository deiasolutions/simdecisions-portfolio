---
id: WIKI-106
priority: P1
model: sonnet
role: bee
depends_on:
  - WIKI-105
---
# SPEC-WIKI-106: Markdown Viewer with Wikilink Navigation

## Priority
P1

## Model Assignment
sonnet

## Depends On
- WIKI-105

## Intent
Replace the placeholder div in WikiPane with a real markdown viewer. Fetch page content from API, render markdown, and make wikilinks clickable. Clicking a wikilink navigates to that page.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/WikiPane.tsx` — from WIKI-105
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md` — lines 1504-1545 for wikilink rendering example

## Acceptance Criteria
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/MarkdownViewer.tsx`
- [ ] MarkdownViewer component:
  - Accepts `path` prop
  - Fetches page from `/api/wiki/pages/{path}`
  - Renders markdown content
  - Transforms `[[wikilink]]` to clickable elements
  - On wikilink click: calls `onNavigate(targetPath)`
- [ ] WikiPane updated:
  - Selected path state managed
  - On tree node click: set selected path
  - MarkdownViewer receives selected path
  - On wikilink click: update selected path (navigates to linked page)
- [ ] Wikilink transformation:
  - Regex: `/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g`
  - Replace with `<a>` tag with click handler
  - Display text: use alias if present, otherwise link target
- [ ] At least 4 component tests:
  - MarkdownViewer fetches and renders page
  - Wikilinks transformed to clickable elements
  - Clicking wikilink calls onNavigate
  - Navigation updates selected path in WikiPane
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use `react-markdown` for markdown rendering
- Wikilink click should preventDefault to avoid page reload
- Use CSS variables for link styling (var(--sd-link-color))
- TDD: tests first
- No stubs
- No git operations

## Smoke Test
```bash
# Ensure hivenode running with wiki data
curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"index","title":"Index","content":"# Wiki Index\n\nSee [[architecture]] for details."}'

curl -X POST http://127.0.0.1:8420/api/wiki/pages \
  -H "Content-Type: application/json" \
  -d '{"path":"architecture","title":"Architecture","content":"# Architecture\n\nBack to [[index]]"}'

# In browser: navigate to wiki pane
# Click "index" in tree
# Verify markdown renders with clickable [[architecture]] link
# Click the link
# Verify navigation to architecture page
```

Expected: Full wiki navigation works — tree click loads page, wikilink click navigates.
