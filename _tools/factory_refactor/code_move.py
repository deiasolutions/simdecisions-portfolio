"""
code_move
=========

Factory Self-Refactor — Step 2: Code move + import rewrite.

Moves code from shiftcenter into simdecisions packages/ layout, rewrites
Python imports into the simdecisions.* namespace, writes per-package
pyproject.toml files, updates deployment configs.

Non-code conveyance already done by convey.py.

Run from shiftcenter repo root:
    python _tools/factory_refactor/code_move.py

Dependencies:
- from __future__ import annotations
- import re
- import shutil
- import sys
- from pathlib import Path

Functions:
- copy_tree(src: Path, dst: Path): Copy tree with IGNORE, return file count.
- phase_1_copy_code(): Rewrite imports in one .py file. Return number of substitutions.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
