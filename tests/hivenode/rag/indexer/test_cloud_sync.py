"""
test_cloud_sync
===============

Tests for cloud sync service.

Tests the PostgreSQL cloud sync with pgvector extension.
Ported from platform/efemera tests.

Dependencies:
- import os
- import tempfile
- from datetime import datetime
- from pathlib import Path
- import pytest
- from hivenode.rag.chunkers import CodeChunk
- from hivenode.rag.indexer.cloud_sync import CloudSyncService, _vector_to_pgvector
- from hivenode.rag.indexer.markdown_exporter import MarkdownExporter
- from hivenode.rag.indexer.models import (
- from hivenode.rag.indexer.storage import IndexStorage

Functions:
- postgres_container(): Start PostgreSQL container with pgvector extension.
- temp_storage(): Create temp storage for testing.
- temp_markdown_dir(): Create temp directory for markdown exports.
- cloud_sync(postgres_container, temp_storage, temp_markdown_dir): Create CloudSyncService with test Postgres.
- sample_record(): Create sample IndexRecord for testing.
- sample_chunks(): Create sample chunks for testing.
- sample_embeddings(): Create sample embeddings for testing.
- test_ensure_schema(cloud_sync): Test that ensure_schema creates tables and vector extension.
- test_sync_to_cloud_insert(cloud_sync, temp_storage, sample_record, sample_chunks, sample_embeddings): Test that sync_to_cloud inserts record + chunks + embeddings.
- test_sync_to_cloud_upsert(cloud_sync, temp_storage, sample_record, sample_chunks, sample_embeddings): Test that sync_to_cloud upserts (updates existing record).
- test_sync_all(cloud_sync, temp_storage): Test that sync_all syncs multiple records.
- test_cascade_delete(cloud_sync, temp_storage, sample_record, sample_chunks, sample_embeddings): Test cascade delete removes chunks and embeddings.
- test_ivfflat_index_exists(cloud_sync): Test IVFFlat index exists on embeddings.vector.
- test_vector_to_pgvector(): Test _vector_to_pgvector converts list to string correctly.
- test_cloud_sync_disabled(): Test cloud sync disabled when db_url is None.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
