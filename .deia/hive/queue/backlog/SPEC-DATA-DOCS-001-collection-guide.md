---
id: DATA-DOCS-001
priority: P1
model: haiku
depends_on: BEE-TELEMETRY-001
area_code: docs
---

# SPEC-DATA-DOCS-001: Data Collection and Query Guide

## Priority
P1

## Depends On
SPEC-BEE-TELEMETRY-001 (documents the new telemetry system it creates)

## Model Assignment
haiku

## Objective

Write a single reference document that maps every question an operator might ask ("how did the benchmark go?", "which bees are hanging?", "what's our cost burn rate?") to the exact data source and query command. Currently answering basic questions about benchmark runs requires 20+ minutes of agent research across scattered files. This doc makes it 2 minutes.

## Files to Read First

- `.deia/hive/queue/monitor-state.json` — build monitor state
- `hivenode/routes/build_monitor.py` — BuildState endpoints
- `hivenode/hive_mcp/tools/telemetry.py` — MCP telemetry tools
- `hivenode/telemetry/bee_events.py` — bee lifecycle event log (created by BEE-TELEMETRY-001)
- `_tools/analyze_swebench.py` — benchmark analysis script
- `_tools/inventory.py` — feature inventory CLI
- `.deia/hive/responses/` — response file format (read 1-2 examples)

## Deliverables

- [ ] Create `docs/DATA-COLLECTION-GUIDE.md` with these sections:

### Section 1: Data Sources Map
Table mapping each data source to its location, format, retention, and what questions it answers:
- RAW response files (`.deia/hive/responses/*-RAW.txt`)
- RESPONSE files (`.deia/hive/responses/*-RESPONSE.md`)
- Bee events DB (`.deia/hive/bee_events.db`)
- Monitor state (`monitor-state.json`)
- Queue runner log (`queue_runner.log`)
- Dispatcher log (`dispatcher.log`)
- Event ledger (`.deia/hive/event_ledger.db`)
- Inventory DB (Railway PG)
- Benchmark results (`.deia/benchmark/results/`)
- Patches (`.deia/benchmark/swebench/patches/`)

### Section 2: Common Queries
For each question, the exact command or query:
- "How did the last benchmark run go?" → `bee-telemetry run-summary --start X --end Y`
- "What's the concurrency profile?" → `bee-telemetry concurrency --start X --end Y`
- "Which bees are currently running?" → `curl -s http://127.0.0.1:8420/build/status`
- "Is anything hanging?" → check stall advisory via MCP heartbeat
- "What's our cost so far?" → `bee-telemetry cost --start X --end Y`
- "How many specs are in the queue?" → `curl -s http://127.0.0.1:8420/build/status` or `ls .deia/hive/queue/backlog/`
- "Did a specific bee fail?" → `bee-telemetry timeline <bee_id>`
- "What's our inventory count?" → `python _tools/inventory.py stats`

### Section 3: File Format Reference
Document the exact format of:
- RAW file headers (Success, Duration, Cost, Turns, Files modified)
- RESPONSE file 8-section template
- bee_events.db schema
- monitor-state.json schema

### Section 4: Troubleshooting
- "I see a bee that ran for 18 hours" → how to find it, how to kill it
- "Rate limit hit" → how to check cooldown status, how to resume
- "Queue runner died" → how to check, how to restart
- "MCP server down" → how to check, how to restart

## Test Requirements

- [ ] No code tests needed (documentation only)
- [ ] Verify all referenced commands actually work by running them
- [ ] Verify all file paths are correct

## Constraints

- No file over 500 lines (split into sub-docs if needed)
- No stubs
- No git operations
- Use absolute paths in all examples
- All timestamps in CDT (UTC-5)
