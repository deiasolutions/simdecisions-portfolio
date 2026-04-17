"""
store
=====

Analytics store — SQLAlchemy Core tables + CRUD functions.

Single source of truth for pageview analytics data.
Follows the same pattern as hivenode/inventory/store.py.

Dependencies:
- import uuid
- from datetime import datetime, timezone, timedelta
- from urllib.parse import urlparse
- from sqlalchemy import (
- from sqlalchemy.pool import StaticPool

Functions:
- init_engine(url: str, force: bool = False): Initialize the analytics store engine. Called once at startup.
- get_engine(): Get the current engine. Raises if not initialized.
- reset_engine(): For tests only — reset global engine.
- _migrate_schema(eng): Add missing columns to inv_pageviews if they exist (idempotent).
- _now(): Extract domain from referrer URL for grouping.
- record_pageview(domain: str,
    path: str,
    referrer: str | None,
    user_agent: str | None,
    country: str | None,
    screen_w: int | None,
    session_id: str | None,): Insert one pageview row. Returns the generated id.
- get_stats(domain: str | None = None, days: int = 30): Return aggregated stats: total_views, unique_sessions, top_pages, referrers, visits_per_day, geo_breakdown.
- get_top_pages(domain: str | None = None, days: int = 30, limit: int = 20): Return [{'path': '/blog/...', 'views': 89}, ...] ordered by views desc.
- get_referrers(domain: str | None = None, days: int = 30, limit: int = 20): Return [{'referrer': 'linkedin.com', 'views': 112}, ...]. Group by domain portion of referrer.
- get_visits_per_day(domain: str | None = None, days: int = 30): Return [{'date': '2026-04-09', 'views': 52, 'sessions': 31}, ...].
- get_geo_breakdown(domain: str | None = None, days: int = 30, limit: int = 20): Return [{'country': 'US', 'views': 201}, ...] ordered by views desc.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
