# TASK-032: Repo Index Core — Schema, Indexer, Gitignore Parser

**Status:** READY
**Assigned to:** BEE-SONNET
**Priority:** P1
**Depends on:** (none)
**Blocks:** TASK-033, TASK-034
**Estimate:** S
**Created:** 2026-03-12

---

## Objective

Build the core `hivenode/repo/` module with SQLite schema, RepoIndexer class, gitignore parsing, and comprehensive unit tests. This is the foundation for the Repo File Index Service (SPEC-REPO-INDEX-001).

## Context

The frontend needs read-only awareness of every file in the repository. This task creates the indexing engine that scans the repo tree, computes content hashes, applies gitignore rules, and stores metadata in SQLite.

## Acceptance Criteria

### 1. File Structure

Create `hivenode/repo/` module:

```
hivenode/repo/
├── __init__.py
├── indexer.py        # RepoIndexer class, scan logic, DB operations
├── gitignore.py      # GitignoreParser class using pathspec library
└── schemas.py        # Pydantic models
```

### 2. SQLite Schema (`indexer.py`)

Database location: `~/.shiftcenter/repo-index.db`

```sql
CREATE TABLE files (
    path        TEXT PRIMARY KEY,
    is_dir      BOOLEAN NOT NULL,
    size        INTEGER NOT NULL DEFAULT 0,
    modified    REAL NOT NULL,
    content_hash TEXT,
    extension   TEXT,
    gitignored  BOOLEAN NOT NULL DEFAULT 0,
    visible     BOOLEAN NOT NULL DEFAULT 1
);

CREATE INDEX idx_files_visible ON files(visible);
CREATE INDEX idx_files_gitignored ON files(gitignored);
CREATE INDEX idx_files_extension ON files(extension);
CREATE INDEX idx_files_parent ON files(path);

CREATE TABLE scan_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

### 3. Gitignore Parser (`gitignore.py`)

```python
class GitignoreParser:
    """Parse .gitignore files and check if paths match."""

    def __init__(self, repo_root: Path):
        """Initialize with repo root, read all .gitignore files."""

    def is_ignored(self, path: str) -> bool:
        """Check if path matches gitignore patterns."""
```

**Requirements:**
- Use `pathspec` library (you'll add to pyproject.toml in TASK-034)
- Read `.gitignore` at repo root
- Support nested `.gitignore` files (walk tree, combine patterns)
- Handle negation patterns (`!important.log`)
- Standard gitignore wildcard semantics (`*.pyc`, `dist/`)

### 4. Pydantic Schemas (`schemas.py`)

Define models for:

```python
class FileEntry(BaseModel):
    """Single file/directory entry."""
    path: str
    is_dir: bool
    size: int
    modified: float
    content_hash: str | None
    extension: str | None
    gitignored: bool
    visible: bool

class ScanResult(BaseModel):
    """Result of scan operation."""
    ok: bool
    file_count: int
    dir_count: int
    duration_ms: float
    gitignored_count: int

class IndexQuery(BaseModel):
    """Query filters for index."""
    path: str = ""
    ext: str | None = None
    gitignored: str = "exclude"  # exclude | include | only
    show_all: bool = False
    hidden_only: bool = False
    search: str | None = None
    limit: int = 500
    offset: int = 0

class IndexResult(BaseModel):
    """Query result."""
    files: list[FileEntry]
    total: int
    limit: int
    offset: int

class TreeNode(BaseModel):
    """Directory tree node."""
    name: str
    path: str
    is_dir: bool = True
    size: int | None = None
    extension: str | None = None
    children: list["TreeNode"] = []

class FileContent(BaseModel):
    """File content response."""
    path: str
    content: str
    encoding: str  # utf-8 | base64
    size: int

class RepoStats(BaseModel):
    """Summary statistics."""
    total_files: int
    total_dirs: int
    visible_files: int
    gitignored_files: int
    hidden_files: int
    last_scan_time: str | None
    extensions: dict[str, int]
    total_size_bytes: int
