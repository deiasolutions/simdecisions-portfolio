"""
test_storage
============

Tests for IndexStorage SQLite persistence layer.

Tests cover schema creation, CRUD operations, cascade deletes,
pagination, and content hashing.

Dependencies:
- import sqlite3
- import tempfile
- from datetime import datetime
- from pathlib import Path
- import pytest
- from hivenode.rag.chunkers import CodeChunk
- from hivenode.rag.indexer.models import (
- from hivenode.rag.indexer.storage import IndexStorage, compute_content_hash

Functions:
- temp_db(): Create a temporary database for testing.
- storage(temp_db): Create IndexStorage instance with temporary database.
- sample_record(): Create a sample IndexRecord for testing.
- sample_chunks(): Create sample CodeChunk list for testing.
- sample_embeddings(): Create sample EmbeddingRecord list for testing.
- test_schema_creation(storage, temp_db): Test that database schema is created with all 3 tables and indexes.
- test_insert_record_only(storage, sample_record): Test inserting IndexRecord without chunks or embeddings.
- test_insert_with_chunks(storage, sample_record, sample_chunks): Test inserting IndexRecord with chunks.
- test_insert_with_embeddings(storage, sample_record, sample_embeddings): Test inserting IndexRecord with embeddings.
- test_get_by_id(storage, sample_record): Test retrieving record by artifact_id.
- test_get_by_id_not_found(storage): Test retrieving non-existent record returns None.
- test_get_by_path(storage, sample_record): Test retrieving record by file path.
- test_get_by_path_not_found(storage): Test retrieving by non-existent path returns None.
- test_update_record(storage, sample_record, sample_chunks): Test updating record deletes old data and re-inserts.
- test_cascade_delete_chunks_and_embeddings(storage, sample_record, sample_chunks, sample_embeddings): Test that deleting index_record cascades to chunks and embeddings.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
