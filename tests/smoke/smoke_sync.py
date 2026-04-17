"""
smoke_sync
==========

Volume Sync Smoke Test

Manual smoke test script that verifies sync works between local hivenode
(localhost:8420) and cloud hivenode (Railway deployment).

Usage: python tests/smoke/smoke_sync.py

Environment variables:
  LOCAL_HIVENODE_URL   - Local hivenode URL (default: http://localhost:8420)
  CLOUD_HIVENODE_URL   - Cloud hivenode URL (default: https://api.shiftcenter.com)

Dependencies:
- import base64
- import os
- import sys
- from datetime import datetime, timezone
- import httpx

Functions:
- check_health(url, name): Check hivenode health endpoint.
- main(): Run smoke test.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
