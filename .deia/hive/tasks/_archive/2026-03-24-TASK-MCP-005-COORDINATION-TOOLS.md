# TASK-MCP-005: Briefing Write/Read/Ack Tools

## Objective
Implement `briefing_write`, `briefing_read`, `briefing_ack` MCP tools for Q33NR ↔ Q33N coordination workflow, enabling acknowledged briefing delivery.

## Context
Phase 1 of SPEC-HIVE-MCP-001-v2. These tools enable the "walkie-talkie click" pattern where Q33NR knows Q33N received a briefing. Q33NR writes briefings, Q33N reads them, Q33N acknowledges receipt. The ack timestamp is written to both the briefing file header and the state manager.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` (to understand tool registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\state.py` (for ack storage)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\tasks.py` (similar pattern)
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (section 4.2)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\coordination.py`:
  - `briefing_write(filename: str, content: str)` — writes to `.deia/hive/coordination/`, enforces naming convention `YYYY-MM-DD-BRIEFING-*.md`
  - `briefing_read(filename: Optional[str])` — reads specified briefing or latest if no filename given
  - `briefing_ack(filename: str, bee_id: str)` — writes ack timestamp to briefing file YAML frontmatter, stores in state manager
- [ ] Register tools in `local_server.py`
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_coordination.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (10+ tests minimum)
- [ ] Edge cases tested:
  - Invalid filename format (rejects)
  - Path traversal attempts (rejects)
  - Missing file on read (error)
  - Latest file selection logic
  - Ack updates frontmatter correctly
  - Ack stores in state manager

## Constraints
- No file over 500 lines
- No stubs
- Python 3.13
- Use existing `state.py` for ack storage
- Naming convention MUST be: `YYYY-MM-DD-BRIEFING-*.md`
- Reject malformed names with actionable error message
- Path traversal MUST be rejected

## Acceptance Criteria
- [ ] briefing_write creates file in `.deia/hive/coordination/` with enforced naming
- [ ] briefing_write rejects malformed filenames
- [ ] briefing_write rejects path traversal attempts
- [ ] briefing_read returns latest briefing when no filename given
- [ ] briefing_read returns specified briefing when filename given
- [ ] briefing_ack writes timestamp to file YAML frontmatter header
- [ ] briefing_ack stores ack in state manager
- [ ] 10+ tests passing
- [ ] No stubs

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-005-RESPONSE.md`

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
