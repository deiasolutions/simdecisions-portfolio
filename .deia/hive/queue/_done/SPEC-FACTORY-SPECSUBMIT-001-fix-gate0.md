# SPEC-FACTORY-SPECSUBMIT-001-fix-gate0: Fix REST Spec Submit to Pass Gate 0

## Priority
P1

## Depends On
None

## Model Assignment
haiku

## Objective

The `POST /factory/spec-submit` endpoint in `factory_routes.py` generates specs with placeholder acceptance criteria (`- [ ] (Add acceptance criteria)`) that fail Gate 0 validation. Fix the spec template to generate valid specs that pass Gate 0, and require the caller to provide real acceptance criteria in the request payload.

## Files to Read First

- hivenode/routes/factory_routes.py
- .deia/hive/scripts/queue/gate0.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Acceptance Criteria

- [ ] `spec-submit` request payload accepts an `acceptance_criteria` field (list of strings)
- [ ] If `acceptance_criteria` is empty or missing, return 422 with error message explaining the requirement
- [ ] Generated spec includes all Gate 0 required sections: Priority, Depends On, Model Assignment, Objective, Files to Read First, Acceptance Criteria, Smoke Test, Constraints
- [ ] Generated spec's acceptance criteria use `- [ ]` checkbox format
- [ ] Generated spec includes default constraints (no file over 500 lines, no stubs, no git operations)
- [ ] Generated spec passes Gate 0 validation (run gate0.validate_spec programmatically before writing to disk, return 422 if it fails)
- [ ] All existing tests still pass
- [ ] 3+ new tests: valid submission passes, missing criteria returns 422, generated spec passes Gate 0

## Smoke Test

- [ ] POST a valid spec via curl, verify it lands in backlog and queue runner picks it up

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Do not change the Gate 0 rules — fix the spec generator to comply with them
