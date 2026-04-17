# SPEC-MCP-WRITE-TOOLS: Task Write, Response Submit, Task Archive

## Objective

Implement task_write, response_submit, task_archive MCP tools with frontmatter validation and structured error handling.

## Context

Phase 1 of SPEC-HIVE-MCP-001-v2. These are the write-side counterparts to the Phase 0 read tools. response_submit is the most important — it validates bee responses and returns actionable errors.

## Files to Read First
- hivenode/hive_mcp/local_server.py
- hivenode/hive_mcp/state.py
- hivenode/hive_mcp/tools/tasks.py
- hivenode/hive_mcp/tools/responses.py
- hivenode/hive_mcp/validators/frontmatter.py
- hivenode/hive_mcp/tests/test_tools_responses.py
- hivenode/hive_mcp/tests/test_tools_tasks.py

## Files to Modify
- hivenode/hive_mcp/tools/tasks.py
- hivenode/hive_mcp/tools/responses.py
- hivenode/hive_mcp/validators/frontmatter.py
- hivenode/hive_mcp/tests/test_tools_responses.py
- hivenode/hive_mcp/tests/test_tools_tasks.py
- hivenode/hive_mcp/local_server.py

## Deliverables
- [ ] task_write creates file in .deia/hive/tasks/ with naming validation
- [ ] task_archive moves to _archive/, rejects if no response file exists
- [ ] response_submit validates YAML frontmatter (features_delivered, features_modified, features_broken, test_summary)
- [ ] response_submit returns structured error on validation failure (spec section 8.1 format)
- [ ] 3-retry limit tracked, TASK_BLOCKED emitted after 3 failures
- [ ] response_read returns response content
- [ ] Tools registered in local_server.py

## Acceptance Criteria
- [ ] task_write creates file in .deia/hive/tasks/ with naming validation
- [ ] task_archive moves to _archive/, rejects if no response file exists
- [ ] response_submit validates frontmatter (features_delivered, features_modified, features_broken, test_summary)
- [ ] response_submit returns structured error on validation failure (spec section 8.1 format)
- [ ] 3-retry limit tracked, TASK_BLOCKED emitted after 3 failures
- [ ] response_read returns response content
- [ ] Path traversal rejected on all tools
- [ ] 15+ tests passing
- [ ] No stubs

## Smoke Test
- [ ] cd hivenode && python -m pytest hive_mcp/tests/test_tools_responses.py -v — all tests pass
- [ ] cd hivenode && python -m pytest hive_mcp/tests/test_tools_tasks.py -v — all tests pass
- [ ] cd hivenode && python -m pytest hive_mcp/tests/ -v — no regressions

## Constraints
- TDD, 500-line limit per file, Python 3.13
- Error format MUST match spec section 8.1 exactly
- Use state.py for retry tracking

## Depends On
- SPEC-MCP-TRANSPORT-FIX

## Model Assignment
sonnet

## Priority
P0
