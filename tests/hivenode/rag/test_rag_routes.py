"""
test_rag_routes
===============

Tests for RAG API routes.

Dependencies:
- import tempfile
- from pathlib import Path
- from unittest.mock import patch
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.rag.engine import RagEngine

Classes:
- TestStatusRoute: Smoke tests for POST /rag/query endpoint.

Functions:
- mock_embed_texts(texts: list[str]): Create a minimal FastAPI app with RAG routes for testing.
- client(test_app): Smoke tests for POST /rag/query endpoint.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
