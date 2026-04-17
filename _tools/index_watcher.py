"""
index_watcher
=============

Real-time File Watcher for Repository Index

Monitors the repository for changes to .py, .md, .ts, .tsx, .css, and .ir.json files.
Automatically updates the index database and vector embeddings on file changes.

Supports:
- File creation, modification, deletion, and renaming
- Debouncing (batches changes within 2 seconds)
- Model kept in memory (loaded once at startup)
- Graceful shutdown on Ctrl+C
- Windows compatibility

Usage:
    python _tools/index_watcher.py
    python _tools/index_watcher.py --verbose

Dependencies:
- import os
- import sys
- import ast
- import json
- import sqlite3
- import pickle
- import argparse
- import time
- import re
- from pathlib import Path

Classes:
- Chunk: Represents a chunk of code/text with metadata
- IndexEventHandler: Handles file system events and updates the index

Functions:
- should_skip_dir(dir_path: str): Check if directory should be skipped
- should_skip_file(file_path: str): Check if file should be skipped based on path
- extract_python_chunks(file_path: str, content: str): Extract functions and classes from Python file using AST
- extract_typescript_chunks(file_path: str, content: str): Extract functions and classes from TypeScript/TSX file using regex
- extract_markdown_chunks(file_path: str, content: str): Extract sections from Markdown file by headings
- extract_ir_chunks(file_path: str, content: str): Extract nodes from IR JSON file
- extract_chunks(file_path: str, content: str): Extract chunks from a file based on its extension
- create_database(db_path: str): Create SQLite database with chunks table
- embed_chunks(chunks: List[Chunk], model: SentenceTransformer): Embed chunks using sentence-transformers
- rebuild_vector_index(db_path: str, vectors_path: str): Rebuild the vector index from all embeddings in the database
- count_indexed_files(db_path: str): Count how many files are currently indexed

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
