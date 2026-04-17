"""
routes
======

Wiki CRUD API routes.

Dependencies:
- import json
- import uuid
- import hashlib
- from datetime import datetime, timezone
- from fastapi import APIRouter, Depends, HTTPException, status
- from sqlalchemy import select, insert, update as sql_update, and_
- from hivenode.dependencies import verify_jwt_or_local
- from hivenode.wiki.store import get_engine, wiki_pages, wiki_edit_log
- from hivenode.wiki.parser import parse_wikilinks, parse_frontmatter
- from hivenode.ledger.emitter import emit_event

Functions:
- _now(): Return current UTC timestamp in ISO 8601 format.
- _row_to_page_response(row): Convert SQLAlchemy row to PageResponse.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
