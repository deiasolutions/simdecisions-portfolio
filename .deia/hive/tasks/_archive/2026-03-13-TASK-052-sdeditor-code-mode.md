# TASK-052: SDEditor Code Mode with Syntax Highlighting

## Objective
Add syntax highlighting to SDEditor's code mode using Prism.js or highlight.js, with a language selector dropdown.

## Context
Code mode currently exists (via codeRenderer.tsx) but has no syntax highlighting. This task adds:
- Syntax highlighting via a lightweight library
- Language selector dropdown (Python, JavaScript, TypeScript, JSON, YAML, Markdown, HTML, CSS, Bash)
- Line numbers (already exists in codeRenderer)
- Monospace font (already exists)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\codeRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` (check existing dependencies)

## Deliverables
- [ ] Check if Prism.js or highlight.js already exists in dependencies — if not, add via npm/yarn
- [ ] Update `CodeView` component to accept `language` prop
- [ ] Add syntax highlighting to CodeView using the library
- [ ] Create language selector dropdown in code mode toolbar
- [ ] Language selector state stored in localStorage (key: `sd:code_language_${nodeId}`)
- [ ] Default language: 'javascript'
- [ ] Supported languages: python, javascript, typescript, json, yaml, markdown, html, css, bash
- [ ] Update sd-editor.css with syntax highlighting theme using `var(--sd-*)` colors
- [ ] All styles use `var(--sd-*)` only (no hardcoded colors from Prism/highlight.js default themes)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing code mode tests pass
- [ ] 7+ new tests in codeRenderer.test.tsx:
  - Syntax highlighting renders for JavaScript
  - Syntax highlighting renders for Python
  - Syntax highlighting renders for JSON
  - Language selector shows 9 languages
  - Changing language updates highlighting
  - Language preference persists to localStorage
  - Fallback to plain text for unknown language

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only — map Prism/highlight.js token types to SD theme variables
- No stubs
- Use CDN import OR npm package (check existing pattern in project)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260313-TASK-052-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
sonnet

## Dependencies
- Depends on TASK-050 (mode refactor)

## Notes for Bee
- Prefer highlight.js if no preference exists — it's lighter and easier to theme
- Token-to-color mapping should be semantic (keywords → purple, strings → green, etc.)
- Do NOT import the default Prism/highlight.js CSS — build your own theme using SD variables
