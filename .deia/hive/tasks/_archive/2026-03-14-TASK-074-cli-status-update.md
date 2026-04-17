# TASK-074: Update CLI Commands for Canonical Statuses

## Objective

Update all CLI commands in `inventory.py` to use the new canonical status set and display statuses correctly in output/exports.

## Context

After TASK-073 migrates the database, the CLI must:
1. Validate input statuses against the canonical set
2. Display canonical statuses in `stats`, `list`, `export-md` commands
3. Update error messages to reference new status values

The CLI currently validates against old VALID_STATUSES (`BUILT`, `SPECCED`, etc.). After migration, these must use the new set.

**Depends on:** TASK-073 (migration function and updated constants)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` — CLI tool
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py` — Database operations (for updated constants)

## Deliverables

- [ ] Update `cmd_add()` to validate `--status` against new canonical set
- [ ] Update `cmd_update()` to validate `--status` against new canonical set
- [ ] Update `cmd_stats()` to group by canonical statuses (not old ones)
- [ ] Update `cmd_export_md()` to display canonical statuses in markdown table
- [ ] Update `cmd_list()` to display canonical statuses (no changes needed if using DB values directly)
- [ ] Update `cmd_bug_add()` validation to use canonical bug statuses
- [ ] Update `cmd_bug_list()` to display canonical statuses
- [ ] Update error messages to reference canonical status list
- [ ] Verify file sizes stay under 500 lines (inventory.py currently 505 lines)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Test: `add` command rejects invalid status with clear error message
- [ ] Test: `add` command accepts all canonical statuses
- [ ] Test: `update` command validates status correctly
- [ ] Test: `stats` command groups by canonical statuses
- [ ] Test: `export-md` shows canonical statuses in table
- [ ] Test: Bug commands validate against canonical set
- [ ] Test: Error message lists all valid statuses when validation fails
- [ ] Minimum 7 tests total

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\tests\test_cli_status_validation.py`

Edge cases to test:
- Status validation with uppercase/lowercase input (should be case-sensitive)
- Empty status (should use default)
- Null status (should use default)

## Constraints

- No file over 500 lines (inventory.py is currently 505 — may need to extract helper functions if adding code)
- CSS: not applicable (backend only)
- No stubs
- TDD: tests first, then implementation
- All status validation must use VALID_STATUSES constant (not hardcoded lists)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-074-RESPONSE.md`

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

---

**Model Assignment:** haiku
**Estimated Size:** S-M (validation updates ~30 lines, tests ~80 lines)
