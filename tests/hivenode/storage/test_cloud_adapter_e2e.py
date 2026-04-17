"""
test_cloud_adapter_e2e
======================

End-to-end integration tests for cloud:// storage adapter.

This test suite verifies CloudAdapter integration with storage routes using TWO approaches:

1. **Storage Routes E2E (local mode server)**: Starts a real hivenode server in LOCAL MODE
   and tests storage routes with a persistent volume. This verifies the HTTP → routes →
   transport → adapter → disk stack works correctly. Uses JWT dependency override.

2. **CloudAdapter Integration (respx mocking)**: Tests CloudAdapter HTTP client behavior
   with mocked HTTP responses to verify offline handling, error cases, and sync queue.

NOTE: Full cloud mode E2E tests (with JWKS infrastructure) are skipped because cloud mode
startup requires JWKS endpoint availability and hangs during lifespan initialization.
The hybrid approach provides equivalent coverage without infrastructure complexity.

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
- import respx

Functions:
- find_free_port(): Find a random available port.
- cloud_e2e_server(tmp_path_factory): Start a real hivenode server in LOCAL MODE for E2E tests.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
