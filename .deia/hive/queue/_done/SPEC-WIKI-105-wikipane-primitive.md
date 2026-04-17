---
id: WIKI-105
priority: P1
model: sonnet
role: bee
depends_on:
  - WIKI-103
  - WIKI-104
---
# SPEC-WIKI-105: WikiPane Primitive Component

## Priority
P1

## Model Assignment
sonnet

## Depends On
- WIKI-103
- WIKI-104

## Intent
Create WikiPane primitive component and register it in ShellNodeRenderer. This is the container that will hold the wiki tree and content viewer. For now, it's a basic layout — tree browser on left (using existing tree-browser), content pane on right (placeholder for now).

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/components/ShellNodeRenderer.tsx` — where primitives register
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/ConversationPane.tsx` — reference primitive
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/TreeBrowser.tsx` — tree component we'll use

## Acceptance Criteria
- [ ] Directory created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/`
- [ ] File created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/WikiPane.tsx`
- [ ] WikiPane component renders:
  - Left: tree-browser configured for wiki pages
  - Right: placeholder div "Wiki content will go here"
- [ ] WikiPane registered in ShellNodeRenderer.tsx with appType: 'wiki'
- [ ] Tree adapter created: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/wiki/wikiAdapter.ts`
  - Fetches pages from `/api/wiki/pages`
  - Transforms to tree nodes (path becomes tree structure)
- [ ] On tree node click: console.log the selected path (viewer not built yet)
- [ ] At least 2 component tests:
  - WikiPane renders tree and content area
  - Tree adapter fetches and transforms pages
- [ ] No file over 500 lines

## Constraints
- You are in EXECUTE mode. Write all code and tests. Do NOT enter plan mode. Do NOT ask for approval. Just build it.
- Use existing tree-browser component — don't build a new one
- Content viewer is NOT in scope — just placeholder div
- Markdown rendering is NOT in scope yet
- Follow primitive registration pattern from conversation-pane
- TDD: tests first (use vitest for React tests)
- No stubs
- No git operations

## Smoke Test
```bash
# Start vite dev server
cd browser && npx vite --port 5173 &

# In browser: open http://localhost:5173
# Navigate to wiki primitive in shell
# Verify tree shows wiki pages
# Click a node, check console for path
```

Expected: Tree renders with wiki pages, clicking logs the path.
