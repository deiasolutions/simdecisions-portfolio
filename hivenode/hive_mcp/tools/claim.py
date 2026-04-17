"""
claim
=====

Claim/release tools for Hive MCP (Phase 1 write tools).

File-based claim/release system:
- mcp_claim_task: Move spec from queue/backlog to _active
- mcp_release_task: Move spec from _active to _done/_dead/backlog

Dependencies:
- import shutil
- from pathlib import Path
- from typing import Dict, Any, Literal
- from datetime import datetime, timezone

Functions:
- _find_repo_root(): Find repository root by looking for .deia directory.
- mcp_claim_task(spec_id: str,
    bee_id: str,
    state_manager: Any): Claim a spec (file-based claim).
- mcp_release_task(spec_id: str,
    reason: Literal["done", "failed", "timeout"],
    state_manager: Any): Release a claimed spec.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
