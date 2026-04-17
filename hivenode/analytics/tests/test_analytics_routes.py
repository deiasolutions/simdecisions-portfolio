"""
test_analytics_routes
=====================

Integration tests for analytics routes.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from unittest.mock import patch
- from hivenode.main import app
- from hivenode.analytics import store
- from hivenode.routes import analytics_routes

Functions:
- setup_analytics_db(): Set up in-memory SQLite for each test.
- client(): Create test client.
- reset_rate_limiter(): Reset rate limiter between tests.
- test_beacon_happy_path(client, reset_rate_limiter): Beacon accepts valid pageview and returns 204.
- test_beacon_missing_path_field(client, reset_rate_limiter): Beacon rejects request missing required 'path' field.
- test_beacon_bad_domain(client, reset_rate_limiter): Beacon silently drops request from non-allowed domain.
- test_beacon_localhost_allowed(client, reset_rate_limiter): Beacon accepts localhost for dev testing.
- test_beacon_extracts_domain_from_referer(client, reset_rate_limiter): Beacon falls back to Referer header when Origin missing.
- test_beacon_unknown_domain_fallback(client, reset_rate_limiter): Beacon handles missing Origin/Referer headers (unknown domain).
- test_beacon_rate_limiting(client, reset_rate_limiter): Beacon enforces 60 requests per minute per IP.
- test_beacon_rate_limit_resets(client, reset_rate_limiter): Beacon rate limit window resets after 60 seconds.
- test_beacon_optional_fields(client, reset_rate_limiter): Beacon accepts request with only required 'path' field.
- test_beacon_store_error_still_returns_204(client, reset_rate_limiter): Beacon returns 204 even if store write fails (never break page load).
- test_stats_endpoint_local_mode(mock_settings, client): Stats endpoint works in local mode without auth.
- test_stats_endpoint_filter_by_domain(mock_settings, client): Stats endpoint filters results by domain.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