```

### 5. RepoIndexer Class (`indexer.py`)

```python
class RepoIndexer:
    """Indexes repository files into SQLite database."""

    def __init__(self, repo_root: Path, db_path: Path):
        """
        Initialize indexer.

        Args:
            repo_root: Absolute path to git repo root
            db_path: Where to store repo-index.db
        """

    async def scan(self) -> ScanResult:
        """
        Full repo re-scan.

        - Walk file tree from repo_root
        - Skip hardcoded exclusions: .git/, node_modules/, __pycache__/, .venv/, venv/
        - For each file: compute SHA-256 hash, check gitignore status
        - Upsert to files table
        - Delete rows for files that no longer exist
        - Preserve `visible` flag for existing paths
        - New files default to visible=True
        - Update scan_meta table with timestamp and counts

        Returns:
            ScanResult with counts and duration
        """

    async def query(self, filters: IndexQuery) -> IndexResult:
        """
        Query file index with filters.

        Filter logic:
        - path: prefix match (e.g., "hivenode/" shows all under hivenode/)
        - ext: exact match on extension (e.g., ".py")
        - gitignored: exclude (default), include, only
        - show_all: override visibility, show everything
        - hidden_only: only show visible=False
        - search: substring match on path (case-insensitive)
        - limit/offset: pagination

        Default view (no params): visible=1 AND gitignored=0 ("GitHub view")

        Returns:
            IndexResult with matching files and total count
        """

    async def tree(self, filters: IndexQuery) -> TreeNode:
        """
        Build directory tree from index.

        - Apply same filters as query()
        - Return nested structure from root
        - Each TreeNode has name, path, is_dir, children[]

        Returns:
            TreeNode representing root with nested children
        """

    async def read_file(self, path: str, encoding: str = "auto") -> FileContent:
        """
        Read file from disk (not from DB — always fresh).

        Security:
        - Reject paths with ".." (traversal attack)
        - Reject absolute paths (must be relative)
        - Reject .git/ contents (forbidden)
        - Resolve real path, assert it starts with repo_root

        Auto-detection (encoding="auto"):
        - Text extensions: .py, .ts, .tsx, .js, .jsx, .md, .json, .yml, .yaml,
          .toml, .css, .html, .sql, .sh, .bat, .txt, .cfg, .ini, .env, .egg.md
        - Everything else: base64

        Size limit: 10 MB (configurable)

        Returns:
            FileContent with content as UTF-8 string or base64 string

        Raises:
            ValueError: Path traversal attempt or invalid path
            PermissionError: Tried to read .git/
            FileNotFoundError: File doesn't exist
        """

    async def set_visibility(self, path: str, visible: bool) -> int:
        """
        Set visibility flag for file or directory.

        If path is a directory, recursively update all descendants (SQL LIKE prefix match).

        Args:
            path: Relative path from repo root
            visible: True to show, False to hide

        Returns:
            int: Number of rows affected
        """

    async def stats(self) -> RepoStats:
        """
        Compute summary statistics from database.

        - Count total files, dirs, visible, gitignored, hidden
        - Group by extension, count each
        - Sum total size
        - Get last_scan_time from scan_meta

        Returns:
            RepoStats model
        """
```

### 6. Hardcoded Exclusions

These directories are NEVER indexed, regardless of `.gitignore`:

- `.git/`
- `node_modules/`
- `__pycache__/`
- `.venv/`
- `venv/`

Implement as a constant in `indexer.py`:

```python
HARDCODED_EXCLUSIONS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
```

### 7. Repo Root Auto-Detection

In `__init__(self, repo_root: Path, ...)`, if `repo_root` is not provided or is `None`, auto-detect by walking up from `hivenode/` directory until a `.git/` folder is found.

```python
def _find_repo_root() -> Path:
    """Walk up from current file until .git/ is found."""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise ValueError("Could not find git repository root")
