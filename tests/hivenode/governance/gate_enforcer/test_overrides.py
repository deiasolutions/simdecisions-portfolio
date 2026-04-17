"""
test_overrides
==============

Tests for overrides module.

Dependencies:
- from datetime import datetime, timedelta, timezone
- from hivenode.governance.gate_enforcer.overrides import OverrideRegistry

Functions:
- test_grant_exemption_creates_valid_exemption(): grant_exemption creates valid exemption with ID.
- test_check_exemption_finds_matching_exemption(): check_exemption finds matching exemption (action + target).
- test_check_exemption_returns_none_when_no_match(): check_exemption returns None when no match.
- test_consume_exemption_decrements_uses_remaining(): consume_exemption decrements uses_remaining.
- test_exhausted_exemption_not_valid(): Exhausted exemption (uses_remaining = 0) is no longer valid.
- test_expired_exemption_not_valid(): Expired exemption is no longer valid.
- test_revoke_exemption_removes_exemption(): revoke_exemption removes exemption.
- test_emergency_stop_halts_agent(): emergency_stop halts agent.
- test_is_halted_returns_true_for_stopped_agent(): is_halted returns true for stopped agent.
- test_resume_agent_resumes_halted_agent(): resume_agent resumes halted agent.
- test_list_exemptions_filters_by_agent_id(): list_exemptions filters by agent_id.
- test_list_exemptions_filters_by_validity(): list_exemptions filters by validity.
- test_cleanup_expired_removes_invalid_exemptions(): cleanup_expired removes invalid exemptions.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
