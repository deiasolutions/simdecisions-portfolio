"""
storage
=======

SQLite-based persistence layer for RAG indexer.

This module provides the IndexStorage class for storing and retrieving
IndexRecord, chunks, and embeddings with cascade delete support.

Ported from platform/efemera/src/efemera/indexer/storage.py.

Dependencies:
- import hashlib
- import json
- import logging
- import pickle
- import sqlite3
- import uuid
- from datetime import datetime
- from pathlib import Path
- from typing import Optional
- from hivenode.rag.chunkers import CodeChunk

Classes:
- IndexStorage: SQLite-based storage for index records, chunks, and embeddings.

Functions:
- compute_content_hash(content: str): Compute SHA256 hash of content.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
