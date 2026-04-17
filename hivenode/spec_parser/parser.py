"""
parser
======

Parser for markdown spec files.

Dependencies:
- import re
- from dataclasses import dataclass
- from pathlib import Path

Classes:
- SpecParseError: Raised when spec file cannot be parsed.
- ParsedSpec: Structured metadata extracted from a spec file.

Functions:
- parse_spec(path: Path): Parse a spec file and extract structured metadata.
- _extract_spec_id(content: str, path: Path): Extract Spec ID from frontmatter.
- _extract_priority(content: str, path: Path): Extract priority from frontmatter or section.
- _extract_model(content: str): Extract model assignment from spec.
- _extract_dependencies(content: str): Extract dependency list from spec.
- _extract_status(content: str): Extract status from frontmatter.
- _extract_acceptance_criteria(content: str): Extract acceptance criteria checkboxes from spec.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
