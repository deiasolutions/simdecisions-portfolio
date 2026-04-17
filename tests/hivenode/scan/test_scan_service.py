"""
test_scan_service
=================

Tests for SCAN service functionality.

Dependencies:
- import pytest
- from datetime import datetime, timedelta
- from sqlalchemy import create_engine
- from sqlalchemy.orm import sessionmaker
- from hivenode.scan.models import Base, ScanSource, ScanItem, ScanDigest
- from hivenode.scan.service import ScanService
- from hivenode.scan.adapters import RSSAdapter, HackerNewsAdapter

Functions:
- db_session(): Create an in-memory test database.
- scan_service(db_session): Create a SCAN service with test database.
- test_create_source(db_session, scan_service): Test creating a scan source.
- test_get_adapter_rss(db_session, scan_service): Test getting RSS adapter from source.
- test_get_adapter_hackernews(db_session, scan_service): Test getting HackerNews adapter from source.
- test_get_adapter_unknown_type(db_session, scan_service): Test error handling for unknown source type.
- test_create_scan_item(db_session): Test creating a scan item.
- test_create_scan_digest(db_session): Test creating a scan digest.
- test_score_relevance_no_llm(db_session, scan_service): Test relevance scoring without LLM returns default score.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
