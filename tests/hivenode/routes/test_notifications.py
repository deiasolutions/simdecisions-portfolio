"""
test_notifications
==================

Tests for GET /build/notifications endpoint.

Test coverage:
- Returns last 100 notifications from build monitor
- Notification types: build_event, inventory_update, system_alert
- Reverse-chronological sort (newest first)
- Empty response when no notifications
- HTTP error handling

Dependencies:
- from datetime import datetime
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- test_get_notifications_empty(): GET /build/notifications returns empty list when no notifications.
- test_get_notifications_returns_build_events(): GET /build/notifications includes build events from monitor.
- test_get_notifications_reverse_chronological(): GET /build/notifications returns newest notifications first.
- test_notification_structure_complete(): Notification has all required fields with correct types.
- test_notification_types_supported(): Notification types: build_event, inventory_update, system_alert.
- test_notifications_limit_100(): GET /build/notifications returns at most 100 notifications.
- test_notification_default_unread(): New notifications default to read=false.
- test_notification_timestamp_iso8601(): Notification timestamp is ISO 8601 format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
