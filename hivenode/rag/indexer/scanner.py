"""
scanner
=======

File scanner for identifying and classifying artifacts.

This module provides functionality to scan a repository and classify files
by their artifact type. Ported from platform/efemera/src/efemera/indexer/scanner.py.

Dependencies:
- import json
- from pathlib import Path
- from typing import Iterator, Optional
- from hivenode.rag.indexer.models import ArtifactType

Classes:
- Scanner: Scanner for identifying and classifying artifacts in a repository.

Functions:
- _is_phase_ir_file(file_path: Path): Check if a JSON file is a PHASE-IR file.
- scan(repo_path: Path, skip_dirs: Optional[set[str]] = None): Scan a repository and yield (file_path, artifact_type) tuples.
- _detect_type(file_path: Path): Detect artifact type for a file.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
