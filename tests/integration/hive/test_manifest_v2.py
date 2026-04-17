"""
test_manifest_v2
================

Tests for manifest_v2.py PRISM-IR v1.1 compliance.

Validates that ManifestEntry and manifest I/O functions handle all
extended fields from PRISM-IR Section 10.1 correctly.

Dependencies:
- import pytest
- from datetime import datetime, timezone
- from pathlib import Path
- import json
- import sys
- from manifest_v2 import ManifestEntry, write_manifest, read_manifest, MANIFEST_VERSION

Classes:
- TestManifestEntryPRISMIR: Test ManifestEntry dataclass has all PRISM-IR v1.1 fields.
- TestManifestV2IO: Test manifest v2 read/write functions.
- TestManifestTimestampConversion: Test timestamp conversion between datetime and ISO strings.
- TestManifestV2Example: Test manifest v2 matches PRISM-IR Section 10.1 example format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
