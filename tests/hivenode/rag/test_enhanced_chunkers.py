"""
test_enhanced_chunkers
======================

Tests for enhanced chunking functionality.

Tests AST-based Python chunking, JavaScript chunking, PHASE-IR chunking,
ADR/SPEC document chunking, and IR pair extraction.

Dependencies:
- import json
- from hivenode.rag.chunkers import (

Functions:
- test_chunk_python_with_three_functions(): Test chunking Python file with 3 functions → 3 chunks.
- bar(x): Second function.
- test_chunk_python_class_with_methods(): Test chunking Python class with 2 methods → 1 class chunk.
- test_extract_ir_pairs_from_docstring(): Test IR pair extraction from docstring with multiple pairs.
- test_chunk_python_syntax_error(): Test syntax error handling → empty list + warning.
- test_chunk_python_empty_file(): Test empty file → empty list.
- test_chunk_javascript_functions(): Test chunking JS file with function declarations and arrow functions.
- test_chunk_javascript_class(): Test chunking JS class with methods.
- test_chunk_javascript_nested_functions(): Test nested functions → only outer scope chunked.
- test_chunk_javascript_unmatched_braces(): Test edge case: unmatched braces → skip malformed code.
- test_chunk_phase_ir_valid_json(): Test valid PHASE-IR JSON with 5 nodes → 5 chunks.
- test_chunk_phase_ir_with_metadata_ir_pairs(): Test IR pairs extracted from node metadata.
- test_chunk_phase_ir_invalid_json(): Test invalid JSON → empty list.
- test_chunk_adr_three_decisions(): Test ADR with 3 decisions → 3 chunks.
- test_chunk_adr_decision_numbering_preserved(): Test decision numbering preserved in chunks.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
