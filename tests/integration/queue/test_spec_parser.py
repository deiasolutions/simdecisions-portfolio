"""
test_spec_parser
================

Tests for spec_parser module.

Test-driven development for the spec parser that extracts structured
metadata from markdown spec files.

Dependencies:
- import pytest
- from pathlib import Path
- from dataclasses import dataclass
- from hivenode.spec_parser import parse_spec, SpecParseError

Classes:
- SpecFile: Helper to create temporary spec files for testing.

Functions:
- create_spec_file(tmp_path: Path, filename: str, content: str): Create a temporary spec file for testing.
- test_parse_valid_spec_with_all_fields(tmp_path): Test parsing a complete, well-formed spec file.
- test_parse_spec_missing_priority_raises_error(tmp_path): Test that missing priority field raises SpecParseError.
- test_parse_spec_with_no_acceptance_criteria(tmp_path): Test spec with no acceptance criteria returns empty list.
- test_parse_spec_with_mixed_checkbox_states(tmp_path): Test parsing specs with mix of checked and unchecked boxes.
- test_parse_spec_missing_spec_id_raises_error(tmp_path): Test that missing Spec ID raises SpecParseError.
- test_parse_spec_with_no_dependencies(tmp_path): Test spec without dependencies section.
- test_parse_spec_with_priority_in_section_format(tmp_path): Test parsing priority from '## Priority' section.
- test_parse_spec_file_not_found_raises_error(tmp_path): Test that nonexistent file raises appropriate error.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
