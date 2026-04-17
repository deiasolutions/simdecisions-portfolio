# SPEC-RESEARCH-CLOUDNODE-AUDIT-001: Hivenode/Cloudnode Architecture Audit

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Audit the simdecisions repository to determine what infrastructure currently exists for: (1) local factory runtime (hivenode), (2) cloud coordination layer (cloudnode or equivalent on Railway), (3) communication between local and cloud, and (4) frontend-to-backend routing. Compare findings against the target architecture: Phone -> Frontend (Vercel) -> cloudnode (Railway) -> hivenode (local PC). This is a read-only research audit — no code changes.

## Files to Read First

- hivenode/main.py
- hivenode/config.py
- hivenode/queue_bridge.py
- hivenode/queue_watcher.py
- hivenode/scheduler/scheduler_daemon.py
- hivenode/scheduler/dispatcher_daemon.py
- hivenode/routes/build_monitor.py
- hivenode/routes/factory_routes.py
- hivenode/relay/store.py
- hivenode/hive_mcp/local_server.py
- Dockerfile
- railway.toml
- vercel.json
- browser/src/services/identity/identityService.ts

## Research Questions

### Hivenode (Local Runtime)

- Q1: What is the current entry point for hivenode? (main.py? uvicorn config?)
- Q2: What daemons/services run locally? (scheduler, dispatcher, queue watcher, triage, queue runner)
- Q3: Does hivenode currently check in with any remote service on boot?
- Q4: Does hivenode maintain a heartbeat or presence signal to any external endpoint?
- Q5: How does hivenode receive inbound commands today? (file watch? API? MCP?)

### Cloudnode (Railway Backend)

- Q6: What currently runs on Railway? Is it the same codebase as hivenode or a separate deployment?
- Q7: Is there any registry or tracking of connected hivenode instances?
- Q8: Is there a command relay mechanism from cloud to local?
- Q9: What API routes exist on the Railway deployment?
- Q10: Is there any offline queue or deferred command pattern?

### Frontend (Vercel)

- Q11: What backend URL does the frontend connect to? (Railway? localhost? configurable?)
- Q12: Does the frontend ever attempt to connect directly to hivenode?
- Q13: How is auth handled in frontend-to-backend calls?

### Communication Patterns

- Q14: Is there any WebSocket, SSE, or long-poll connection between hivenode and cloud?
- Q15: Is MCP used for any cloud-to-local communication?
- Q16: Are there any tunnel or reverse-proxy patterns in use (ngrok, cloudflared, etc.)?

## Output Format

Write findings as a YAML block in the response file covering: hivenode (entry_point, daemons, checkin_exists, heartbeat_exists, inbound_command_method), cloudnode (exists, location, registry_exists, relay_exists, api_routes, offline_queue), frontend (backend_url_config, direct_hivenode_connection, auth_method), communication (websocket, sse, mcp, tunnel). Include a gaps list (delta vs target architecture) and recommendations list (next specs to write).

## Acceptance Criteria

- [ ] All 16 research questions have an answer (even if "not found" or "unclear")
- [ ] Findings YAML block is populated with evidence (file paths and line numbers for each finding)
- [ ] Gaps list identifies delta between current state and target architecture (Phone -> Vercel -> Railway -> local)
- [ ] Recommendations list proposes concrete next specs or tasks
- [ ] No code changes made — audit is read-only
- [ ] Response file written to `.deia/hive/responses/`

## Smoke Test

- [ ] Response file exists and contains the findings YAML block
- [ ] All 16 questions have answers in the response

## Constraints

- No code changes — this is a read-only research audit
- No file modifications of any kind
- No git operations
- Report even if some findings are incomplete — partial answers are valuable
- The repo was flattened: there is no `packages/` directory and no separate `shiftcenter/` repo. Everything is in top-level dirs: `hivenode/`, `simdecisions/`, `browser/`, `_tools/`
