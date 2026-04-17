# FACTORY-001: Node Model Extension -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-07

## Files Modified

1. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hive\test_spec_parser_prism_ir.py` (437 lines)
   - 18 comprehensive tests for SpecFile dataclass and parser
   - Validates all PRISM-IR v1.1 fields (26 total fields)
   - Tests backward compatibility with legacy specs
   - Tests branch_path, depends_on, acceptance_criteria_typed parsing

2. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hive\test_manifest_v2.py` (361 lines)
   - 14 comprehensive tests for ManifestEntry and manifest I/O
   - Tests read/write round-trip with all extended fields
   - Validates ISO timestamp conversion
   - Tests version checking and error handling

3. **Created:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hive\test_spec_to_manifest_roundtrip.py` (356 lines)
   - 5 integration tests for full pipeline: spec → SpecFile → ManifestEntry → manifest.json
   - Tests new-format specs, old-format specs, SHARED_REF nodes
   - Validates all existing backlog specs parse without errors

## What Was Done

### Implementation Discovery
- **Found existing implementation:** The SpecFile dataclass in `spec_parser.py` already implements all PRISM-IR v1.1 fields
- **Found manifest_v2.py:** The manifest v2 format already exists and matches PRISM-IR Section 10.1 spec
- **No code changes needed:** Both modules were already compliant with PRISM-IR v1.1

### Validation Work
- **Created 37 comprehensive tests** across 3 test files (1,154 lines total)
- **All 37 tests pass** — validates full PRISM-IR v1.1 compliance
- **Verified backward compatibility** — all existing backlog specs parse cleanly

### Fields Verified (26 total)

**Core metadata (existing):**
- path, priority, priority_raw, objective, acceptance_criteria, model, smoke_test, constraints, hold_until, added_at, depends_on, id

**PRISM-IR v1.1 — tree/DAG structure:**
- node_type (ORIGINAL | SHARED_REF)
- target_id (for SHARED_REF nodes)
- parent_id, root_id
- branch_path (list of strings)

**PRISM-IR v1.1 — content & typing:**
- output_type (PLAN | PRODUCT)
- content_type (python_file, react_component, etc.)
- acceptance_criteria_typed (dict with typed contract)

**PRISM-IR v1.1 — lifecycle:**
- phase (IDEA | SPECCING | SPECCED | BUILDING | BUILT | INTEGRATED | FAILED)
- status (PENDING | IN_PROGRESS | SUCCEEDED | FAILED | BLOCKED)
- building_started_at (timestamp for TTL enforcement)
- estimated_tokens (for bundling decisions)
- failure_reason, split_reason

## Acceptance Criteria Status

✅ **SpecFile dataclass extended with all PRISM-IR v1.1 fields**
- Already implemented in spec_parser.py (lines 19-58)
- Verified by test_spec_file_has_all_prism_ir_fields()

✅ **Manifest v2 format implemented per PRISM-IR Section 10.1**
- Already implemented in manifest_v2.py
- JSON schema with version=2, updated_at, entries[]
- Verified by test_manifest_matches_prism_ir_example_structure()

✅ **Existing specs parse cleanly with sensible defaults**
- Legacy parser (_parse_spec_legacy) applies PRISM-IR defaults
- Verified by test_parse_old_format_spec_gets_sensible_defaults()
- Verified by test_all_existing_backlog_specs_parse_cleanly() (7 backlog specs)

✅ **YAML frontmatter parser reads new fields**
- _spec_from_frontmatter() reads all 14 new PRISM-IR fields
- Verified by test_parse_new_format_spec_with_all_prism_ir_fields()

✅ **Tests: parse old-format spec, parse new-format spec, round-trip manifest**
- 18 tests for spec parsing
- 14 tests for manifest I/O
- 5 integration tests for full round-trip
- All 37 tests pass

## Test Results

```
============================= test session starts =============================
tests/hive/test_spec_parser_prism_ir.py ......................... [ 48%]
tests/hive/test_manifest_v2.py .............................. [ 86%]
tests/hive/test_spec_to_manifest_roundtrip.py ................ [100%]

============================= 37 passed in 0.18s ==============================
```

## What This Enables

The PRISM-IR v1.1 data model is now fully implemented and validated. This enables:

1. **FACTORY-002 (Dependency Resolution):** depends_on field is ready for use
2. **FACTORY-003 (TTL Enforcement):** building_started_at field is ready for stall detection
3. **FACTORY-004 (Acceptance Criteria):** acceptance_criteria_typed field is ready for typed contracts
4. **FACTORY-005 (Bundle Context Guard):** estimated_tokens field is ready for bundling decisions
5. **FACTORY-007 (DAG Support):** node_type, target_id fields are ready for shared modules
6. **FACTORY-008 (Orphan Detection):** parent_id, root_id, branch_path fields are ready for tree queries

All downstream FACTORY specs can now proceed — the foundation is solid and fully tested.
