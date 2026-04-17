"""
routes
======

Moderation queue endpoints — review held messages, approve/reject, resubmit.

Dependencies:
- from typing import Optional
- from fastapi import APIRouter, HTTPException, status, Query, Depends
- from pydantic import BaseModel
- from hivenode.relay import store
- from hivenode.relay.moderation.pipeline import run_pipeline, Decision
- from hivenode.dependencies import verify_jwt_or_local

Classes:
- ModerationQueueEntry: Entry in the moderation queue.
- ReviewAction: Review action (approve or reject).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
