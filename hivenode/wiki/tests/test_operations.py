"""
test_operations
===============

Tests for wiki operations: ingest, query, lint.

Dependencies:
- import pytest
- from pathlib import Path
- import tempfile
- import shutil
- from hivenode.wiki.store import init_engine, reset_engine
- from hivenode.wiki.operations import (

Functions:
- temp_wiki_dir(): Create temporary wiki directory structure.
- setup_db(): Initialize in-memory database for each test.
- test_append_to_log(temp_wiki_dir): Test appending operations to log.md.
- test_update_wiki_index(temp_wiki_dir): Test auto-generating index.md from database.
- test_ingest_source_creates_page(temp_wiki_dir): Test ingesting a raw source creates wiki page.
- test_ingest_source_updates_existing_page(temp_wiki_dir): Test ingesting same source twice updates page.
- test_query_wiki_finds_pages(temp_wiki_dir): Test querying wiki finds relevant pages.
- test_query_wiki_files_answer(temp_wiki_dir): Test querying wiki with file_answer=True creates new page.
- test_lint_wiki_finds_orphans(temp_wiki_dir): Test lint operation finds orphan pages.
- test_lint_wiki_finds_missing_pages(temp_wiki_dir): Test lint operation finds missing pages (broken links).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
