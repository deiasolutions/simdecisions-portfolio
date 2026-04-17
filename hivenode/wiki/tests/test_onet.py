"""
test_onet
=========

Tests for ONET integration.

Dependencies:
- import pytest
- from sqlalchemy import select
- from hivenode.wiki.store import (
- from hivenode.wiki.onet_seed import seed_sample_onet_data

Functions:
- setup_db(): Initialize in-memory database for each test.
- test_onet_tables_created(): Test that ONET tables are created during init.
- test_seed_sample_onet_data(): Test seeding sample ONET data.
- test_query_occupation(): Test querying occupation by SOC code.
- test_query_occupation_skills(): Test querying skills for an occupation.
- test_query_ai_exposure(): Test querying AI exposure data.
- test_query_wage_data(): Test querying wage data.
- test_high_ai_exposure_occupations(): Test finding occupations with high AI exposure.
- test_occupation_skills_join(): Test joining occupations with skills.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
