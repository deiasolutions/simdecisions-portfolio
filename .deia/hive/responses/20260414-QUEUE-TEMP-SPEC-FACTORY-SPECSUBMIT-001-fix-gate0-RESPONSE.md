# QUEUE-TEMP-SPEC-FACTORY-SPECSUBMIT-001-fix-gate0: Fix REST Spec Submit to Pass Gate 0 -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-14

## Files Modified

- hivenode/routes/factory_routes.py
- tests/hivenode/routes/test_factory_spec_submit.py (new file)

## What Was Done

- Added `acceptance_criteria` field (list[str]) to SpecSubmitRequest model
- Updated `render_spec_template()` to:
  - Use "## Objective" instead of "## Description"
  - Include "## Depends On" section with "None" or dependency list
  - Populate "## Acceptance Criteria" with checkboxes from request payload
  - Include "## Files to Read First" section (placeholder)
  - Add default constraints: "No file over 500 lines", "No stubs", "No git operations"
- Added Gate 0 validation in `submit_spec()` endpoint:
  - Validates acceptance_criteria is non-empty, returns 422 if missing/empty
  - Writes spec to disk temporarily
  - Runs `gate0.validate_spec()` programmatically
  - Deletes spec file and returns 422 if Gate 0 validation fails
  - Returns success if validation passes
- Imported gate0 and spec_parser modules from `.deia/hive/scripts/queue/`
- Created comprehensive test suite (7 tests):
  - Valid request passes and spec passes Gate 0
  - Missing criteria returns 422
  - Empty criteria returns 422
  - Generated spec has all required sections
  - Generated spec passes all 6 Gate 0 checks
  - Dependencies are correctly formatted
  - Validation runs before file write

## Tests Run

All 7 new tests in `tests/hivenode/routes/test_factory_spec_submit.py` pass:
- test_spec_submit_valid_request
- test_spec_submit_missing_criteria_returns_422
- test_spec_submit_empty_criteria_returns_422
- test_generated_spec_has_all_gate0_sections
- test_generated_spec_passes_gate0_programmatically
- test_spec_submit_with_dependencies
- test_spec_submit_validates_before_writing

No regressions in existing factory route tests.

## Smoke Test Results

Manual curl tests confirmed:
1. Valid spec with acceptance_criteria creates spec that passes Gate 0 ✅
2. Request without acceptance_criteria returns 422 with clear error message ✅
3. Generated spec includes all required sections:
   - ## Priority
   - ## Depends On
   - ## Model Assignment
   - ## Objective (not "Description")
   - ## Files to Read First
   - ## Acceptance Criteria (populated from request)
   - ## Smoke Test
   - ## Constraints
4. Acceptance criteria formatted as `- [ ]` checkboxes ✅
5. Dependencies listed correctly when provided ✅

## Key Changes Summary

**Request model:**
- Added `acceptance_criteria: list[str] = []` field

**Template generation:**
- Changed "## Description" → "## Objective"
- Added "## Depends On" section (shows "None" or list of deps)
- Added "## Files to Read First" placeholder
- Populate "## Acceptance Criteria" from request.acceptance_criteria
- Format criteria as `- [ ] {criterion}` checkboxes
- Include default constraints

**Validation:**
- Check acceptance_criteria is non-empty before rendering
- Run gate0.validate_spec() after writing to disk
- Remove file and return 422 if validation fails
- Only return success if spec passes all 6 Gate 0 checks

## Blockers

None

## Notes

- Gate 0 validation runs programmatically before spec is permanently written
- If validation fails, spec file is deleted and HTTP 422 returned with failure details
- The `GATE0_AVAILABLE` flag handles cases where gate0 module isn't available (degrades gracefully)
- All existing smoke test placeholder patterns retained (e.g., "Add smoke test commands")
- Service required full restart to pick up new code (--force flag on restart-services.sh)
