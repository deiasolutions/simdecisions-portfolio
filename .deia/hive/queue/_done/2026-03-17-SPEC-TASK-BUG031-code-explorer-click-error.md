# BUG-031: Code explorer files return error on click

## Objective
Fix the Code EGG's file explorer so clicking a file opens it instead of showing "Error loading file Bar Request URI".

## Context
The Code EGG has a tree-browser file explorer. Clicking a file triggers an API request that fails with a bad request URI error. The fileExplorerAdapter is likely constructing the wrong URL or the backend endpoint doesn't exist/has changed.

## Files to Read First
- `eggs/code.egg.md`
- `browser/src/primitives/tree-browser/adapters/`
- `browser/src/apps/`
- `hivenode/routes/`

## Deliverables
- [ ] Trace file click handler and API request construction
- [ ] Fix the request URI to match the backend endpoint
- [ ] File content loads and displays in the editor pane
- [ ] Tests for file selection and loading

## Acceptance Criteria
- [ ] Clicking a file in Code explorer loads its content
- [ ] No "Error loading file" message
- [ ] Error handling for genuinely missing files
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
