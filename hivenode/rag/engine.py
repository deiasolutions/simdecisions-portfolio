"""
engine
======

RAG engine — indexing, ingestion, and semantic search.

Stores code chunks and chat chunks in SQLite with numpy-based
cosine similarity search. sentence-transformers is lazy-loaded.

Dependencies:
- import os
- import pickle
- import sqlite3
- import time
- from contextlib import contextmanager
- from pathlib import Path
- from typing import Any, Optional
- import numpy as np
- from hivenode.rag.chunkers import (
- from hivenode.rag.embedder import embed_texts, MODEL_NAME

Classes:
- RagEngine: Core RAG engine for code + chat search.

Functions:
- get_indexer_service(repo_path: Path, db_session: Any): Get or create IndexerService singleton.
- get_reliability_calculator(db_session: Any): Get or create ReliabilityCalculator singleton.
- get_synthesizer(): Get or create Synthesizer singleton.
- get_sync_daemon(): Get or create SyncDaemon singleton.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
