"""
test_relay_smoke
================

Efemera smoke test — runs through the full messaging flow.

Usage:
    python tests/hivenode/test_efemera_smoke.py [--url http://localhost:8420]

Starts hivenode if not already running, then exercises:
  1. List default channels
  2. Create a new channel
  3. Send messages
  4. Read messages back
  5. Poll with ?since=
  6. Add members
  7. Update presence
  8. Print summary

NOTE: This test assumes the server runs in local mode (no auth required).
In local mode, identity comes from verify_jwt_or_local() which returns
a local claims dict. Request bodies no longer include author/user fields.

Dependencies:
- import argparse
- import json
- import subprocess
- import sys
- import time
- import urllib.request
- import urllib.error

Functions:
- req(method: str, url: str, data: dict | None = None): Make an HTTP request, return (status, json_body).
- wait_for_server(base: str, retries: int = 10): Poll /health until server is up.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
