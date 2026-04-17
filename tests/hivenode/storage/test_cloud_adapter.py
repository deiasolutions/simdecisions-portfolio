"""
test_cloud_adapter
==================

Tests for cloud adapter HTTP client.

Dependencies:
- import pytest
- import respx
- import httpx

Functions:
- cloud_adapter(): Create a cloud adapter instance.
- sync_queue(tmp_path): Create a sync queue instance.
- test_read_success(cloud_adapter): Test read returns bytes when cloud responds 200.
- test_read_not_found(cloud_adapter): Test read raises FileNotFoundError when cloud responds 404.
- test_read_offline_network_error(cloud_adapter): Test read raises VolumeOfflineError on network error.
- test_write_success(cloud_adapter): Test write returns metadata when cloud responds 200.
- test_write_offline_enqueues(cloud_adapter, sync_queue, tmp_path): Test write enqueues in sync_queue when cloud is offline.
- test_list_success(cloud_adapter): Test list returns file list when cloud responds 200.
- test_list_offline_raises(cloud_adapter): Test list raises VolumeOfflineError on network error.
- test_stat_success(cloud_adapter): Test stat returns metadata when cloud responds 200.
- test_stat_not_found(cloud_adapter): Test stat raises FileNotFoundError when cloud responds 404.
- test_delete_success(cloud_adapter): Test delete returns confirmation when cloud responds 200.
- test_exists_true(cloud_adapter): Test exists returns True when stat succeeds.
- test_exists_false(cloud_adapter): Test exists returns False when stat returns 404.
- test_move_success(cloud_adapter): Test move implements read + write + delete sequence.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
