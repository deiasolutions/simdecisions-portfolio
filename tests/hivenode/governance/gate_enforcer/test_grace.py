"""
test_grace
==========

Tests for grace module.

Dependencies:
- import time
- from hivenode.governance.gate_enforcer.grace import GraceManager
- from hivenode.governance.gate_enforcer.models import (

Functions:
- test_normal_to_grace_active_transition(): Normal → GRACE_ACTIVE transition works correctly.
- test_grace_active_to_normal_on_clean_expiry(): GRACE_ACTIVE → NORMAL on clean expiry (0-1 violations).
- test_grace_active_to_escalation_needed_on_dirty_expiry(): GRACE_ACTIVE → escalation needed on dirty expiry (2+ violations).
- test_already_in_grace_violation_count_increments(): Already in grace: violation count increments, no restart.
- test_end_grace_manually_resets_to_normal(): end_grace manually resets to NORMAL.
- test_four_level_grace_duration_priority_per_agent(): 4-level grace duration priority: per-agent overrides all.
- test_four_level_grace_duration_priority_per_violation(): 4-level grace duration priority: per-violation-type when no agent override.
- test_four_level_grace_duration_priority_per_disposition(): 4-level grace duration priority: per-disposition when no violation-type match.
- test_four_level_grace_duration_priority_global(): 4-level grace duration priority: global default as fallback.
- test_no_grace_gates_return_zero_seconds(): No-grace gates return 0 seconds (no grace granted).
- test_should_escalate_returns_true_when_expired_with_2plus_violations(): should_escalate returns true when expired with 2+ violations.
- test_should_escalate_returns_false_when_clean(): should_escalate returns false when grace expired cleanly.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
