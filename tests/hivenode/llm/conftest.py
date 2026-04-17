"""
conftest
========

Pytest configuration for LLM router tests.

Dependencies:
- import pytest
- import tempfile
- import os
- from cryptography.fernet import Fernet
- from hivenode.llm.config import RouterConfig
- from hivenode.llm.byok import BYOKStore
- from hivenode.ledger.writer import LedgerWriter

Functions:
- temp_db(): Create temporary database for testing.
- temp_ledger_db(): Create temporary database for ledger.
- temp_byok_db(): Create temporary database for BYOK store.
- fernet_key(): Generate Fernet encryption key for testing.
- byok_store(temp_byok_db, fernet_key): Create BYOK store for testing.
- ledger_writer(temp_ledger_db): Create ledger writer for testing.
- router_config(): Create router config for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
