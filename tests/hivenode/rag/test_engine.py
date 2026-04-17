"""
test_engine
===========

Tests for RagEngine — core RAG operations with mock embeddings.

Dependencies:
- import tempfile
- from pathlib import Path
- from unittest.mock import patch
- import pytest
- from hivenode.rag.engine import RagEngine

Functions:
- mock_embed_texts(texts: list[str]): Produce deterministic 384-dim vectors from text content.
- tmp_dir(): Create RagEngine with mock embedder and temp DB.
- engine_with_code(tmp_dir): Engine with sample code files already on disk.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
