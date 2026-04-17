"""
integrity_check
===============

Queue tree/DAG integrity detection queries.

Implements PRISM-IR v1.1 Section 9 — Orphan Detection.

Provides health-check queries for:
- Incomplete subtrees (descendants not BUILT/INTEGRATED)
- Stalled builds (BUILDING longer than TTL)
- Blocked nodes (status=BLOCKED with unmet dependencies)
- Orphaned nodes (parent INTEGRATED but node not BUILT)
- Dangling refs (SHARED_REF with invalid target_id)
- Circular dependencies (cycles in depends_on graph)

Dependencies:
- import argparse
- import sys
- from datetime import datetime, UTC
- from pathlib import Path
- from spec_parser import SpecFile, parse_spec

Functions:
- _load_all_specs(directories: list[Path]): Load all spec files from multiple directories.
- find_incomplete_subtrees(directory: Path, root_id: str): Find all descendants of root_id that are not BUILT or INTEGRATED.
- find_stalled_nodes(active_dir: Path, ttl_seconds: int = 600): Find nodes in BUILDING phase longer than TTL.
- find_blocked_nodes(directory: Path): Find nodes with status=BLOCKED and their unmet dependencies.
- find_orphaned_nodes(directory: Path): Find nodes whose parent is INTEGRATED but they are not BUILT.
- find_dangling_refs(specs: list[SpecFile]): Find SHARED_REF nodes with invalid target_id.
- find_circular_deps(specs: list[SpecFile]): Find circular dependencies in depends_on graph using DFS with coloring.
- format_markdown_report(incomplete: list[SpecFile],
    stalled: list[SpecFile],
    blocked: list[SpecFile],
    orphaned: list[SpecFile],
    dangling: list[SpecFile],
    cycles: list[list[str]],
    timestamp: str,): Format integrity check results as markdown report.
- main(): CLI entry point for integrity check.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
