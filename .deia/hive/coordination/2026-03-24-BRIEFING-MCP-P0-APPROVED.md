# BRIEFING: MCP Phase 0 Tasks — APPROVED, DISPATCH NOW

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0
**Q88N has approved dispatch.**

---

## Status

Your 3 task files are APPROVED with one correction already applied:

**Correction (already made by Q33NR in TASK-MCP-003):**
- The MCP server is a **separate FastAPI app on port 8421**, NOT a router registered on the main hivenode app (port 8420). The task file has been updated. Do NOT register MCP routes in `hivenode/routes/__init__.py`.

## Your Job

Dispatch all 3 tasks sequentially. They have dependencies:

1. **TASK-MCP-001-STATE-MANAGER** — dispatch now
2. **TASK-MCP-002-READ-TOOLS** — dispatch after MCP-001 completes
3. **TASK-MCP-003-SSE-TRANSPORT** — dispatch after MCP-002 completes

All Sonnet bees. All `--inject-boot`.

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MCP-001-STATE-MANAGER.md --model sonnet --role bee --inject-boot
# Wait for completion, verify response
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MCP-002-READ-TOOLS.md --model sonnet --role bee --inject-boot
# Wait for completion, verify response
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-24-TASK-MCP-003-SSE-TRANSPORT.md --model sonnet --role bee --inject-boot
```

## Report

After all 3 bees complete, write a single response summarizing:
- Which tasks passed/failed
- Total test count
- Any issues or follow-ups
- Files created

Do not wait for my review between bees — dispatch sequentially on your own.
