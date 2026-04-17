# BRIEFING: Process MCP Phase 1 Queue Specs

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Q88N has approved dispatch.**

---

## Your Job

4 specs are in `.deia/hive/queue/` for MCP Phase 1. Process them in order:

1. **SPEC-MCP-TRANSPORT-FIX** — dispatch first (no dependencies)
2. After transport fix completes, dispatch these 3 in parallel:
   - **SPEC-MCP-COORDINATION-TOOLS**
   - **SPEC-MCP-WRITE-TOOLS**
   - **SPEC-MCP-DISPATCH-TELEMETRY**

For each spec:
1. Read the spec from `.deia/hive/queue/`
2. Write a task file to `.deia/hive/tasks/`
3. Dispatch a Sonnet bee with `--inject-boot`
4. Wait for completion, verify response

All Sonnet bees. All `--inject-boot`.

The spec reference for all tasks is: `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md`

The existing Phase 0 code is in `hivenode/hive_mcp/` — bees must read it before building on top.

## Blanket Approval

You have blanket approval to create task files and dispatch all 4 bees without waiting for Q33NR review between them. Report results when all 4 are done.

## Constraints

- Sonnet bees, `--inject-boot`
- TDD, no stubs, 500-line limit
- Transport fix MUST complete before the other 3 dispatch (they depend on updated server)
