"""
test_early_access_store
=======================

Tests for early access signup store.

Dependencies:
- import pytest
- from hivenode.early_access.store import EarlyAccessStore

Functions:
- store(tmp_path): Create a fresh store with a temp SQLite database.
- test_add_signup_success(store): Adding a new email returns (True, 'registered').
- test_add_signup_duplicate(store): Adding the same email twice returns (False, 'already registered').
- test_add_signup_defaults(store): Comment defaults to empty, source defaults to 'chat'.
- test_list_all(store): list_all returns all signups in insertion order.
- test_count(store): count returns total number of signups.
- test_count_excludes_duplicates(store): Duplicate attempts don't inflate the count.
- test_created_at_populated(store): created_at is populated with an ISO timestamp.
- test_list_all_includes_all_fields(store): Each row dict has id, email, comment, source, created_at.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
