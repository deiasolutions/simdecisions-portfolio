"""
test_rag_route_dedup
====================

Test RAG route deduplication (SPEC-RAG-DEDUP-001).

Verifies that RAG endpoints are registered exactly once at /api/rag/*.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app

Classes:
- TestRagRouteDeduplication: Verify no duplicate RAG route registrations.
- TestRagEndpointsAvailable: Verify all RAG endpoints respond correctly.

Functions:
- client(): Create TestClient for full app integration testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
