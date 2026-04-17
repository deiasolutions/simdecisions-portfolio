"""
early_access
============

Early access signup routes.

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException
- from pydantic import BaseModel, EmailStr, field_validator
- from hivenode.early_access.store import EarlyAccessStore
- from hivenode import dependencies

Classes:
- SignupRequest: Early access signup request.

Functions:
- _get_early_access_store(): Dependency: get early access store.
- post_early_access(body: SignupRequest,
    store: EarlyAccessStore = Depends(_get_early_access_store): Register for early access. Public, no auth required.
- get_early_access_count(store: EarlyAccessStore = Depends(_get_early_access_store): Get total early access signup count. Public.
- list_early_access(store: EarlyAccessStore = Depends(_get_early_access_store): List all signups. Admin only (requires auth).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
