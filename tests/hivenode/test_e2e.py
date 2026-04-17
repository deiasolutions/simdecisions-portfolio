"""
test_e2e
========

End-to-end integration tests for all hivenode routes.

This test suite starts a REAL hivenode server in a subprocess and makes REAL HTTP calls
via httpx.AsyncClient (not mocked transport). All data is written to disk, SQLite, etc.

Tests verify the full HTTP → route → business logic → storage → response flow.

Dependencies:
- import pytest
- import httpx
- import asyncio
- import subprocess
- import time
- import socket
- import os
- import sys
- import base64
- from pathlib import Path

Functions:
- find_free_port(): Find a random available port.
- e2e_server(tmp_path_factory): Start a real hivenode server for E2E tests.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
