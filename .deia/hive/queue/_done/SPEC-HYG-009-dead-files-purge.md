# SPEC-HYG-009-dead-files-purge: Remove stranded files and dead exports identified by knip

## Priority
P2

## Depends On
SPEC-HYG-006, SPEC-HYG-007, SPEC-HYG-008

## Model Assignment
sonnet

## Objective

Remove 55 stranded files identified by knip (legacy test files, obsolete adapters, Vite build artifacts that are no longer referenced). Remove `@types/p5` from browser/package.json devDependencies since no code imports p5. Triage 126 unused exports — remove confirmed-dead ones that have no consumers anywhere in the codebase, and keep legitimate public API exports that are intentionally exposed. This must happen after HYG-006/007/008 to avoid removing files that are only "unused" due to type errors.

## Files to Read First

- .deia/reports/knip.json
- .deia/reports/code-hygiene-2026-04-12.md
- browser/package.json

## Acceptance Criteria

- [ ] All 55 stranded files from knip.json are either deleted or documented with justification for keeping
- [ ] `@types/p5` is removed from browser/package.json devDependencies
- [ ] At least 80 of the 126 unused exports are removed (remaining must have documented justification)
- [ ] No import errors when running `cd browser && npx tsc --noEmit`
- [ ] All existing tests still pass after changes
- [ ] No production functionality is broken by file removals
- [ ] `npm install` in browser/ completes without errors after package.json changes

## Smoke Test

- [ ] Run `cd browser && npx tsc --noEmit` and confirm no new errors introduced
- [ ] Run `cd browser && npx vitest run --reporter=verbose 2>&1 | tail -5` and confirm tests pass
- [ ] Run `cd browser && cat package.json | python -c "import sys,json; d=json.load(sys.stdin); print('@types/p5' not in d.get('devDependencies',{}))"` and confirm True
- [ ] Run `cd browser && npx knip --reporter json 2>/dev/null | python -c "import sys,json; d=json.load(sys.stdin); print('files:', len(d.get('files',[])))"` and confirm files count is below 10

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `npx tsc --noEmit` to verify no new errors
- Before deleting any file, grep the entire codebase for imports/references to that file
- Before removing any export, grep for all consumers — if any consumer exists outside tests, keep the export
- Do not remove files that are dynamically imported or loaded at runtime via string paths
- If unsure whether a file is dead, keep it and note the uncertainty in the response
