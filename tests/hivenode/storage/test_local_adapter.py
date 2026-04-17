"""
test_local_adapter
==================

Tests for local filesystem adapter.

Dependencies:
- import pytest

Functions:
- test_write_and_read_file(local_adapter_root): Test writing and reading a file.
- test_write_creates_parent_dirs(local_adapter_root): Test that write creates parent directories.
- test_read_missing_file(local_adapter_root): Test reading non-existent file raises FileNotFoundError.
- test_delete_file(local_adapter_root): Test deleting a file.
- test_delete_missing_file(local_adapter_root): Test deleting non-existent file raises FileNotFoundError.
- test_exists_file(local_adapter_root): Test checking if file exists.
- test_list_files_in_directory(local_adapter_root): Test listing files in a directory.
- test_list_nested_directory(local_adapter_root): Test listing files in nested directory.
- test_stat_file(local_adapter_root): Test getting file metadata.
- test_move_file_within_volume(local_adapter_root): Test moving file within the same volume.
- test_reject_path_traversal_read(local_adapter_root): Test rejection of path traversal on read.
- test_reject_path_traversal_write(local_adapter_root): Test rejection of path traversal on write.
- test_reject_absolute_path(local_adapter_root): Test rejection of absolute paths.
- test_binary_content(local_adapter_root): Test writing and reading binary content.
- test_empty_file(local_adapter_root): Test handling empty files.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