```

### 8. Unit Tests (`tests/hivenode/repo/test_indexer.py`)

Write comprehensive tests:

#### Gitignore Tests
- Parse standard `.gitignore` patterns (*.pyc, dist/, etc.)
- Nested `.gitignore` files (combine rules from root and subdirs)
- Negation patterns (`!important.log`)
- Wildcard patterns work correctly

#### Scan Tests
- Scan a temp directory tree, verify DB contents match
- Files matching gitignore patterns get `gitignored=True`
- Hardcoded exclusions (`.git/`, `node_modules/`) never appear in DB
- Content hash is correct SHA-256
- Modified timestamp captured
- Extensions parsed correctly (lowercase, with dot)
- Directories have `is_dir=True`, `content_hash=None`

#### Re-scan Tests
- Re-scan preserves `visible` flag for existing files
- Re-scan updates modified time and hash for changed files
- Re-scan removes rows for deleted files
- New files default to `visible=True`

#### Query Tests
- Filter by path prefix (`path="hivenode/"`)
- Filter by extension (`ext=".py"`)
- Filter by gitignored: exclude (default), include, only
- `show_all=True` includes hidden files
- `hidden_only=True` shows only `visible=False`
- Search substring match (case-insensitive)
- Pagination works (limit/offset)
- Default view: `visible=1 AND gitignored=0`

#### Tree Tests
- Tree structure is nested correctly
- Filters apply to tree building
- Empty directories included if they have visible children

#### Read File Tests
- Read text file → UTF-8 content
- Read binary file → base64 content
- Read missing file → FileNotFoundError
- Path traversal (`../../../etc/passwd`) → ValueError
- Absolute path (`/etc/passwd`) → ValueError
- `.git/` access (`".git/config"`) → PermissionError

#### Visibility Tests
- Set visibility on single file
- Set visibility on directory (recursive, all descendants updated)
- Returns correct affected row count

#### Stats Tests
- Counts are accurate
- Extension grouping works
- Total size computed correctly
- `last_scan_time` from scan_meta

### 9. Test Fixtures

Use temp directories for test repo structure:

```python
@pytest.fixture
def test_repo(tmp_path):
    """Create a test repo with known structure."""
    repo = tmp_path / "test_repo"
    repo.mkdir()

    # Create .gitignore
    (repo / ".gitignore").write_text("*.pyc\ndist/\n.env\n")

    # Create file structure
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("print('hello')")
    (repo / "src" / "cache.pyc").write_text("bytecode")  # gitignored

    (repo / "dist").mkdir()  # gitignored directory
    (repo / "dist" / "bundle.js").write_text("// bundled")

    (repo / "README.md").write_text("# Test Repo")
    (repo / ".env").write_text("SECRET=xyz")  # gitignored

    (repo / ".git").mkdir()  # hardcoded exclusion
    (repo / ".git" / "config").write_text("[core]")

    (repo / "node_modules").mkdir()  # hardcoded exclusion
    (repo / "node_modules" / "lib.js").write_text("module")

    return repo

@pytest.fixture
async def indexer(test_repo, tmp_path):
    """Create indexer instance for test repo."""
    db_path = tmp_path / "test-index.db"
    idx = RepoIndexer(repo_root=test_repo, db_path=db_path)
    await idx.scan()  # Initial scan
    return idx
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-REPO-INDEX-001.md` — full spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — DB path pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\base.py` — adapter pattern reference
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter.py` — test pattern reference

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\schemas.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\gitignore.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\repo\indexer.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_gitignore.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\repo\test_indexer.py`

## Constraints

- **NO STUBS.** Every method fully implemented.
- **TDD.** Write tests first, then implementation.
- **No file over 500 lines.** Modularize if needed.
- Use `pathspec` library (assume it's already in pyproject.toml — TASK-034 will add it)
- Follow existing hivenode patterns (Pydantic models, async methods, SQLite)
- Use stdlib `sqlite3`, `hashlib`, `os.walk` — no additional dependencies beyond pathspec
- All paths in DB are relative to repo root, forward slashes, no leading slash

## Expected Test Coverage

- `test_gitignore.py`: ~8 tests (patterns, negation, nested, wildcards)
- `test_indexer.py`: ~20 tests (scan, query, tree, read, visibility, stats, security)

Minimum: 28 passing tests.

## Success Criteria

- All tests pass: `pytest tests/hivenode/repo/ -v`
- Scan indexes a real repo (shiftcenter itself) without errors
- Gitignore rules correctly applied
- Path traversal attacks blocked
- `.git/` never indexed, never served
- Code is clean, well-documented, no magic numbers

---

**Model:** sonnet
**Estimate:** S (2-3 hours)

*Ready for dispatch.*
