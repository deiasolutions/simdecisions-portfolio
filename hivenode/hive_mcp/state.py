"""
state
=====

Hive MCP state manager - in-memory state with JSON persistence.

Dependencies:
- import json
- import shutil
- import threading
- from pathlib import Path
- from typing import Dict, Any
- from copy import deepcopy

Classes:
- StateManager: Manages hive operational state in memory with JSON backup.

Functions:
- recover_claims_from_active(state_manager: StateManager, repo_root: Path): Recover task claims from _active directory on MCP server startup.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
