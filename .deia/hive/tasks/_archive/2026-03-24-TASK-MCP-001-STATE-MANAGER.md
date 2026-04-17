# TASK-MCP-001: Hive MCP State Manager + JSON Persistence

## Objective
Scaffold `hivenode/hive_mcp/` package and implement in-memory state manager with JSON persistence to `~/.shiftcenter/hive_state/`.

## Context
Phase 0 of SPEC-HIVE-MCP-001-v2. Building the foundation layer for the Hive MCP Intercom Layer. The state manager holds all operational hive state (claims, task status, bee roster, heartbeats) in memory as Python dicts, with flush-to-JSON backup for restart recovery.

**Why no SQLite:** OneDrive file sync conflicts make SQLite unreliable in the synced repo directory. JSON backup goes outside OneDrive sync.

**Spec location:** `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`

## Files to Read First
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (sections 3.1, 3.4, 7.2)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (route registration pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (FastAPI app structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings pattern)

## Deliverables
- [ ] Create `hivenode/hive_mcp/` package structure:
  - `hivenode/hive_mcp/__init__.py` (empty exports for now)
  - `hivenode/hive_mcp/state.py` (state manager)
  - `hivenode/hive_mcp/tools/` (package for tools, empty __init__.py)
- [ ] Implement `state.py` with in-memory state manager:
  - Python dicts for: `task_claims`, `bee_roster`, `heartbeats`, `briefing_acks`
  - `StateManager` class with methods: `get_state()`, `update_state()`, `flush_to_disk()`, `load_from_disk()`
  - JSON persistence to `~/.shiftcenter/hive_state/hive_state.json`
  - Atomic writes (write to .tmp, rename)
  - Auto-flush on every write
  - Auto-load on init
- [ ] Create directory `~/.shiftcenter/hive_state/` if it doesn't exist
- [ ] All state operations thread-safe (use threading.Lock)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `hivenode/hive_mcp/tests/test_state.py`
- [ ] Test coverage:
  - StateManager init creates directory if missing
  - Empty state on first init
  - State persists across save/load cycles
  - Update operations modify in-memory state correctly
  - JSON files are valid and atomic (no partial writes)
  - Thread safety (concurrent reads/writes)
  - Handles corrupted JSON gracefully (creates new state file)
- [ ] All tests pass (minimum 15 tests)
- [ ] Edge cases: directory permissions, disk full simulation (mock), concurrent access

## Constraints
- No file over 500 lines
- No hardcoded colors (N/A — backend only)
- No stubs — every function fully implemented
- Python 3.13
- No SQLite for hive state
- State directory MUST be outside OneDrive sync (`~/.shiftcenter/`)
- Use pathlib.Path for all file operations
- Use json.dumps with indent=2 for readability

## Acceptance Criteria
- [ ] Package `hivenode/hive_mcp/` exists with __init__.py, state.py, tools/__init__.py
- [ ] StateManager loads empty state on first run
- [ ] StateManager persists state to `~/.shiftcenter/hive_state/hive_state.json`
- [ ] State survives process restart (load_from_disk works)
- [ ] All 15+ tests pass
- [ ] No stub functions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-001-RESPONSE.md`

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
