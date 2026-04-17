"""
convey
======

Factory Self-Refactor — Step 1: Convey non-code content.

Copies non-code content from shiftcenter into simdecisions.
Code directories (browser, hivenode, engine, hodeia_auth, _tools) are NOT
copied here — that's step 2 (code_move.py).

Per SPEC-FACTORY-SELF-REFACTOR-001 Conveyance Rule: all non-code content
carries forward unchanged, including secrets, logs, and state.

Run from shiftcenter repo root:
    python _tools/factory_refactor/convey.py

Dependencies:
- from __future__ import annotations
- import shutil
- import sys
- from pathlib import Path

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
