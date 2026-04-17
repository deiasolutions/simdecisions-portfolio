# TASK-CLOUD-STORAGE-A: PostgreSQL Cloud Storage Store (TDD)

## Objective

Create PostgreSQL-backed storage module (`cloud_store.py`) with quota tracking, namespace isolation, and CRUD operations for cloud file storage on Railway hivenode. TDD approach.

---

## Context

Currently, cloud storage routes don't exist on the server side. The `CloudAdapter` (HTTP client) calls `/storage/*` routes, but those routes need a PostgreSQL backend instead of local filesystem.

This task creates the database layer. Two tables:

1. **`cloud_files`** — stores file content as BYTEA
2. **`cloud_quotas`** — tracks per-user storage usage with 10 MB limit

All operations enforce namespace isolation: users can only access `cloud://{user_id}/path/to/file` where `user_id` matches their JWT `sub` claim.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\database.py` — SQLAlchemy setup (Base, engine, DATABASE_URL)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\base.py` — BaseVolumeAdapter interface (for reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py` — CloudAdapter HTTP client (will call our new routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — settings object (database_url)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\conftest.py` — test fixtures pattern

---

## Deliverables

- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\cloud_store.py` (TDD)
- [ ] File created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cloud_store.py` (tests first)
- [ ] SQLAlchemy models for `cloud_files` and `cloud_quotas` tables
- [ ] Store functions: `write_file()`, `read_file()`, `list_files()`, `stat_file()`, `delete_file()`, `get_quota()`, `update_quota()`
- [ ] Quota enforcement in `write_file()` — raise `QuotaExceededError` if write would exceed limit
- [ ] Namespace isolation in all functions — user can only access their own namespace
- [ ] Auto-initialize quota row on first write (default: 10 MB = 10,485,760 bytes)
- [ ] Tests pass: minimum 18 unit tests

---

## Test Requirements (TDD — Write Tests First)

File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cloud_store.py`

Minimum 18 tests covering:

### Quota Enforcement (5 tests)
1. Write file within quota → success, `bytes_used` updated
2. Write file exceeding quota → raises `QuotaExceededError`
3. Multiple writes accumulate quota correctly
4. Delete file → `bytes_used` decremented
5. Overwrite file (same path) → `bytes_used` delta calculated correctly (not doubled)

### CRUD Operations (6 tests)
6. Write file → read file → content matches
7. Write file → stat file → size/timestamps correct
8. Write file → list directory → file appears in list
9. Delete file → read file → raises `FileNotFoundError`
10. Read nonexistent file → raises `FileNotFoundError`
11. List empty directory → returns empty list

### Namespace Isolation (4 tests)
12. User A writes `userA/file.txt` → success
13. User B reads `userA/file.txt` → raises `PermissionError`
14. User A lists `userA/` → only sees their files
15. User B lists `userB/` → doesn't see User A's files

### Quota Management (3 tests)
16. Get quota for new user → auto-initialized with 0 bytes_used
17. Get quota after write → returns correct `bytes_used`
18. Update quota manually → get quota returns new value

---

## Implementation Notes

### Database Schema (SQLAlchemy Core or ORM)

Use SQLAlchemy Core or ORM. Both tables should be created via `Base.metadata.create_all()` on module import or in init function.

**Table: `cloud_files`**
```python
class CloudFile(Base):
    __tablename__ = "cloud_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False, index=True)
    path = Column(Text, nullable=False)
    content = Column(LargeBinary, nullable=False)  # BYTEA in PostgreSQL
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('user_id', 'path', name='uq_user_path'),
        Index('idx_cloud_files_user', 'user_id'),
    )
```

**Table: `cloud_quotas`**
```python
class CloudQuota(Base):
    __tablename__ = "cloud_quotas"

    user_id = Column(String(255), primary_key=True)
    bytes_used = Column(BigInteger, default=0, nullable=False)
    quota_bytes = Column(BigInteger, default=10485760, nullable=False)  # 10 MB
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### URI Parsing Helper

```python
def parse_cloud_uri(uri: str) -> tuple[str, str]:
    """
    Parse cloud://user_id/path/to/file -> (user_id, path).

    Raises ValueError if URI is malformed.
    """
    if not uri.startswith("cloud://"):
        raise ValueError("Invalid cloud URI: must start with cloud://")

    rest = uri[8:]  # remove "cloud://"
    parts = rest.split("/", 1)

    if len(parts) < 2:
        raise ValueError("Cloud URI must include user_id and path: cloud://user_id/path")

    user_id = parts[0]
    path = parts[1]

    return user_id, path
```

