"""
test_spec_parser_prism_ir
=========================

Tests for spec_parser.py PRISM-IR v1.1 compliance.

Validates that SpecFile dataclass and parser handle all extended fields
from PRISM-IR Section 1.1 correctly.

Dependencies:
- from PRISM-IR Section 1.1 correctly.
- from pathlib import Path
- import sys
- from spec_parser import SpecFile, parse_spec

Classes:
- TestPRISMIRv11Fields: Test PRISM-IR v1.1 extended fields in SpecFile.
- TestFrontmatterParserPRISMIR: Test YAML frontmatter parsing for PRISM-IR v1.1 fields.
- TestLegacyParserBackwardCompat: Test backward compatibility with old-format specs (no frontmatter).
- TestBranchPathParsing: Test parsing of branch_path field in various formats.
- TestDependsOnParsing: Test parsing of depends_on field (non-parent dependencies).
- TestAcceptanceCriteriaTyped: Test parsing of acceptance_criteria_typed field.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
