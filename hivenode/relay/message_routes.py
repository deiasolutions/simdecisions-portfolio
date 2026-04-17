"""
message_routes
==============

Efemera message versioning and threading API routes.

Dependencies:
- from fastapi import APIRouter, HTTPException, status, Depends
- from pydantic import BaseModel, Field
- from hivenode.relay import store
- from hivenode.dependencies import verify_jwt_or_local

Classes:
- EditMessageRequest: Edit a message, creating a new version. Only the sender can edit.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
