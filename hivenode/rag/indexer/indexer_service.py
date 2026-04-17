"""
indexer_service
===============

Indexer Service: Two-pass orchestration for RAG indexing.

This module provides the IndexerService class that coordinates scanning,
chunking, embedding, and storage with two-pass TF-IDF fitting.

Ported from platform/efemera/src/efemera/indexer/indexer_service.py.

Dependencies:
- import json
- import logging
- import uuid
- from datetime import datetime
- from pathlib import Path
- from typing import Optional
- from sqlalchemy.orm import Session
- from hivenode.rag.chunkers import CodeChunk, chunk_file
- from hivenode.rag.embedder import TFIDFEmbedder
- from hivenode.rag.indexer.models import (

Classes:
- IndexerService: Orchestrates two-pass indexing: scan → fit embedder → index all files.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
