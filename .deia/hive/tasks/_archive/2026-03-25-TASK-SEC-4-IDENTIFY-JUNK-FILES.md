# TASK-SEC-4: Identify Junk Files in Repository Root

## Objective
Identify malformed artifacts in repository root (files starting with `{`, `nul`, `C...`, etc.) and document them without deletion.

## Context
During development, malformed files may have been created. This task identifies them for Q88N review before deletion.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.gitignore`

## Deliverables
- [ ] Run `ls -la` in repo root and identify files matching these patterns:
  - Starts with `{` (e.g., `{browser`, `{hivenode`)
  - Named `nul`
  - Starts with `C` followed by `...` or similar malformed path
  - Contains pattern `k.startsWith('RAILWAY'))`
- [ ] List each file with its size and modification date
- [ ] Do NOT delete any files (read-only task)
- [ ] Document findings in response file for Q88N review

## Test Requirements
- No tests required (read-only verification task)
- Document output of `ls -la` showing identified files

## Constraints
- Read-only task
- No git operations
- If `nul` file exists, document it but do not delete

## Model
Haiku (simple file listing)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-SEC-4-RESPONSE.md`

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
