"""
pie
===

PIE (PHASE-IR Egg) -- a directory-based package format for distributing
PHASE-IR flows.  One PIE = one flow.

Standard PIE layout:
    <name>/
        manifest.yaml       -- package metadata
        intent.md           -- human-readable intent description
        flow.phase          -- the PHASE-IR flow (YAML)
        config/             -- runtime configuration profiles
        tests/              -- scenarios, expected outputs, fixtures
        traces/             -- execution trace logs
        checkpoints/        -- checkpoint snapshots
        render/             -- visual theme and layout
        data/               -- data manifests
        optimization/       -- objectives, decisions, constraints
        provenance/         -- provenance records

Dependencies:
- from __future__ import annotations
- import os
- import shutil
- import uuid
- import zipfile
- from dataclasses import dataclass, field
- from datetime import datetime, timezone
- from pathlib import Path
- import yaml
- from .primitives import Flow

Classes:
- PIEManifest: Metadata for a PIE package.

Functions:
- create_pie_scaffold(name: str,
    base_dir: str,
    intent: str = "",
    author: str = "",): Create a new PIE directory scaffold with all standard subdirectories
- load_pie(pie_dir: str): Load a PIE from a directory.
- save_pie(pie_dir: str, manifest: PIEManifest, flow: Flow): Save manifest and flow to an existing PIE directory.
- validate_pie(pie_dir: str): Validate a PIE directory structure.
- pack_pie(pie_dir: str, output_path: str): Pack a PIE directory into a .pie.zip archive.
- unpack_pie(archive_path: str, output_dir: str): Extract a .pie.zip archive to a directory.
- read_intent(pie_dir: str): Read the intent.md file from a PIE directory.
- write_intent(pie_dir: str, intent: str): Write the intent.md file in a PIE directory.
- inject_workbench(pie_dir: str, workbench_html_path: str): Inject a workbench.html file into a PIE directory and update manifest.
- prepare_workbench(pie_dir: str): Prepare and validate a workbench installation for a PIE.
- get_pie_info(pie_dir: str): Return a summary dict for a PIE:
- _write_text(path: str, content: str): Write text to a file with UTF-8 encoding.
- _write_manifest(pie_dir: str, manifest: PIEManifest): Serialize and write a PIEManifest to manifest.yaml.
- _read_manifest(pie_dir: str): Read and parse manifest.yaml into a PIEManifest.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
