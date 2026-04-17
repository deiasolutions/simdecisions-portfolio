"""
test_spec_to_manifest_roundtrip
===============================

Integration test: spec file → SpecFile → ManifestEntry → manifest.json roundtrip.

Validates that the full pipeline from parsing a spec to writing manifest v2
and reading it back preserves all PRISM-IR v1.1 fields.

Dependencies:
- import pytest
- from datetime import datetime, timezone
- from pathlib import Path
- import sys
- from spec_parser import parse_spec
- from manifest_v2 import ManifestEntry, write_manifest, read_manifest

Classes:
- TestSpecToManifestRoundtrip: Test full roundtrip from spec file to manifest and back.
- TestBackwardCompatibilityGuarantee: Verify that all existing specs in backlog can be parsed without errors.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
