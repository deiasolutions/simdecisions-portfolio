"""
sync_routes
===========

Sync HTTP Routes

Routes for triggering sync, checking status, and resolving conflicts.

Dependencies:
- from fastapi import APIRouter, Request, HTTPException, Query
- from pydantic import BaseModel
- from typing import Optional, List
- from hivenode.sync.engine import SyncEngine
- from hivenode.sync.sync_log import SyncLog
- from hivenode.sync.outbox import SyncOutbox

Classes:
- SyncTriggerRequest: Request body for POST /sync/trigger.
- SyncTriggerResponse: Response for POST /sync/trigger.
- SyncStatusResponse: Response for GET /sync/status.
- ConflictEntry: Single conflict entry.
- SyncConflictsResponse: Response for GET /sync/conflicts.
- SyncResolveRequest: Request body for POST /sync/resolve.
- SyncResolveResponse: Response for POST /sync/resolve.
- OutboxEntry: Single outbox entry.
- SyncPullResponse: Response for GET /sync/pull.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