### Quota Error Exception

```python
class QuotaExceededError(Exception):
    """Raised when write would exceed user's storage quota."""

    def __init__(self, bytes_used: int, quota_bytes: int):
        self.bytes_used = bytes_used
        self.quota_bytes = quota_bytes
        super().__init__(
            f"Quota exceeded: {bytes_used}/{quota_bytes} bytes used"
        )
```

### Store Functions

**`write_file(uri: str, content: bytes, user_id: str) -> dict`**

1. Parse URI to extract namespace user_id and path
2. Verify namespace: URI user_id must match function user_id (raise PermissionError if not)
3. Check if file exists (SELECT by user_id + path)
4. Calculate delta_bytes: if exists, `delta = len(content) - existing.size`, else `delta = len(content)`
5. Get quota (auto-create if not exists)
6. If `bytes_used + delta > quota_bytes`, raise `QuotaExceededError(bytes_used, quota_bytes)`
7. Upsert file row (INSERT or UPDATE on conflict)
8. Update quota: `bytes_used += delta`
9. Return `{"ok": True, "size": len(content)}`

**`read_file(uri: str, user_id: str) -> bytes`**

1. Parse URI
2. Verify namespace
3. SELECT content WHERE user_id = ? AND path = ?
4. If not found, raise FileNotFoundError
5. Return content bytes

**`list_files(uri: str, user_id: str) -> List[str]`**

1. Parse URI
2. Verify namespace
3. SELECT path WHERE user_id = ? AND path LIKE 'prefix/%'
4. Return list of relative paths

**`stat_file(uri: str, user_id: str) -> dict`**

1. Parse URI
2. Verify namespace
3. SELECT size, created_at, updated_at WHERE user_id = ? AND path = ?
4. If not found, raise FileNotFoundError
5. Return `{"size": size, "created": created_at, "modified": updated_at}`

**`delete_file(uri: str, user_id: str) -> dict`**

1. Parse URI
2. Verify namespace
3. SELECT size WHERE user_id = ? AND path = ?
4. If not found, raise FileNotFoundError
5. DELETE WHERE user_id = ? AND path = ?
6. Update quota: `bytes_used -= size`
7. Return `{"ok": True}`

**`get_quota(user_id: str) -> dict`**

1. SELECT * FROM cloud_quotas WHERE user_id = ?
2. If not exists, INSERT (bytes_used=0, quota_bytes=10485760)
3. Return `{"bytes_used": ..., "quota_bytes": ..., "updated_at": ...}`

**`update_quota(user_id: str, delta_bytes: int) -> None`**

1. Get or create quota row
2. UPDATE bytes_used = bytes_used + delta_bytes WHERE user_id = ?
3. UPDATE updated_at = NOW()

---

## Constraints

- **TDD:** Write tests first, then implementation
- **File size limit:** 500 lines. If `cloud_store.py` exceeds 500 lines, split into `cloud_store.py` (functions) and `cloud_models.py` (SQLAlchemy models)
- **No hardcoded connection string:** Use `from engine.database import engine, Base`
- **No stubs:** All functions fully implemented
- **Python 3.13**
- **Type hints:** All functions must have complete type annotations
- **Docstrings:** All public functions must have docstrings

---

## Acceptance Criteria

- [ ] `cloud_store.py` created with all 7 store functions
- [ ] SQLAlchemy models for `cloud_files` and `cloud_quotas`
- [ ] `QuotaExceededError` exception class
- [ ] `parse_cloud_uri()` helper function
- [ ] Quota enforcement: write fails when quota exceeded
- [ ] Namespace isolation: users cannot access other users' files
- [ ] Auto-initialize quota on first write (10 MB default)
- [ ] Tests written FIRST (TDD)
- [ ] All 18+ tests pass
- [ ] No file exceeds 500 lines
- [ ] No stubs
- [ ] Type hints on all functions
- [ ] Docstrings on all public functions

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-CLOUD-STORAGE-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Dependencies

None. This is the first task in the sequence.

---

## Test Command

```bash
cd hivenode && python -m pytest tests/hivenode/test_cloud_store.py -v
```
