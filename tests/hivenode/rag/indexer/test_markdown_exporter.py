"""
test_markdown_exporter
======================

Tests for markdown exporter.

Tests the markdown export system for IndexRecord human-readable cache.
Ported from platform/efemera tests.

Dependencies:
- import tempfile
- from datetime import datetime
- from pathlib import Path
- import pytest
- from hivenode.rag.indexer.markdown_exporter import MarkdownExporter
- from hivenode.rag.indexer.models import (
- from hivenode.rag.indexer.storage import IndexStorage

Functions:
- temp_markdown_dir(): Create temp directory for markdown exports.
- temp_storage(): Create temp storage for testing.
- sample_record(): Create sample IndexRecord for testing.
- test_export_to_markdown_structure(sample_record): Test that export_to_markdown produces correct structure.
- test_export_to_markdown_values(sample_record): Test that export_to_markdown includes correct values.
- test_ir_pair_status_symbols(temp_markdown_dir): Test that IR pair status symbols are correct.
- test_write_markdown_file(temp_markdown_dir, temp_storage, sample_record): Test that write_markdown_file writes to disk.
- test_sync_all_to_markdown(temp_markdown_dir, temp_storage): Test that sync_all_to_markdown exports multiple records.
- test_directory_creation(): Test that directory is created if it doesn't exist.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
