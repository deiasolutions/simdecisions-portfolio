"""
ir_density
==========

IR Density Measurement — Dual-Mode Scorer (spec + prism).

Measures instruction density in two document types:
1. Hive specs (SPEC-*.md, TASK-*.md, IMPL-*.md)
2. PRISM-IR process definitions (*.prism.md, *.ir.yaml)

Pure static analysis, no LLM calls, no external dependencies.

Usage:
    python ir_density.py score path/to/file.md
    python ir_density.py score path/to/file.md --mode spec
    python ir_density.py batch .deia/hive/queue/backlog/
    python ir_density.py gate-check file.md --min-density 0.4

Dependencies:
- import argparse
- import csv
- import io
- import json
- import re
- import sys
- from pathlib import Path
- from typing import Optional

Functions:
- detect_doc_type(text: str): Auto-detect document type for scoring.
- estimate_tokens(text: str): Estimate token count using chars/4 approximation.
- count_prism_elements(text: str): Count executable elements in PRISM-IR process definition.
- get_ird_rating(ird: float): Get rating label for IRD score.
- score_prism(text: str): Score PRISM-IR process definition.
- count_checkboxes(text: str): Count checkbox items (acceptance criteria, smoke tests).
- count_bullets(text: str): Count bullet points (deliverables, constraints).
- count_file_paths(text: str): Count file path references.
- count_code_blocks(text: str): Count fenced code blocks.
- count_code_block_lines(text: str): Count lines inside code blocks.
- extract_section(text: str, section_name: str): Extract section content from markdown.
- check_sections_present(text: str): Check which expected sections are present in spec.
- score_spec(text: str): Score hive spec document (SPEC-*.md, TASK-*.md, IMPL-*.md).
- score(text: str, mode: Optional[str] = None): Score document with auto-detection or forced mode.
- cmd_score(args): Score a single file.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
