# SPEC-WIKIV1-01: ShiftCenter Wiki Pane Basics

## Priority
P2

## Model Assignment
sonnet

## Depends On
WIKI-01

## Intent
Create the WikiPane primitive component for ShiftCenter with tree browser and markdown viewer. This is the minimal viable UI - display and navigate wiki pages only. No editing, no notebooks, just read-only navigation with wikilink support.

## Files to Read First
.deia/BOOT.md
browser/src/primitives/tree-browser/TreeBrowser.tsx
browser/src/shell/HiveHostPanes.tsx

## Acceptance Criteria
- [ ] WikiPane component created at `browser/src/primitives/wiki/WikiPane.tsx`
- [ ] WikiTree component displays .wiki/ directory structure in tree view
- [ ] Markdown viewer component renders wiki page content with proper formatting
- [ ] Wikilink renderer converts `[[page]]` to clickable links that navigate to target page
- [ ] Clicking wikilink navigates to target page within same WikiPane
- [ ] Page navigation updates URL hash to enable browser back/forward
- [ ] Loading states shown while fetching pages
- [ ] Error states shown for missing pages with helpful message
- [ ] WikiPane registered as primitive in HiveHostPanes
- [ ] API integration with GET /api/wiki/pages and GET /api/wiki/pages/{path} endpoints
- [ ] Frontmatter displayed in metadata panel (collapsible)
- [ ] All colors use CSS variables `var(--sd-*)`
- [ ] Component TypeScript with proper prop types
- [ ] At least 4 component unit tests (rendering, navigation, wikilinks, error states)
- [ ] At least 2 integration tests with mock API
- [ ] No file over 500 lines
- [ ] Component follows existing primitive patterns (tree-browser, conversation-pane, etc.)

## Constraints
- This spec implements ONLY read-only viewer
- Editing is NOT in scope
- Backlinks panel is NOT in scope
- Search is NOT in scope
- Version history is NOT in scope
- Notebooks are NOT in scope
- Eggs are NOT in scope
- Focus on clean, minimal navigation experience
- Reuse existing tree-browser patterns where applicable
- All file paths absolute
- No stubs
- No git operations

## Smoke Test
After completion:
1. Open WikiPane in ShiftCenter shell
2. Tree shows .wiki/ structure
3. Click on a page in tree - content renders
4. Click on a wikilink in content - navigates to linked page
5. Browser back button returns to previous page
6. Try navigating to non-existent page - shows friendly error
7. Verify all colors are CSS variables (inspect element)
