"""
test_smoke_backup
=================

Backend smoke tests — integration tests for major flows.

Dependencies:
- import pytest
- import base64
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from hivenode.config import HivenodeConfig
- from hivenode import dependencies

Functions:
- smoke_client(tmp_path, monkeypatch): TestClient with real services pointing to temp storage.
- test_smoke_health(smoke_client): GET /health returns 200 with basic status.
- test_smoke_status(smoke_client): GET /status returns node_id, mode, uptime.
- test_smoke_storage_write_read(smoke_client): POST /storage/write → GET /storage/read → content matches.
- test_smoke_storage_list_after_write(smoke_client): Write file → GET /storage/list → file in listing.
- test_smoke_storage_stat_after_write(smoke_client): Write file → GET /storage/stat → size, hash, modified.
- test_smoke_ledger_write_query(smoke_client): Write event via route → GET /ledger/events → event in list.
- test_smoke_ledger_cost_with_tokens(smoke_client): Write events via storage → GET /ledger/cost → verify token aggregation.
- test_smoke_ledger_query_by_type(smoke_client): Write events via storage → query by event type filter → correct filtering.
- test_smoke_shell_exec_allowed(smoke_client): POST /shell/exec with echo → status: success, stdout contains output.
- test_smoke_shell_exec_denied(smoke_client): POST /shell/exec with denied command → status: denied.
- test_smoke_sync_status(smoke_client): GET /sync/status → returns last_sync, pending, conflicts.
- test_smoke_sync_trigger(smoke_client): POST /sync/trigger → returns sync result.
- test_smoke_volumes_list(smoke_client): GET /storage/volumes → returns list with home:// volume.
- test_smoke_node_status_local(smoke_client): GET /node/status → returns node info in local mode.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
