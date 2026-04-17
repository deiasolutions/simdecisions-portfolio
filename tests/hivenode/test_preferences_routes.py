"""
test_preferences_routes
=======================

Tests for hivenode user preferences API routes.

Dependencies:
- import os
- import pytest
- from fastapi import FastAPI
- from fastapi.testclient import TestClient
- from hivenode.preferences.store import PreferencesStore
- from hivenode.routes.preferences import router

Classes:
- TestPreferencesRoutes: Tests for GET/PUT /api/user/preferences.

Functions:
- _make_app(store: PreferencesStore): Create a minimal FastAPI app with just the preferences router.
- prefs_client(tmp_path): TestClient with a minimal app (no lifespan port conflicts).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
