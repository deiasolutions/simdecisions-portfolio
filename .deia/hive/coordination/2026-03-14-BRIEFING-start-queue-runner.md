# BRIEFING: Start Queue Runner

**From:** Q88N
**To:** Q33NR
**Date:** 2026-03-14
**Status:** EXECUTE

---

## Objective

Start the queue runner to process pending specs in `.deia/hive/queue/`. Do NOT add any new specs to the queue. Only process what is already there.

## Pre-flight Checks

Before starting the queue runner:

1. Verify hivenode is running on port 8420 (needed for heartbeats):
   ```bash
   curl http://localhost:8420/health
   ```
   If not running, start it:
   ```bash
   python _tools/hivenode-service.py run &
   ```

2. List pending specs in the queue:
   ```bash
   ls .deia/hive/queue/*.md
   ```
   Exclude morning reports and event logs — only SPEC files get processed.

3. Move the orphaned fix-cycle spec to _done:
   ```bash
   mv .deia/hive/queue/2026-03-13-2251-SPEC-fix-deployment-wiring-retry.md .deia/hive/queue/_done/
   ```

## Start the Queue Runner

```bash
python .deia/hive/scripts/queue/run_queue.py
```

The runner will:
- Read all SPEC files from `.deia/hive/queue/`
- Sort by priority (P0 → P1 → P2)
- Process each spec through the dispatch chain
- Move completed specs to `_done/`
- Move specs needing human input to `_needs_review/`
- Log events to a session JSON file

## Constraints

- Do NOT add new specs to the queue
- Do NOT modify existing specs
- Do NOT skip the hivenode health check
- If the runner fails, report the error — do NOT retry without Q88N approval
- Budget ceiling: $20 per session (configured in queue.yml)

## Expected Queue Contents

| Spec | Priority | Description |
|------|----------|-------------|
| BL-126 kanban-backlog-db | P1 | Connect kanban to authoritative backlog DB |
| ra96it-sso-federation | P1 | SSO federation with Efemera identity |
