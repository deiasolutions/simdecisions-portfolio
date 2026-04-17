# SPEC-HYG-005-ts-node-types: Add @types/node to fix 344 TS2304 errors

## Priority
P1

## Depends On
None

## Model Assignment
haiku

## Objective

Add `@types/node` to browser/package.json devDependencies and add "node" to the `types` array in browser/tsconfig.json. This single change fixes 344 TS2304 "Cannot find name" errors for Node.js globals (global, __dirname, process, Buffer, setTimeout return type, etc.) that are referenced throughout the browser codebase and test files.

## Files to Read First

- browser/tsconfig.json
- browser/package.json
- .deia/reports/tsc.txt

## Acceptance Criteria

- [ ] `@types/node` is listed in browser/package.json devDependencies
- [ ] "node" is included in the `types` array in browser/tsconfig.json compilerOptions
- [ ] `npx tsc --noEmit 2>&1 | grep "TS2304"` count is reduced by at least 300 errors
- [ ] No new TypeScript errors are introduced by this change
- [ ] `npm install` in browser/ completes without errors

## Smoke Test

- [ ] Run `cd browser && npm install` and confirm successful install
- [ ] Run `cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2304"` and confirm the count is below 50
- [ ] Run `cd browser && npx vitest run --reporter=verbose 2>&1 | tail -5` and confirm tests still pass

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- All existing tests must still pass after changes
- Run `npx tsc --noEmit` to verify fixes
- Only modify browser/package.json and browser/tsconfig.json — no source file changes
