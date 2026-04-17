"""
test_database
=============

Tests for simdecisions.database module.

Dependencies:
- import pytest
- import os
- from pathlib import Path

Functions:
- clear_database_state(monkeypatch): Clear database state before each test.
- test_init_database_with_explicit_path(tmp_path): Test that init_database() accepts an explicit db_path parameter.
- test_init_database_no_default_path(): Test that init_database() does not use a default path when called without arguments.
- test_init_database_creates_engine(tmp_path): Test that init_database() creates a SQLAlchemy engine.
- test_init_database_creates_session_local(tmp_path): Test that init_database() creates SessionLocal.
- test_init_database_idempotent(tmp_path): Test that init_database() can be called multiple times without error.
- test_init_database_with_database_url_env_var(monkeypatch, tmp_path): Test that init_database() uses DATABASE_URL env var when db_path is None.
- test_lazy_initialization_with_database_url(monkeypatch, tmp_path): Test that accessing engine/SessionLocal lazily initializes from DATABASE_URL.
- test_no_circular_dependency_simdecisions_to_hivenode(): Test that simdecisions.database does NOT import from hivenode.
- test_get_db_yields_session(tmp_path): Test that get_db() yields a valid session.
- test_get_db_closes_session(tmp_path): Test that get_db() closes session on exit.
- test_base_class_exists(): Test that Base class is available for model definitions.
- test_init_database_with_relative_path_converts_to_absolute(tmp_path, monkeypatch): Test that init_database() converts relative paths to absolute.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
