"""
test_wiki_schema
================

Test wiki database schema (SQLAlchemy Core).

Tests table creation, column types, indexes, and idempotent migrations.
Follows the same pattern as inventory/tests/test_inventory_schema_*.py.

Dependencies:
- import pytest
- from sqlalchemy import create_engine, inspect
- from sqlalchemy.pool import StaticPool

Functions:
- wiki_engine(): Create fresh in-memory SQLite database for each test.
- test_tables_created_on_fresh_db(wiki_engine): Verify that both wiki_pages and wiki_edit_log tables are created.
- test_wiki_pages_columns_exist(wiki_engine): Verify all required columns exist in wiki_pages table.
- test_wiki_pages_column_types(wiki_engine): Verify column types are Text and Integer (SQLite/PostgreSQL compatible).
- test_wiki_pages_nullability(wiki_engine): Verify required columns are NOT NULL.
- test_wiki_edit_log_columns_exist(wiki_engine): Verify all required columns exist in wiki_edit_log table.
- test_wiki_edit_log_column_types(wiki_engine): Verify edit_log column types are Text (SQLite/PostgreSQL compatible).
- test_wiki_edit_log_nullability(wiki_engine): Verify required edit_log columns are NOT NULL.
- test_indexes_created(wiki_engine): Verify indexes exist on key columns.
- test_init_engine_idempotent(wiki_engine): Verify calling init_engine twice doesn't error.
- test_migrate_schema_adds_missing_columns(wiki_engine): Verify _migrate_schema adds columns that are missing from existing tables.
- test_insert_wiki_page_basic(wiki_engine): Verify we can insert a basic wiki page.
- test_insert_wiki_edit_log_basic(wiki_engine): Verify we can insert a basic edit log entry.
- test_default_values_applied(wiki_engine): Verify server defaults are applied for optional columns.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
