"""
test_reader
===========

Tests for ledger reader - query interface.

Dependencies:
- import tempfile
- from pathlib import Path
- from datetime import datetime

Functions:
- test_query_by_event_type(): Test querying events by event_type.
- test_query_by_actor(): Test querying events by actor.
- test_query_by_domain(): Test querying events by domain.
- test_query_by_time_range(): Test querying events by time range.
- test_query_empty_ledger(): Test querying an empty ledger returns empty list.
- test_query_with_multiple_filters(): Test combining multiple filters.
- test_query_by_signal_type(): Test querying by signal_type.
- test_query_by_oracle_tier(): Test querying by oracle_tier.
- test_get_event_by_id(): Test retrieving a single event by ID.
- test_get_nonexistent_event(): Test getting an event that doesn't exist returns None.
- test_count_events(): Test counting events with filters.
- test_context_manager(): Test that LedgerReader works as context manager.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
