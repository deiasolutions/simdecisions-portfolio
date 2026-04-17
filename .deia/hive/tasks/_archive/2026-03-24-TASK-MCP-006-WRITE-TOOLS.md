# TASK-MCP-006: Task Write, Response Submit, Task Archive Tools

## Objective
Implement `task_write`, `response_submit`, `response_read`, `task_archive` MCP tools with frontmatter validation and structured error handling per spec section 8.1.

## Context
Phase 1 of SPEC-HIVE-MCP-001-v2. These are the write-side counterparts to Phase 0 read tools. `response_submit` is the most important tool — it validates bee response YAML frontmatter and returns structured errors when validation fails. After 3 validation failures for the same task, emit a TASK_BLOCKED event.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` (tool registration pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\state.py` (retry tracking storage)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\tasks.py` (similar patterns)
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (sections 4.1, 8.1, 8.2, 7.4)

## Deliverables
- [ ] Extend `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\tasks.py` OR create new `responses.py` if tasks.py approaches 500 lines:
  - `task_write(filename: str, content: str)` — writes to `.deia/hive/tasks/`, validates naming convention
  - `task_archive(task_file: str)` — moves to `_archive/`, enforces PROCESS-0002 (requires response file exists)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\responses.py`:
  - `response_submit(filename: str, content: str)` — writes to `.deia/hive/responses/`, validates YAML frontmatter
  - `response_read(filename: str)` — reads response file
  - Frontmatter MUST have: `features_delivered`, `features_modified`, `features_broken`, `test_summary`
  - On validation failure, return structured error per spec section 8.1:
    ```json
    {
      "error": "validation_failed",
      "tool": "response_submit",
      "violations": [{"field": "...", "issue": "missing", "fix": "..."}],
      "retryable": true
    }
    ```
  - Track retry count per task in state manager — after 3 failures emit TASK_BLOCKED event
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\validators\frontmatter.py`:
  - YAML frontmatter parser
  - Validator with required fields check
  - Violation report generator
- [ ] Register tools in `local_server.py`
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_responses.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (15+ tests minimum)
- [ ] Edge cases tested:
  - task_write with malformed filename (rejects)
  - task_write with path traversal (rejects)
  - task_archive without response file (rejects)
  - response_submit with missing frontmatter fields (structured error)
  - response_submit with invalid YAML (structured error)
  - response_submit 3-retry limit and TASK_BLOCKED event
  - response_read with nonexistent file (error)

## Constraints
- No file over 500 lines
- No stubs
- Python 3.13
- Error format MUST match spec section 8.1 exactly
- Use `state.py` for retry tracking
- Task naming convention: `YYYY-MM-DD-TASK-*.md`
- Response naming convention: `YYYYMMDD-TASK-*-RESPONSE.md`

## Acceptance Criteria
- [ ] task_write creates file in `.deia/hive/tasks/` with naming validation
- [ ] task_archive moves to `_archive/`, rejects if no response file exists
- [ ] response_submit validates frontmatter (features_delivered, features_modified, features_broken, test_summary)
- [ ] response_submit returns structured error on validation failure (spec section 8.1 format)
- [ ] 3-retry limit tracked in state manager
- [ ] TASK_BLOCKED event emitted after 3 validation failures
- [ ] response_read returns response content
- [ ] Path traversal rejected on all tools
- [ ] 15+ tests passing
- [ ] No stubs

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-006-RESPONSE.md`

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
