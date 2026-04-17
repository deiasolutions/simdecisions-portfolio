"""
shell
=====

Shell execution routes.

Dependencies:
- from fastapi import APIRouter, HTTPException, Depends, status
- from hivenode.config import settings
- from hivenode.dependencies import get_ledger_writer, get_volume_registry, verify_jwt_or_local
- from hivenode.ledger.writer import LedgerWriter
- from hivenode.storage.registry import VolumeRegistry
- from hivenode.storage.resolver import PathResolver
- from hivenode.shell.executor import ShellExecutor
- from hivenode.shell.allowlist import is_allowed
- from hivenode.shell.schemas import ShellExecRequest, ShellExecResponse

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
