# QUEUE-TEMP-SPEC-MCP-BEE-HEARTBEAT: Inject MCP Heartbeat Instructions into Bee Prompts -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-26

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py (added _build_mcp_instructions function and injection logic)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\dispatch\test_dispatch_mcp_injection.py (new file — 10 tests)

## What Was Done

- Added `_build_mcp_instructions(task_id)` function to dispatch.py
  - Returns markdown-formatted MCP usage instructions
  - Includes task_id in heartbeat call template
  - References correct tool names: heartbeat, status_report, cost_summary
  - Clearly marks MCP calls as optional/best-effort
  - Instructs bee to use bot ID from role header
  - References correct MCP server port (8421)
- Integrated MCP instruction injection into `dispatch_bee()` function
  - Injected only for bee role (not queen or regent)
  - Appended after governance docs section
  - Does not affect dispatch behavior if MCP server is down
- Created comprehensive test file with 10 tests
  - Tests function existence and return type
  - Verifies tool names present (heartbeat, status_report, cost_summary)
  - Verifies task_id included in instructions
  - Verifies optional/best-effort language present
  - Verifies port 8421 referenced
  - Verifies bot ID usage instructions
  - Tests role-specific injection (bee only, not queen)
  - Tests injection order (after governance docs)
- All 17 dispatch tests pass (7 existing + 10 new)

## Test Results

```
tests/dispatch/test_dispatch_cleanup_integration.py::TestDispatchChildProcessCleanupIntegration — 7 passed
tests/dispatch/test_dispatch_mcp_injection.py::TestMCPInstructionInjection — 10 passed

Total: 17 passed in 0.07s
```

## Deliverables

- [x] New function `_build_mcp_instructions()` returns MCP usage prompt text
- [x] Instructions appended to bee prompt after governance docs section
- [x] Instructions tell bee to: heartbeat every 5 minutes, status_report on each major step, cost_summary on completion
- [x] Instructions explicitly state: MCP is best-effort, do NOT stop work if MCP calls fail
- [x] Only injected for bee role (not queen, not regent)

## Acceptance Criteria

- [x] Dispatched bee prompt contains MCP usage instructions
- [x] Instructions reference correct tool names (heartbeat, status_report, cost_summary)
- [x] Instructions include the spec name as identifier in heartbeat calls
- [x] MCP section clearly marked as optional/best-effort
- [x] No change to dispatch behavior if MCP server is not running
- [x] Existing dispatch tests still pass

## Test Requirements

- [x] Test: MCP instructions present in bee prompt
- [x] Test: MCP instructions NOT present in queen prompt
- [x] Test: instructions contain heartbeat, status_report, cost_summary tool names
- [x] All existing dispatch tests pass
- [x] 10 new tests (exceeds minimum of 3)

## Smoke Test

- [x] python -m pytest tests/dispatch/test_dispatch*.py -v — all pass (17/17)

## CLOCK / COIN / CARBON

- **CLOCK:** ~8 minutes
- **COIN:** ~$0.05 (haiku execution)
- **CARBON:** Negligible

## Features Delivered

- FEAT-MCP-BEE-HEARTBEAT-INJECTION — MCP instructions automatically injected into all bee prompts

## Features Modified

- None (pure extension)

## Features Broken

- None

## Notes

MCP instruction injection is now live for all bee dispatches. Bees will see instructions at the end of their prompts telling them to use the MCP heartbeat, status_report, and cost_summary tools. Instructions are clearly marked as optional/best-effort, so bees will not fail if MCP server is down.

The implementation is minimal and non-invasive:
- Single new function (_build_mcp_instructions)
- Single conditional injection (if role == "bee")
- No changes to existing logic or control flow
- All existing tests pass

Next steps (if needed):
- Monitor bee logs to verify they follow MCP instructions
- Adjust frequency or wording if bees ignore or misinterpret instructions
- Consider adding MCP usage metrics to build monitor
