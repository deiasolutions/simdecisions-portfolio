# TASK-032: Repo Index Core — Schema, Indexer, Gitignore Parser -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-12

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\__init__.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\schemas.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\gitignore.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\indexer.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\__init__.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_gitignore.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_indexer.py` (created)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\FEATURE-INVENTORY.md` (updated via inventory tool)

## What Was Done

- Created `hivenode/repo/` module with schemas, gitignore parser, and indexer
- Implemented Pydantic schemas: FileEntry, ScanResult, IndexQuery, IndexResult, TreeNode, FileContent, RepoStats
- Implemented GitignoreParser class using pathspec library with support for:
  - Standard gitignore patterns (*.pyc, dist/, etc.)
  - Nested .gitignore files (combines rules from multiple levels)
  - Negation patterns (!important.log)
  - Wildcard and directory-specific patterns
- Implemented RepoIndexer class with SQLite backend:
  - Database schema with files and scan_meta tables
  - Full repo scan with hardcoded exclusions (.git/, node_modules/, etc.)
  - SHA-256 content hashing for files
  - Gitignore status tracking (computed during scan)
  - User-controlled visibility flags (preserved across re-scans)
  - Query interface with filters: path prefix, extension, gitignored, visibility, search, pagination
  - Tree builder for nested directory structure
  - File reader with security checks (path traversal, .git/ access blocked)
  - Auto-detection of text vs binary files (UTF-8 or base64 encoding)
  - Visibility toggle for files and directories (recursive for dirs)
  - Statistics computation (counts, extensions, sizes)
- Created comprehensive test suite (39 tests total):
  - 7 gitignore parser tests
  - 32 indexer tests covering scan, query, tree, read, visibility, stats
  - All security checks tested (path traversal, absolute paths, .git/ access)
  - Re-scan behavior verified (preserves visibility, updates hashes, removes deleted)
- Verified indexer works on real shiftcenter repo (628 files, 113 dirs, scanned in 252ms)
- Added REPO-INDEX-001 to feature inventory (39 tests)

## Test Results

```
tests/hivenode/repo/test_gitignore.py::test_parse_simple_patterns PASSED
tests/hivenode/repo/test_gitignore.py::test_nested_gitignore_files PASSED
tests/hivenode/repo/test_gitignore.py::test_negation_patterns PASSED
tests/hivenode/repo/test_gitignore.py::test_wildcard_patterns PASSED
tests/hivenode/repo/test_gitignore.py::test_empty_gitignore PASSED
tests/hivenode/repo/test_gitignore.py::test_directory_slash_pattern PASSED
tests/hivenode/repo/test_gitignore.py::test_absolute_path_pattern PASSED
tests/hivenode/repo/test_indexer.py::test_scan_indexes_files PASSED
tests/hivenode/repo/test_indexer.py::test_scan_excludes_hardcoded_dirs PASSED
tests/hivenode/repo/test_indexer.py::test_scan_marks_gitignored_files PASSED
tests/hivenode/repo/test_indexer.py::test_scan_computes_content_hash PASSED
tests/hivenode/repo/test_indexer.py::test_scan_parses_extensions PASSED
tests/hivenode/repo/test_indexer.py::test_scan_directories_marked PASSED
tests/hivenode/repo/test_indexer.py::test_rescan_preserves_visibility PASSED
tests/hivenode/repo/test_indexer.py::test_rescan_updates_modified_files PASSED
tests/hivenode/repo/test_indexer.py::test_rescan_removes_deleted_files PASSED
tests/hivenode/repo/test_rescan_new_files_default_visible PASSED
tests/hivenode/repo/test_indexer.py::test_query_filter_by_path_prefix PASSED
tests/hivenode/repo/test_indexer.py::test_query_filter_by_extension PASSED
tests/hivenode/repo/test_indexer.py::test_query_default_excludes_gitignored PASSED
tests/hivenode/repo/test_indexer.py::test_query_gitignored_include PASSED
tests/hivenode/repo/test_indexer.py::test_query_gitignored_only PASSED
tests/hivenode/repo/test_indexer.py::test_query_show_all_includes_hidden PASSED
tests/hivenode/repo/test_indexer.py::test_query_hidden_only PASSED
tests/hivenode/repo/test_indexer.py::test_query_search_substring PASSED
tests/hivenode/repo/test_indexer.py::test_query_pagination PASSED
tests/hivenode/repo/test_indexer.py::test_tree_structure_nested PASSED
tests/hivenode/repo/test_indexer.py::test_tree_applies_filters PASSED
tests/hivenode/repo/test_indexer.py::test_read_file_text PASSED
tests/hivenode/repo/test_indexer.py::test_read_file_auto_detection PASSED
tests/hivenode/repo/test_indexer.py::test_read_file_missing_raises PASSED
tests/hivenode/repo/test_indexer.py::test_read_file_path_traversal_blocked PASSED
tests/hivenode/repo/test_indexer.py::test_read_file_absolute_path_blocked PASSED
tests/hivenode/repo/test_indexer.py::test_read_file_git_dir_forbidden PASSED
tests/hivenode/repo/test_indexer.py::test_set_visibility_single_file PASSED
tests/hivenode/repo/test_indexer.py::test_set_visibility_directory_recursive PASSED
tests/hivenode/repo/test_indexer.py::test_stats_counts_accurate PASSED
tests/hivenode/repo/test_indexer.py::test_stats_extension_grouping PASSED
tests/hivenode/repo/test_indexer.py::test_stats_last_scan_time PASSED

============================= 39 passed in 1.90s ========================
```

## Implementation Notes

- Used TDD approach: wrote tests first, then implementation
- All paths in DB stored relative to repo root with forward slashes
- Hardcoded exclusions (.git/, node_modules/, etc.) never indexed, never served
- Gitignore parser uses pathspec library with 'gitignore' pattern type
- Path filtering supports trailing slash for directories (cleaned internally)
- Query path filter matches directory itself plus descendants
- Security: path traversal blocked, absolute paths rejected, .git/ access forbidden
- Auto-detection uses TEXT_EXTENSIONS set for UTF-8 vs base64 encoding
- Scan is fast: ~250ms for 628 files on real repo
- Database location: ~/.shiftcenter/repo-index.db (follows config.py pattern)
- Repo root auto-detection: walks up from hivenode/ until .git/ found

## Key Patterns Followed

- TDD: All tests written before implementation
- No stubs: Every method fully implemented
- Pydantic models for all data structures
- Async methods throughout (even though using sync sqlite3 for simplicity)
- SQLite with proper indexes for query performance
- Follows existing hivenode patterns (config.py for DB paths, async interfaces)
- Comprehensive error handling with specific exceptions
- Security-first: all path operations validated

## Blocks

TASK-033 (Repo Routes): Can now proceed with FastAPI routes
TASK-034 (Dependencies): pathspec library needs to be added to pyproject.toml

## Next Steps

TASK-033 will implement the FastAPI routes (/repo/scan, /repo/index, etc.) using this core module.
TASK-034 will add pathspec dependency and create `.deia/to_localhost/` directory.
