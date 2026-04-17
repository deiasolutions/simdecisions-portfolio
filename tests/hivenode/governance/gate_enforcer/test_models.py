"""
test_models
===========

Tests for gate_enforcer models.

Dependencies:
- from datetime import datetime, timedelta, timezone
- from hivenode.governance.gate_enforcer.models import (

Functions:
- test_disposition_enum_has_five_values(): Disposition enum has 5 values: PASS, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN.
- test_violation_type_enum_has_seven_values(): ViolationType enum has 7 values.
- test_agent_ethics_defaults(): AgentEthics defaults are correct.
- test_agent_ethics_with_require_human_conditions(): AgentEthics can be created with require_human_conditions.
- test_grace_state_active_property_normal(): GraceState.active returns False when status is NORMAL.
- test_grace_state_active_property_grace_active(): GraceState.active returns True when status is GRACE_ACTIVE and not expired.
- test_grace_state_active_property_grace_expired(): GraceState.active returns False when grace period has expired.
- test_grace_state_expired_property(): GraceState.expired returns True when grace period has expired.
- test_grace_state_expired_property_not_expired(): GraceState.expired returns False when still active.
- test_exemption_valid_property_with_uses_remaining(): Exemption.valid returns True when uses remain and not expired.
- test_exemption_valid_property_exhausted(): Exemption.valid returns False when uses_remaining is 0.
- test_exemption_valid_property_expired(): Exemption.valid returns False when expiry time has passed.
- test_check_result_construction(): CheckResult can be constructed with all fields.
- test_grace_config_defaults(): GraceConfig defaults are correct.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
