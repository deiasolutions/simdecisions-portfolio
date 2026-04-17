"""
operations
==========

Wiki operations: ingest, query, lint.

This module implements the LLM Wiki pattern operations:
- Ingest: Read raw/ sources, create/update wiki pages, update index.md, log activity
- Query: Search wiki pages, synthesize answers with citations, optionally file answers
- Lint: Health check for contradictions, orphan pages, stale claims

Dependencies:
- import json
- import os
- import re
- from pathlib import Path
- from typing import List, Dict, Any, Optional, Tuple
- from datetime import datetime, timezone
- from sqlalchemy import select, insert, update as sql_update, and_
- from hivenode.wiki.store import get_engine, wiki_pages
- from hivenode.wiki.parser import parse_wikilinks, parse_frontmatter
- from hivenode.ledger.emitter import emit_event

Functions:
- _now(): Return current UTC timestamp in ISO 8601 format.
- _ensure_dir(path: Path): Ensure directory exists.
- append_to_log(wiki_root: Path,
    operation: str,
    subject: str,
    details: Dict[str, Any]): Append operation to log.md in wiki directory.
- update_wiki_index(wiki_root: Path,
    workspace_id: str = "00000000-0000-0000-0000-000000000000"): Regenerate index.md from current wiki pages in database.
- ingest_source(raw_path: Path,
    wiki_root: Path,
    workspace_id: str = "00000000-0000-0000-0000-000000000000",
    user_id: Optional[str] = None): Ingest a source file from raw/ directory into wiki.
- query_wiki(question: str,
    wiki_root: Path,
    workspace_id: str = "00000000-0000-0000-0000-000000000000",
    file_answer: bool = False,
    user_id: Optional[str] = None): Query wiki with a question, synthesize answer with citations.
- lint_wiki(wiki_root: Path,
    workspace_id: str = "00000000-0000-0000-0000-000000000000"): Run health checks on wiki: find contradictions, orphans, missing pages.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
