"""
dispatch
========

Dispatch tools for Hive MCP.

Dependencies:
- import sys
- import subprocess
- from pathlib import Path
- from datetime import datetime
- from typing import Dict, Any

Functions:
- _find_repo_root(start_path: Path | None = None): Find repository root by looking for .deia directory.
- dispatch_bee(task_file: str,
    model: str = "haiku",
    role: str = "bee",
    inject_boot: bool = True,
    repo_root: Path | None = None): Dispatch a bee via subprocess (wraps dispatch.py).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
