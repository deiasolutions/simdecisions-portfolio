"""
test_early_access_routes
========================

Tests for early access API routes.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from fastapi import FastAPI
- from hivenode.routes.early_access import router, _get_early_access_store
- from hivenode.early_access.store import EarlyAccessStore

Functions:
- store(tmp_path): Create a fresh store with a temp SQLite database.
- app(store): Create a test FastAPI app with early access routes.
- client(app): Create a test client.
- test_post_early_access_success(client): POST /api/early-access with valid email returns 200.
- test_post_early_access_duplicate(client): POST /api/early-access with duplicate email returns 409.
- test_post_early_access_missing_email(client): POST /api/early-access without email returns 422.
- test_post_early_access_empty_email(client): POST /api/early-access with empty email returns 422.
- test_post_early_access_invalid_email(client): POST /api/early-access with invalid email format returns 422.
- test_get_count(client): GET /api/early-access/count returns the signup count.
- test_post_early_access_with_source(client, store): POST /api/early-access respects the source field.
- test_post_early_access_defaults_source(client, store): POST /api/early-access defaults source to 'chat'.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
