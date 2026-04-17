"""
test_ledger_adapter
===================

Tests for DES ledger adapter.

Dependencies:
- import pytest
- import json
- from simdecisions.des.ledger_adapter import LedgerAdapter
- from hivenode.ledger.writer import LedgerWriter
- from hivenode.ledger.reader import LedgerReader

Functions:
- ledger_db(tmp_path): Create temporary ledger database.
- ledger_writer(ledger_db): Create ledger writer.
- ledger_reader(ledger_db): Create ledger reader.
- adapter(ledger_writer): Create ledger adapter.
- filter_sim_events(events): Filter out genesis/system events, return only SIM_* events.
- test_adapter_emit_token_created(adapter, ledger_reader): Verify SIM_TOKEN_CREATED event written to ledger.
- test_adapter_emit_node_started(adapter, ledger_reader): Verify SIM_NODE_STARTED event.
- test_adapter_emit_resource_acquired(adapter, ledger_reader): Verify SIM_RESOURCE_ACQUIRED event.
- test_adapter_currencies(adapter, ledger_reader): Verify CLOCK=sim_time, COIN=0, CARBON=estimated.
- test_adapter_universal_entity_id_format(adapter, ledger_reader): Verify actor is sim:{run_id}, target is {type}:{id}.
- test_adapter_missing_run_id(adapter): Verify raises error if run_id not provided.
- test_adapter_token_arrive_mapping(adapter, ledger_reader): Test token_arrive -> SIM_TOKEN_ARRIVED.
- test_adapter_node_end_mapping(adapter, ledger_reader): Test node_end -> SIM_NODE_COMPLETED.
- test_adapter_resource_released_mapping(adapter, ledger_reader): Test resource_released -> SIM_RESOURCE_RELEASED.
- test_adapter_checkpoint_mapping(adapter, ledger_reader): Test checkpoint -> SIM_CHECKPOINT.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
