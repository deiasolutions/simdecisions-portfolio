"""
build_index
===========

Repository Index Builder for ShiftCenter

Walks the repo, chunks files by structure (functions/classes/sections/nodes),
embeds them using sentence-transformers, and stores in SQLite + FAISS/numpy.

Supports incremental mode (default): only re-chunks/re-embeds files that have changed.
Use --full to force a complete rebuild.

Dependencies:
- import os
- import sys
- import ast
- import json
- import sqlite3
- import pickle
- import argparse
- from typing import List, Dict, Tuple
- import re
- import numpy as np

Classes:
- Chunk: Represents a chunk of code/text with metadata

Functions:
- should_skip_dir(dir_path: str): Check if directory should be skipped
- extract_python_chunks(file_path: str, content: str): Extract functions and classes from Python file using AST
- extract_typescript_chunks(file_path: str, content: str): Extract functions and classes from TypeScript/TSX file using regex
- extract_markdown_chunks(file_path: str, content: str): Extract sections from Markdown file by headings
- extract_ir_chunks(file_path: str, content: str): Extract nodes from IR JSON file
- get_file_mtime(file_path: str): Get modification time of a file
- get_stored_mtime(cursor: sqlite3.Cursor, file_path: str): Get stored mtime for a file from database
- collect_chunks_incremental(repo_path: str, cursor: sqlite3.Cursor): Walk the repository and collect chunks.
- collect_chunks(repo_path: str): Walk the repository and collect all chunks (full rebuild)
- create_database(db_path: str): Create SQLite database with chunks table
- embed_chunks(chunks: List[Chunk], model: SentenceTransformer): Embed all chunks using sentence-transformers
- save_chunks_and_embeddings(chunks: List[Chunk], embeddings: np.ndarray,
                               db_path: str, vectors_path: str, is_incremental: bool = False): Save chunks to SQLite and embeddings to FAISS/numpy

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
