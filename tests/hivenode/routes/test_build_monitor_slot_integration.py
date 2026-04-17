"""
test_build_monitor_slot_integration
===================================

Integration tests for slot reservation system — queue runner + hivenode API.

Dependencies:
- import pytest
- from hivenode.routes.build_monitor import BuildState

Classes:
- TestQueueRunnerSlotIntegration: Test integration between queue runner slot operations and hivenode API.
- TestSlotBackfillIntegration: Test queue runner backfill logic with slot reservation.
- TestSlotReservationPersistence: Test slot reservation state persists across restarts.
- TestSlotOversubscriptionPrevention: Test slot reservation prevents oversubscription.
- TestEdgeCases: Test edge cases in slot management.

Functions:
- temp_state_file(tmp_path): Create a temporary state file for testing.
- state(temp_state_file): Create a fresh BuildState with temp file.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
