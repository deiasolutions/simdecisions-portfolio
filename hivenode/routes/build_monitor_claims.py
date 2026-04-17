"""
build_monitor_claims
====================

File claim management module — parallel bee deconfliction.

Handles file claim tracking, FIFO wait queues, and claim expiration.
This module contains the claim-related business logic separated from core heartbeat.

Dependencies:
- from datetime import datetime
- from typing import Optional
- from pydantic import BaseModel

Classes:
- ClaimPayload: Remove claims older than CLAIM_STALE_SECONDS, promote waiters.

Functions:
- expire_stale_claims(claims: dict[str, dict], claim_waiters: dict[str, list[str]]): Remove claims older than CLAIM_STALE_SECONDS, promote waiters.
- promote_waiter(claims: dict[str, dict],
    claim_waiters: dict[str, list[str]],
    path: str,
    tasks: dict[str, dict] | None = None,): Promote the next FIFO waiter to claim holder for a path.
- claim_files(task_id: str,
    files: list[str],
    claims: dict[str, dict],
    claim_waiters: dict[str, list[str]],): Claim files for a task.
- release_claims(task_id: str,
    files: Optional[list[str]],
    claims: dict[str, dict],
    claim_waiters: dict[str, list[str]],
    tasks: dict[str, dict],): Release claims held by a task, promote FIFO waiters.
- get_claims(claims: dict[str, dict], claim_waiters: dict[str, list[str]]): Return all active claims and wait queues.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
