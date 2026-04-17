"""
test_estimates_schema
=====================

Tests for estimation calibration schema (inv_estimates and inv_calibration tables).

TDD: Tests written first, then implementation.
Coverage: table creation, columns, types, indexes, migrations, unique constraints.

Dependencies:
- import pytest
- import tempfile
- from sqlalchemy import (
- from sqlalchemy.exc import IntegrityError
- from hivenode.inventory import store

Classes:
- TestEstimatesTableSchema: Test inv_estimates table structure and constraints.
- TestCalibrationTableSchema: Test inv_calibration table structure and constraints.
- TestMigrationIdempotency: Test that migrations can be run multiple times safely.
- TestBothTablesExist: Integration test: verify both tables exist and are independent.
- TestPostgreSQLCompatibility: Test schema compatibility with PostgreSQL (if running on Railway).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
