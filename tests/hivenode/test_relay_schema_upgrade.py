"""
test_relay_schema_upgrade
=========================

Tests for Efemera schema upgrade (CONN-07).

Covers:
- Channel creation with explicit channel_id
- Extended channel types
- Message creation with new fields
- get_message() function
- Schema init idempotency
- Join/leave channel endpoints

Dependencies:
- import pytest
- from hivenode.relay.store import (

Classes:
- TestSchemaUpgrade: Tests for schema upgrade features.
- TestSchemaUpgradeAPI: API tests for schema upgrade features.

Functions:
- fresh_engine(): Tests for schema upgrade features.
- from_store_list_channels(): Helper to import list_channels.
- client(): Create a test client with relay routes (engine already init'd by autouse fixture).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
