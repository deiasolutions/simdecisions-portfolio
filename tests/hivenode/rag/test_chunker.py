"""
test_chunker
============

Tests for RAG chunker module.

Tests the Chunker class that breaks artifacts into logical chunks
based on artifact type (code per function, PHASE-IR per node, etc.).

Dependencies:
- from pathlib import Path
- from hivenode.rag.indexer.chunker import Chunker
- from hivenode.rag.indexer.models import ArtifactType, IRStatus

Classes:
- TestChunkerCodePython: Test Python code chunking.
- TestChunkerCodeJavaScript: Test JavaScript/TypeScript code chunking.
- TestChunkerPhaseIR: Test PHASE-IR chunking.
- TestChunkerADR: Test ADR chunking.
- TestChunkerSpec: Test Spec chunking.
- TestChunkerDocument: Test Document chunking.
- TestChunkerHeadings: Test heading-based chunking.
- TestChunkerCreateChunk: Test chunk creation.
- TestChunkerDispatch: Test main chunk dispatcher.
- TestChunkerEdgeCases: Test edge cases.
- TestChunkerIRPairs: Test IR pair creation and management.

Functions:
- goodbye(): Test chunking Python code with class definitions.
- farewell(name): Test chunking very long function.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
