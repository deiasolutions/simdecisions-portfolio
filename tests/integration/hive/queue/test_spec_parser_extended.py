"""
test_spec_parser_extended
=========================

Tests for extended SpecFile dataclass with PRISM-IR v1.1 fields.

Verifies that all new fields from PRISM-IR Section 1.1 are present
and parsed correctly from YAML frontmatter.

Dependencies:
- from datetime import datetime
- from pathlib import Path
- from dataclasses import fields
- import sys
- from spec_parser import SpecFile, parse_spec

Functions:
- test_specfile_has_all_prism_ir_fields(): Verify SpecFile dataclass has all required PRISM-IR v1.1 fields.
- test_parse_spec_with_minimal_fields(tmp_path): Old-format spec with minimal fields should parse with sensible defaults.
- test_parse_spec_with_all_prism_ir_fields(tmp_path): New-format spec with all PRISM-IR fields parses correctly.
- test_parse_spec_shared_ref_type(tmp_path): Spec with node_type=SHARED_REF parses correctly.
- test_parse_spec_phase_enum_values(tmp_path): All phase enum values parse correctly.
- test_parse_spec_status_enum_values(tmp_path): All status enum values parse correctly.
- test_parse_spec_output_type_values(tmp_path): Both output_type values parse correctly.
- test_parse_spec_with_building_timestamp(tmp_path): Spec with building_started_at timestamp parses correctly.
- test_parse_spec_with_failure_info(tmp_path): Spec with failure_reason and split_reason parses correctly.
- test_parse_spec_content_types(tmp_path): Various content_type values parse correctly.
- test_backward_compatibility_legacy_format(tmp_path): Legacy markdown header format still works without new fields.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
