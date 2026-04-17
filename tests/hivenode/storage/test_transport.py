"""
test_transport
==============

Tests for file transport with ledger and provenance integration.

Dependencies:
- import pytest

Functions:
- test_transport_write_emits_ledger_event(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test that write operation emits to Event Ledger.
- test_transport_read_file(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test reading file through transport.
- test_transport_move_emits_ledger_event(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test that move operation emits to Event Ledger.
- test_transport_copy_file(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test copying file through transport.
- test_transport_delete_emits_ledger_event(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test that delete operation emits to Event Ledger.
- test_transport_records_provenance(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test that transport records provenance for operations.
- test_transport_provenance_chain(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test provenance chain for multiple writes.
- test_transport_cross_volume_move(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test moving file across volumes.
- test_transport_cross_volume_copy(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test copying file across volumes.
- test_transport_list_files(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test listing files through transport.
- test_transport_stat_file(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test getting file stats through transport.
- test_transport_requires_actor_and_intent(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test that mutating operations require actor and intent.
- test_transport_validates_actor_format(temp_volumes_yaml, temp_ledger_db, temp_provenance_db): Test that transport validates actor entity ID format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
