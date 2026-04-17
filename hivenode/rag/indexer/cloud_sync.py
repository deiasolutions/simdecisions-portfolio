"""
cloud_sync
==========

Cloud sync service for PostgreSQL with pgvector.

This module syncs IndexRecord data from local SQLite to cloud PostgreSQL
with pgvector extension for embedding search.

Ported from platform/efemera/src/efemera/indexer/cloud_sync.py.

Dependencies:
- import json
- import logging
- import os
- from typing import Optional
- from hivenode.rag.indexer.markdown_exporter import MarkdownExporter
- from hivenode.rag.indexer.storage import IndexStorage

Classes:
- CloudSyncService: Syncs index records from SQLite to PostgreSQL with pgvector.

Functions:
- _vector_to_pgvector(vector: list[float]): Convert Python list to pgvector string format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
