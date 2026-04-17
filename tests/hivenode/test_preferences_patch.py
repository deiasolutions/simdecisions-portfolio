"""
test_preferences_patch
======================

Test preferences route patch semantics.

SPEC-HHPANES-003: Settings Backend Persistence

Dependencies:
- import os
- import pytest
- from fastapi import FastAPI
- from fastapi.testclient import TestClient
- from hivenode.preferences.store import PreferencesStore
- from hivenode.routes.preferences import router

Functions:
- _make_app(store: PreferencesStore): Create a minimal FastAPI app with just the preferences router.
- prefs_client(tmp_path): TestClient with a minimal app (no lifespan port conflicts).
- test_preferences_patch_semantics(prefs_client): Test that PUT /api/user/preferences merges instead of replacing.
- test_preferences_partial_overwrite(prefs_client): Test that incoming values win on conflicts.
- test_preferences_fetch_after_patch(prefs_client): Test that GET reflects merged preferences.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
