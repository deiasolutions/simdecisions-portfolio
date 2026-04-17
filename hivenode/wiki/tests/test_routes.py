"""
test_routes
===========

Integration tests for wiki CRUD API routes.

Dependencies:
- import json
- from datetime import datetime, timezone
- from fastapi.testclient import TestClient
- from hivenode.wiki.store import init_engine, reset_engine

Classes:
- TestCreatePage: Tests for POST /api/wiki/pages.
- TestGetPage: Tests for GET /api/wiki/pages/{path}.
- TestListPages: Tests for GET /api/wiki/pages.
- TestUpdatePage: Tests for PUT /api/wiki/pages/{path}.
- TestDeletePage: Tests for DELETE /api/wiki/pages/{path}.
- TestGetPageHistory: Tests for GET /api/wiki/pages/{path}/history.
- TestGetPageBacklinks: Tests for GET /api/wiki/pages/{path}/backlinks.

Functions:
- _create_test_app(): Create test FastAPI app with wiki routes mounted.
- _setup_db(): Initialize test database.
- _now(): Return current UTC timestamp.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
