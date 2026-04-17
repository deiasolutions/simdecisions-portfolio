"""
test_aggregation
================

Tests for ledger aggregation - cost tracking by task, actor, sprint.

Dependencies:
- import tempfile
- from pathlib import Path

Functions:
- test_aggregate_cost_by_actor(): Test cost aggregation by actor.
- test_aggregate_cost_by_task(): Test cost aggregation by task (using target field).
- test_aggregate_cost_by_domain(): Test cost aggregation by domain.
- test_aggregate_with_none_costs(): Test aggregation handles None costs correctly.
- test_aggregate_zero_vs_none_carbon(): Test that zero carbon is aggregated differently from None.
- test_aggregate_empty_ledger(): Test aggregation on empty ledger returns empty dict.
- test_aggregate_cost_by_time_range(): Test cost aggregation within a time range.
- test_total_cost(): Test getting total cost across all events.
- test_get_total_cost_returns_directional_tokens(): Test that get_total_cost returns tokens_up and tokens_down.
- test_aggregate_by_actor_includes_directional_tokens(): Test that aggregate_cost_by_actor includes tokens_up and tokens_down.
- test_aggregation_handles_null_directional_tokens(): Test that aggregation handles NULL directional tokens from old events.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
