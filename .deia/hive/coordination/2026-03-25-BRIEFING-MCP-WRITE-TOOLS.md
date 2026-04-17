# BRIEFING: MCP Write Tools Implementation

**Date:** 2026-03-25
**From:** Q88NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** SPEC-MCP-WRITE-TOOLS (in `.deia/hive/queue/_active/`)

---

## Objective

Implement Phase 1 of SPEC-HIVE-MCP-001-v2: the write-side MCP tools (`task_write`, `response_submit`, `task_archive`) with frontmatter validation and structured error handling.

---

## Context

The MCP server now has:
- Phase 0 (read tools): `task_read`, `briefing_read`, `response_list` — COMPLETE (SPEC-MCP-TRANSPORT-FIX)
- Phase 1 (write tools): needs `task_write`, `response_submit`, `task_archive` — THIS BRIEFING

`response_submit` is the most critical — it validates bee responses and returns actionable errors per spec section 8.1 format. This enables Claude Code to self-correct during hive workflows.

---

## Files to Review

**Read these first to understand current structure:**
- `hivenode/hive_mcp/local_server.py` — server registration, existing read tools
- `hivenode/hive_mcp/state.py` — session state, retry tracking
- `hivenode/hive_mcp/tools/tasks.py` — task read tool (extend with write/archive)
- `hivenode/hive_mcp/tools/responses.py` — response read tool (extend with submit)
- `hivenode/hive_mcp/validators/frontmatter.py` — YAML frontmatter validation
- `hivenode/hive_mcp/tests/test_tools_responses.py` — response tool tests
- `hivenode/hive_mcp/tests/test_tools_tasks.py` — task tool tests

---

## Deliverables Breakdown

### 1. `task_write` Tool
- **Module:** `hivenode/hive_mcp/tools/tasks.py`
- **Function:** Create task file in `.deia/hive/tasks/` with naming validation
- **Naming pattern:** `YYYY-MM-DD-TASK-XXX-<SHORT-NAME>.md`
- **Validation:**
  - Reject relative paths (path traversal attack)
  - Validate task ID format
  - Check file doesn't already exist
- **Tests:** 5+ cases (valid write, duplicate rejection, path traversal, bad ID format, write failure)

### 2. `task_archive` Tool
- **Module:** `hivenode/hive_mcp/tools/tasks.py`
- **Function:** Move task file from `.deia/hive/tasks/` to `.deia/hive/tasks/_archive/`
- **Validation:**
  - Task file must exist
  - Response file must exist (reject archive if missing)
  - No path traversal
- **Tests:** 5+ cases (valid archive, missing response rejection, missing task, path traversal, already archived)

### 3. `response_submit` Tool
- **Module:** `hivenode/hive_mcp/tools/responses.py`
- **Function:** Validate and write bee response file to `.deia/hive/responses/`
- **Naming pattern:** `YYYYMMDD-<TASK-ID>-RESPONSE.md`
- **Frontmatter validation (YAML):**
  - `features_delivered`: list of strings
  - `features_modified`: list of strings
  - `features_broken`: list of strings
  - `test_summary`: object with `passed`, `failed`, `total` (all integers)
- **Error handling:**
  - On validation failure, return structured error per spec section 8.1 format
  - Track retry count in `state.py` (max 3)
  - On 3rd failure, emit `TASK_BLOCKED` event
- **Tests:** 10+ cases (valid submit, missing fields, bad types, retry tracking, 3-failure block, path traversal, duplicate write)

### 4. `response_read` Tool
- **Module:** `hivenode/hive_mcp/tools/responses.py`
- **Function:** Read and return response file content
- **Already exists?** Check if Phase 0 implemented this. If not, add it.
- **Tests:** 3+ cases (valid read, file not found, path traversal)

### 5. Frontmatter Validator
- **Module:** `hivenode/hive_mcp/validators/frontmatter.py`
- **Function:** Parse YAML frontmatter, validate schema
- **Schema enforcement:**
  ```yaml
  features_delivered: [str, str, ...]
  features_modified: [str, str, ...]
  features_broken: [str, str, ...]
  test_summary:
    passed: int
    failed: int
    total: int
  ```
- **Return:** Parsed data dict OR structured error dict (spec section 8.1 format)
- **Tests:** 8+ cases (valid YAML, missing fields, bad types, no frontmatter, malformed YAML)

### 6. Tool Registration
- **Module:** `hivenode/hive_mcp/local_server.py`
- **Update:** Register all 3 new tools in `list_tools()` and `call_tool()`
- **No test needed** (integration tests cover this)

---

## Spec Section 8.1 Error Format

When `response_submit` validation fails, return:

```json
{
  "error": "ValidationError",
  "message": "Response frontmatter validation failed",
  "missing_fields": ["features_delivered", "test_summary"],
  "invalid_fields": {
    "features_broken": "expected list, got str"
  },
  "retry_count": 1,
  "max_retries": 3
}
```

This format enables Claude Code to fix the response and resubmit.

---

## Constraints

- **TDD:** Write tests FIRST for each tool
- **500-line limit:** Each file under 500 lines (modularize if needed)
- **Python 3.13**
- **No stubs:** All functions fully implemented
- **Error format MUST match spec section 8.1 exactly** (critical for self-correction)
- **Use `state.py` for retry tracking** (not in-memory)

---

## Dependencies

- **SPEC-MCP-TRANSPORT-FIX** — COMPLETE (transport updated to MCP stdlib)

---

## Model Assignment

**Sonnet** (spec specifies)

---

## Priority

**P0** (blocks Phase 2 coordination tools)

---

## Acceptance Criteria (from spec)

- [ ] `task_write` creates file in `.deia/hive/tasks/` with naming validation
- [ ] `task_archive` moves to `_archive/`, rejects if no response file exists
- [ ] `response_submit` validates YAML frontmatter (features_delivered, features_modified, features_broken, test_summary)
- [ ] `response_submit` returns structured error on validation failure (spec section 8.1 format)
- [ ] 3-retry limit tracked, `TASK_BLOCKED` emitted after 3 failures
- [ ] `response_read` returns response content
- [ ] Path traversal rejected on all tools
- [ ] 15+ tests passing (5 task + 10 response + 8 validator minimum = 23 total)
- [ ] No stubs

---

## Smoke Test

```bash
cd hivenode && python -m pytest hive_mcp/tests/test_tools_responses.py -v
cd hivenode && python -m pytest hive_mcp/tests/test_tools_tasks.py -v
cd hivenode && python -m pytest hive_mcp/tests/ -v
```

All tests pass. No regressions on Phase 0 tools.

---

## Q33N: Next Steps

1. **Read the 7 files listed** to understand current structure
2. **Write task file(s)** for bee(s) to implement tools
   - Option A: 1 task for all 3 tools (if tightly coupled)
   - Option B: 3 tasks (task_write, response_submit, task_archive) if independent
   - Recommend: **1 task** (all tools share frontmatter validation and state tracking)
3. **Return task file(s) to Q88NR for review** (do NOT dispatch yet)
4. **After Q88NR approval:** Dispatch bee(s)
5. **After bee completion:** Review response files, verify tests pass, report to Q88NR

---

## Notes for Q33N

- The spec references "spec section 8.1 format" — this is the error format shown above. Bee must implement exactly this structure.
- Retry tracking in `state.py` must persist across tool calls (not in-memory). Check how Phase 0 tools use state.
- Path traversal rejection: use `os.path.abspath()` and verify result starts with `.deia/hive/` (Windows path format).
- Test count: spec requires "15+ tests" — allocate 5 task tests, 10 response tests, 8+ validator tests (total 23+).

---

**END BRIEFING**
