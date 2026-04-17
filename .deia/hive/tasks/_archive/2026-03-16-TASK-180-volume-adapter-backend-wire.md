# TASK-180: Wire volumeAdapter to backend /storage endpoints

## Objective
Update filesystemAdapter to use real volume storage endpoints (`/storage/list`, `/storage/stat`) instead of `/repo/tree`. Support home:// protocol for listing directories and reading file metadata.

## Context
The backend already has working storage routes:
- GET `/storage/list?uri=home://path` → returns `{entries: string[]}`
- GET `/storage/stat?uri=home://path/file.txt` → returns `{size: number, modified: string, created: string}`
- GET `/storage/read?uri=home://path/file.txt` → returns file content as bytes

The frontend `filesystemAdapter.ts` currently calls `/repo/tree` which doesn't support volume URIs. Update it to use the storage endpoints.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` (reference for endpoint contracts)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\filesystemAdapter.test.ts`

## Deliverables
- [ ] Update `loadDirectoryTree()` to call `/storage/list?uri=${protocol}://${path}`
- [ ] Fetch metadata for each entry via `/storage/stat` to get size, modified, created dates
- [ ] Return TreeNodeData[] with correct meta fields (path, size, modified, created, isDir)
- [ ] Handle both file and directory entries (directories have no size, files have size)
- [ ] Support protocol parameter (default to `home://`)
- [ ] Error handling for 404, 400, 500 responses

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests still pass (5 tests)
- [ ] New tests for volume protocol:
  - [ ] Calls `/storage/list` with correct URI format
  - [ ] Calls `/storage/stat` for each entry
  - [ ] File nodes include size, modified, created in meta
  - [ ] Directory nodes have children array
  - [ ] Handles 404 gracefully
  - [ ] Protocol defaults to `home://`
- [ ] Minimum 8 tests total

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (not applicable to this task)
- No stubs
- Use existing TreeNodeData interface (no changes to types)
- HIVENODE_URL from import.meta.env.VITE_HIVENODE_URL

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-180-RESPONSE.md`

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
