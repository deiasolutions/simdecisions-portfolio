"""
test_analytics_store
====================

Tests for analytics store module.

Dependencies:
- import pytest
- from datetime import datetime, timezone, timedelta
- from hivenode.analytics.store import (

Functions:
- store(): Initialize in-memory SQLite store for tests.
- test_init_engine_creates_table(store): Test that init_engine creates the inv_pageviews table.
- test_record_pageview_basic(store): Test recording a basic pageview.
- test_record_pageview_minimal(store): Test recording pageview with minimal fields.
- test_get_stats_empty_table(store): Test get_stats on empty table.
- test_get_stats_with_data(store): Test get_stats with pageview data.
- test_get_stats_domain_filter(store): Test get_stats with domain filtering.
- test_get_top_pages(store): Test get_top_pages aggregation.
- test_get_top_pages_limit(store): Test get_top_pages respects limit parameter.
- test_referrer_domain_extraction(): Test _extract_referrer_domain helper.
- test_get_referrers(store): Test get_referrers aggregation and domain grouping.
- test_get_referrers_limit(store): Test get_referrers respects limit.
- test_get_visits_per_day(store): Test get_visits_per_day aggregation.
- test_get_visits_per_day_duplicate_sessions(store): Test that unique session counting works correctly per day.
- test_get_geo_breakdown(store): Test get_geo_breakdown aggregation.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
