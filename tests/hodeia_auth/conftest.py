"""
conftest
========

Test fixtures for hodeia_auth authentication service tests.

Dependencies:
- import pytest
- import pytest_asyncio
- from pathlib import Path
- import tempfile
- from unittest.mock import MagicMock, patch
- from cryptography.hazmat.primitives import serialization
- from cryptography.hazmat.primitives.asymmetric import rsa
- from cryptography.hazmat.backends import default_backend
- from httpx import AsyncClient, ASGITransport
- from sqlalchemy import create_engine

Functions:
- rsa_key_pair(): Generate ephemeral RSA 2048-bit key pair for tests.
- test_db(): Create in-memory SQLite database for tests.
- test_ledger_db(): Create in-memory Event Ledger database for tests.
- session(test_db): Get database session for tests.
- mock_twilio(): Mock Twilio Verify client.
- mock_twilio_fail(): Mock Twilio Verify client that returns failure.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
