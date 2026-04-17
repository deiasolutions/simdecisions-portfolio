"""
chunkers
========

Content chunkers for RAG system.

Ported from _tools/build_index.py with additions for chat messages.
Pure functions — no I/O, no embedding, no database.

Extended with production-grade chunkers for Python (AST), JavaScript,
PHASE-IR JSON, ADR documents, and SPEC documents.

Dependencies:
- import ast
- import hashlib
- import json
- import logging
- import re
- from dataclasses import dataclass, field
- from typing import Any, Optional

Classes:
- CodeChunk: A chunk of code with metadata.
- ChatChunk: A chat message chunk.

Functions:
- _extract_ir_pairs_from_docstring(docstring: str): Extract IR pairs from docstring comments.
- _create_chunk(content: str,
    start_line: int,
    end_line: int,
    ir_pairs: Optional[list] = None,
    chunk_type: str = "section",
    name: str = "",
    file_path: str = "",): Factory function for creating CodeChunk instances.
- _chunk_by_headings(content: str,
    heading_pattern: str,
    file_path: str = "",
    chunk_type: str = "section",): Generic heading-based chunker.
- _chunk_python(content: str, file_path: str = ""): Extract functions and classes from Python using AST.
- _chunk_javascript(content: str, file_path: str = ""): Extract functions and classes from JavaScript/TypeScript.
- _chunk_phase_ir(content: str, file_path: str = ""): Chunk PHASE-IR JSON files.
- _chunk_adr(content: str, file_path: str = ""): Chunk ADR documents by decision sections.
- _chunk_spec(content: str, file_path: str = ""): Chunk SPEC documents by ## headings (capability claims).
- chunk_python(file_path: str, content: str): Extract functions and classes from Python using AST.
- chunk_typescript(file_path: str, content: str): Extract functions and classes from TypeScript/TSX using regex.
- chunk_markdown(file_path: str, content: str): Extract sections from Markdown by headings.
- chunk_css(file_path: str, content: str): Treat entire CSS file as one chunk.
- chunk_file(file_path: str, content: str): Route file to appropriate chunker based on extension and filename.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
