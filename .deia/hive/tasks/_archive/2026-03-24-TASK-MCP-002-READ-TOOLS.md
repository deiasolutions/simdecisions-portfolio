# TASK-MCP-002: Hive MCP Read-Only Tools

## Objective
Implement read-only MCP tools: `queue_list`, `queue_peek`, `task_list`, `task_read`.

## Context
Phase 0 of SPEC-HIVE-MCP-001-v2. These are the first MCP tools exposed by the local hive server. They wrap filesystem reads of `.deia/hive/queue/` and `.deia/hive/tasks/` into typed tool calls.

**Dependencies:** TASK-MCP-001 (state.py must exist)

**Spec location:** `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`

## Files to Read First
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (sections 4.1, 7.2)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\state.py` (from TASK-MCP-001)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\` (sample spec files)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\` (sample task files)

## Deliverables
- [ ] Create `hivenode/hive_mcp/tools/queue.py`:
  - `queue_list(status: Optional[str], area_code: Optional[str], priority: Optional[str]) -> List[Dict]`
    - Lists specs in `.deia/hive/queue/`
    - Returns: `[{file_name, status, area_code, priority, created}, ...]`
    - Status: pending (in queue/), dispatched (claimed in state), dead (_needs_review/)
  - `queue_peek(spec_file: str) -> Dict`
    - Reads full spec file content
    - Returns: `{file_name, content, metadata}`
    - Validates spec_file path (must be in queue/ or _needs_review/)
- [ ] Create `hivenode/hive_mcp/tools/tasks.py`:
  - `task_list(assigned_bee: Optional[str], wave: Optional[str], status: Optional[str]) -> List[Dict]`
    - Lists task files in `.deia/hive/tasks/`
    - Returns: `[{file_name, assigned_bee, wave, status, created}, ...]`
    - Excludes _archive/ subdirectory
  - `task_read(task_file: str) -> Dict`
    - Reads full task file content
    - Parses YAML frontmatter if present
    - Returns: `{file_name, content, frontmatter}`
    - Validates task_file path (must be in tasks/, not _archive/)
- [ ] All tools use absolute paths internally (Path(_find_repo_root()) / ".deia/hive/...")
- [ ] All tools validate inputs (reject path traversal, ../, etc.)
- [ ] All tools return structured dicts (not raw strings)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test files:
  - `hivenode/hive_mcp/tests/test_tools_queue.py` (10+ tests)
  - `hivenode/hive_mcp/tests/test_tools_tasks.py` (10+ tests)
- [ ] Test coverage:
  - queue_list returns all specs in queue/
  - queue_list filters by status, area_code, priority
  - queue_peek reads spec content correctly
  - queue_peek rejects path traversal (../../etc/passwd)
  - task_list returns all tasks in tasks/
  - task_list excludes _archive/
  - task_list filters by assigned_bee, wave, status
  - task_read reads task content + frontmatter
  - task_read rejects path traversal
  - Empty directories return empty lists (not errors)
- [ ] All tests pass (minimum 20 tests total)
- [ ] Use tmp_path fixture for isolated filesystem tests

## Constraints
- No file over 500 lines
- No hardcoded colors (N/A — backend only)
- No stubs — every function fully implemented
- Python 3.13
- Use pathlib.Path for all file operations
- Return dicts, not Pydantic models (tools return plain JSON)
- Validate all user-supplied file paths (reject ../, absolute paths, etc.)
- Use `_find_repo_root()` helper (from hivenode.main) for repo root discovery

## Acceptance Criteria
- [ ] `queue_list` returns all specs in `.deia/hive/queue/` with correct metadata
- [ ] `queue_peek` reads spec file content without errors
- [ ] `task_list` returns all tasks in `.deia/hive/tasks/`, excludes _archive/
- [ ] `task_read` parses YAML frontmatter correctly
- [ ] All path traversal attempts rejected (../../../etc/passwd)
- [ ] All 20+ tests pass
- [ ] No stub functions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-002-RESPONSE.md`

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
