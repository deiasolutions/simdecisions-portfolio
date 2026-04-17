# TASK-014: Port Indexing Tools to _tools/

## Objective

Port the repository indexing tools (build_index.py, query_index.py, index_watcher.py) from the old platform repo to `_tools/` in shiftcenter. Update all hardcoded paths to point at shiftcenter's directory structure. This is developer infrastructure — it makes every bee faster by enabling semantic search across the codebase.

## Priority

Low priority, high leverage. Not a product task. Dispatch when no product tasks are queued.

## Dependencies

None. These are standalone developer tools with no product code dependencies.

## Source Files

Port from the old platform repo:

| Source Path | Lines | Dest Path | What It Does |
|-------------|-------|-----------|-------------|
| `platform\_tools\build_index.py` | 572 | `_tools/build_index.py` | Walks repo, chunks files by structure (functions/classes/sections), embeds via sentence-transformers, stores in SQLite + FAISS/numpy. Incremental by default, `--full` for rebuild. |
| `platform\_tools\query_index.py` | 255 | `_tools/query_index.py` | Semantic similarity search against the index. `--rebuild` for incremental update, `--full-rebuild` for complete rebuild. |
| `platform\_tools\index_watcher.py` | 594 | `_tools/index_watcher.py` | Real-time file watcher (watchdog). Monitors .py/.md/.ir.json changes, debounces (2s batch), re-indexes changed files. Keeps embedding model in memory. |

**All source paths relative to:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\`

## Port Rules

### 1. Path Updates (CRITICAL)

All three files use the same pattern to find the repo root:
```python
repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

This assumes `platform/_tools/build_index.py` — goes up 2 levels to find repo root. **This is correct for shiftcenter too** since the structure is `shiftcenter/_tools/build_index.py`. Verify it works, but it should be a no-op change.

The index directory is hardcoded as:
```python
index_dir = os.path.join(repo_path, '.deia', 'index')
```

This is also correct for shiftcenter. Keep as-is.

`query_index.py` references:
```python
build_script = os.path.join(repo_path, '_tools', 'build_index.py')
```

Also correct. Keep as-is.

### 2. File Extension Patterns

`index_watcher.py` monitors `.py`, `.md`, `.ir.json` files. Add `.ts`, `.tsx`, `.css` to the watch list since shiftcenter has a browser/ frontend. The old platform repo was Python-only.

### 3. Ignore Patterns

Add these to the ignore list if not already present:
- `node_modules/`
- `.deia/hive/responses/` (don't index bee output)
- `.deia/hive/tasks/_archive/` (don't index archived tasks)
- `dist/`, `build/`, `.next/`

### 4. Chunking for TypeScript/TSX

`build_index.py` uses Python's `ast` module for `.py` files. For `.ts`/`.tsx` files, fall back to line-based chunking (split on blank lines or function/class boundaries via regex). Don't add a full TS parser — line-based is good enough for semantic search.

### 5. Dependencies

These tools require optional dependencies. Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
index = ["sentence-transformers", "faiss-cpu", "watchdog"]
```

If `faiss-cpu` is not installed, all three tools fall back to numpy — this is already handled in the source code.

### 6. No Test Files Required

These are developer CLI tools, not product code. Manual testing is sufficient:
- `python _tools/build_index.py` — should build index in `.deia/index/`
- `python _tools/query_index.py "event ledger schema"` — should return relevant files
- `python _tools/index_watcher.py` — should watch for changes and re-index

Verify each command runs without errors after port.

## Source Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\_tools\build_index.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\_tools\query_index.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\_tools\index_watcher.py`

## What NOT to Build

- No new indexing features
- No web UI for search
- No integration with the shell or terminal
- No TypeScript AST parser (regex chunking is fine for TS)

## Constraints

- Python 3.13 compatible
- No file over 500 lines (build_index.py is 572 — modularize the chunking logic into a separate file if needed)
- All paths relative to repo root (no hardcoded absolute paths)

## Deliverables

- [ ] `_tools/build_index.py` (or split into `_tools/build_index.py` + `_tools/chunkers.py` if over 500 lines)
- [ ] `_tools/query_index.py`
- [ ] `_tools/index_watcher.py`
- [ ] Updated `pyproject.toml` with index optional dependencies
- [ ] Manual verification: all 3 commands run successfully

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-014-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- manual verification output for all 3 commands
5. **Build Verification** -- command output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
