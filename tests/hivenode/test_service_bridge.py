"""
test_service_bridge
===================

Tests for ServiceBridge base class.

Tests cover:
- Basic start/stop lifecycle
- Restart on crash with exponential backoff
- Rate limiting (max 5 restarts per 10 minutes)
- Manual wake() after rate limit
- Wake event propagation
- Error notification to /build/heartbeat

Dependencies:
- import asyncio
- import pytest
- import threading
- import time
- from pathlib import Path
- from unittest.mock import Mock, patch
- from hivenode.service_bridge import ServiceBridge

Classes:
- TestServiceBridge: Test implementation of ServiceBridge.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
