"""
test_production_api
===================

Smoke tests for production API endpoints.

Run against deployed production URL (configurable via DEPLOY_URL env var).
Tests verify health endpoint and protected route rejection.

Usage:
    pytest tests/smoke/test_production_api.py -v
    DEPLOY_URL=https://shiftcenter.com pytest tests/smoke/test_production_api.py -v

Dependencies:
- import pytest
- import httpx
- import os

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
