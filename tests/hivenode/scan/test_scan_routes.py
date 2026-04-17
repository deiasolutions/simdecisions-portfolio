"""
test_scan_routes
================

Tests for SCAN API routes.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from sqlalchemy import create_engine
- from sqlalchemy.orm import sessionmaker
- from hivenode.main import app
- from hivenode.scan.models import Base, ScanSource
- from hivenode.scan.store import init_engine, get_session
- from hivenode.scan.routes import get_scan_service

Functions:
- test_db(): Create test database.
- client(): Create test client.
- test_list_sources_empty(client, test_db): Test listing sources when none exist.
- test_create_source(client, test_db): Test creating a new source.
- test_list_sources_with_data(client, test_db): Test listing sources after creating one.
- test_list_items_empty(client, test_db): Test listing items when none exist.
- test_get_nonexistent_item(client, test_db): Test getting item that doesn't exist.
- test_list_digests_empty(client, test_db): Test listing digests when none exist.
- test_get_nonexistent_digest(client, test_db): Test getting digest that doesn't exist.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
