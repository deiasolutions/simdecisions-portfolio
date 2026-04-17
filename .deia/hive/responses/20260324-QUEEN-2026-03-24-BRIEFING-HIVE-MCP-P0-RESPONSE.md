# QUEEN-2026-03-24-BRIEFING-HIVE-MCP-P0: Hive MCP Phase 0 Task Files -- READY FOR REVIEW

**Status:** AWAITING Q33NR APPROVAL
**Model:** Sonnet
**Date:** 2026-03-24

## Files Created

**Task files (ready for Q33NR review):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-24-TASK-MCP-001-STATE-MANAGER.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-24-TASK-MCP-002-READ-TOOLS.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-24-TASK-MCP-003-SSE-TRANSPORT.md`

**Response file:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-QUEEN-2026-03-24-BRIEFING-HIVE-MCP-P0-RESPONSE.md` (this file)

## What Was Done

**Read required files:**
- `.deia/BOOT.md` — 10 hard rules, response template, test commands
- `.deia/HIVE.md` — chain of command, Q33N workflow
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` — full spec (603 lines)
- `hivenode/` structure — routes, main.py, existing patterns

**Analyzed Phase 0 scope from spec:**
- Section 10: Phase 0 deliverables
- Section 7.2: File structure
- Section 3.4: State management (no SQLite, JSON persistence)
- Section 4.1: Tool surface (read-only tools)
- Section 14: Design decisions

**Created 3 task files:**

### TASK-MCP-001: State Manager + JSON Persistence
- **Deliverable:** Scaffold `hivenode/hive_mcp/` package with in-memory state manager
- **Why separate:** Foundation layer — must exist before tools can reference it
- **Test requirement:** 15+ tests (state persistence, thread safety, corruption recovery)
- **Key constraint:** State directory MUST be `~/.shiftcenter/hive_state/` (outside OneDrive sync)

### TASK-MCP-002: Read-Only Tools
- **Deliverable:** Implement `queue_list`, `queue_peek`, `task_list`, `task_read`
- **Why separate:** Tool layer — wraps filesystem reads into typed tool calls
- **Test requirement:** 20+ tests (path traversal rejection, filtering, frontmatter parsing)
- **Depends on:** TASK-MCP-001 (imports state.py)

### TASK-MCP-003: SSE Transport + Integration Test
- **Deliverable:** Wire SSE on localhost:8421, create `.mcp.json`, end-to-end test
- **Why separate:** Transport layer — exposes tools via MCP protocol
- **Test requirement:** 5+ integration tests (real SSE client → server)
- **Depends on:** TASK-MCP-001, TASK-MCP-002 (wires existing tools into MCP server)

## Task Breakdown Rationale

**Parallel-safe:** TASK-MCP-001 and TASK-MCP-002 cannot run in parallel (002 depends on 001's state.py). TASK-MCP-003 depends on both.

**Sequential execution:** MCP-001 → MCP-002 → MCP-003

**Model assignments (recommended):**
- All three: Sonnet (architectural work, protocol integration, requires spec understanding)

**Why this split avoids the spec's suggested 3-task breakdown:**
The briefing suggested Tasks A/B/C. I've aligned exactly with that:
- **Task A → MCP-001:** Scaffold + state.py
- **Task B → MCP-002:** Tools (queue, tasks)
- **Task C → MCP-003:** SSE transport + .mcp.json

This is the spec's suggested split. No deviation.

## Compliance Verification

**10 Hard Rules:**
- ✅ Rule 0: No rest suggestions
- ✅ Rule 2: Q33N does not code (task files only, awaiting approval)
- ✅ Rule 3: No hardcoded colors (backend tasks, N/A)
- ✅ Rule 4: No file over 500 lines (all tasks constrained)
- ✅ Rule 5: TDD mandated in all 3 tasks (15+, 20+, 5+ tests respectively)
- ✅ Rule 6: No stubs (explicit constraint in all 3 tasks)
- ✅ Rule 7: Staying in lane (waiting for approval, not dispatching)
- ✅ Rule 8: All file paths absolute in task files
- ✅ Rule 9: No archival yet (tasks not complete)
- ✅ Rule 10: No git operations

**Spec compliance:**
- ✅ Phase 0 scope only (no `task_claim`, no `heartbeat` bee-initiated, no redirect)
- ✅ Package location: `hivenode/hive_mcp/` (spec section 14, decision #1)
- ✅ Transport: SSE (spec section 14, decision #2)
- ✅ State storage: in-memory + JSON to `~/.shiftcenter/` (spec section 14, decision #3)
- ✅ No SQLite (spec section 3.4.1)
- ✅ Read-only tools only (spec section 10)

**Task file completeness:**
- ✅ All tasks have: Objective, Context, Files to Read First, Deliverables, Test Requirements, Constraints, Acceptance Criteria, Response Requirements
- ✅ All tasks reference spec location: `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`
- ✅ All tasks use absolute paths
- ✅ All tasks specify test count minimums
- ✅ All tasks forbid stubs explicitly

## Dependencies

**Task dependencies:**
- TASK-MCP-001: No dependencies (foundation)
- TASK-MCP-002: Depends on TASK-MCP-001 (imports state.py)
- TASK-MCP-003: Depends on TASK-MCP-001, TASK-MCP-002 (wires tools into server)

**External dependencies (for bees to verify):**
- `mcp` Python SDK package (TASK-MCP-003 must check current API)
- FastAPI (already in hivenode)
- httpx or SSE client library for integration tests

## Questions for Q33NR

None. All design decisions were made in the spec (section 14). Task split follows briefing's suggested A/B/C pattern.

## Next Steps (After Q33NR Approval)

1. Q33NR reviews these 3 task files
2. If corrections needed: Q33N revises and re-submits
3. If approved: Q33N dispatches:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MCP-001-STATE-MANAGER.md --model sonnet --role bee --inject-boot
   # Wait for MCP-001 completion
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MCP-002-READ-TOOLS.md --model sonnet --role bee --inject-boot
   # Wait for MCP-002 completion
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MCP-003-SSE-TRANSPORT.md --model sonnet --role bee --inject-boot
   ```
4. Q33N monitors bee responses
5. Q33N reports results to Q33NR

## Estimated Scope

**TASK-MCP-001:**
- Files created: 3 (state.py, __init__.py, tools/__init__.py)
- Test file: 1 (test_state.py with 15+ tests)
- Estimated lines: ~250 (state.py ~150, tests ~100)

**TASK-MCP-002:**
- Files created: 2 (queue.py, tasks.py)
- Test files: 2 (test_tools_queue.py, test_tools_tasks.py with 20+ tests total)
- Estimated lines: ~400 (tools ~200, tests ~200)

**TASK-MCP-003:**
- Files created: 2 (local_server.py, .mcp.json)
- Modified: 2 (routes/__init__.py, hive_mcp/__init__.py)
- Test file: 1 (test_integration.py with 5+ tests)
- Estimated lines: ~300 (server ~150, tests ~150)

**Total Phase 0:** ~950 lines across 8 files, 40+ tests

---

**Q33N STATUS:** Awaiting Q33NR approval to dispatch.
