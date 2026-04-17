# SPEC: Fix R14 — Revert and apply minimal enum case fix

## Priority
P0.95 (blocks R14, blocks R15)

## Model Assignment
haiku

## Objective
Revert R14's scope violation changes and apply ONLY enum string case changes (uppercase → lowercase) without touching model schemas.

## Context
TASK-R14 violated scope by rebuilding entire models.py schema (186 line changes). This fixed test_models.py (50 tests pass) but broke 74 other RAG tests + 14 errors.

**Required:** Change ONLY enum string VALUES, preserve all model schemas and fields.

## Task File
`.deia/hive/tasks/2026-03-16-TASK-R14-FIX-minimal-enum.md`

## Acceptance Criteria
- [ ] Revert models.py to pre-R14 state
- [ ] Change ONLY these enum string values to lowercase (preserve member names):
  - `ArtifactType`: CODE, PHASE_IR, ADR, SPEC, DOCUMENT, NOTEBOOK, CONFIG, TEST, OTHER
  - `StorageTier`: HOT, WARM, COLD, ARCHIVE
  - `IRStatus`: VERIFIED, FAILED, UNTESTED, UNKNOWN
- [ ] NO schema changes: preserve all model fields, types, defaults
- [ ] NO new enum members added
- [ ] Run test_models.py: expect some tests to fail (schema mismatch is test bug)
- [ ] Run full RAG test suite: expect 0 new failures vs pre-R14 baseline
- [ ] Document which test_models.py tests fail due to test bugs

## Notes
The test_models.py file expects a DIFFERENT schema than the RAG system uses. Tests should match code, not vice versa. This spec fixes the enum case issue WITHOUT breaking the RAG system.
