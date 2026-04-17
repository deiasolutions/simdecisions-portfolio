# SPEC-MOBILE-SUBMIT-001: Phone -> Chat -> Factory Spec Submission Flow (Research)

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Audit and design the end-to-end flow for submitting a spec from Q88N's phone into the factory. Target flow: Q88N types or pastes a spec into the browser chat interface on his phone, the chat asks "submit to factory?", on yes cloudnode (Railway) relays the payload to hivenode (local PC) which writes the spec file into `.deia/hive/queue/backlog/`. Identify why the chat interface does not currently work, inventory what submission and relay infrastructure already exists, and produce a concrete implementation plan as a ranked list of follow-on specs. This is a read-only research audit — no code changes.

## Files to Read First

- browser/src/primitives/conversation-pane/ConversationPane.tsx
- browser/src/primitives/conversation-pane/index.ts
- browser/src/apps/conversationPaneAdapter.tsx
- browser/src/apps/specSubmitAdapter.tsx
- browser/src/services/chat
- browser/src/services/hivenodeUrl.ts
- browser/src/services/identity/identityService.ts
- hivenode/routes/llm_chat_routes.py
- hivenode/routes/canvas_chat.py
- hivenode/routes/factory_routes.py
- hivenode/main.py
- hivenode/config.py
- hivenode/node/client.py
- hivenode/node/heartbeat.py
- hivenode/node_store.py
- hivenode/routes/node.py
- vercel.json
- railway.toml
- .deia/hive/responses/20260414-SPEC-RESEARCH-CLOUDNODE-AUDIT-001-RESPONSE.md
- .deia/hive/queue/_done/SPEC-FACTORY-005-SPEC-SUBMIT.md
- .deia/hive/queue/_done/SPEC-FACTORY-SPECSUBMIT-001-fix-gate0.md
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Research Questions

### A. Chat Interface Current State

- A1: Where does the chat primitive (`ConversationPane`) send messages today? Which service module, which HTTP endpoint?
- A2: Is the chat backed by a vendor LLM route, a hivenode-local route, an Efemera channel, or nothing at all? Cite file and line.
- A3: What is the observed breakage? Read recent chat-related specs in `_done/` (SPEC-TASK-BUG030 chat-tree-empty series, SPEC-EFEMERA-CONN-04-textpane-chat, SPEC-CHROME-CHAT-*). Identify what still fails.
- A4: Does the chat work on desktop today? Does it work on mobile? If different, why?
- A5: Is there existing logic that detects "the user pasted a spec" vs normal chat? (look at specSubmitAdapter.tsx).

### B. Existing Submit Infrastructure

- B1: Does `specSubmitAdapter.tsx` produce spec files today? Where does it POST? Which hivenode route handles the submission?
- B2: Does `hivenode/routes/factory_routes.py` expose a POST endpoint that writes a file under `.deia/hive/queue/backlog/`? If yes, confirm the route path, auth requirements, payload schema, and gate0 validation hook.
- B3: What does `SPEC-FACTORY-005-SPEC-SUBMIT` (done) actually deliver? What does `SPEC-FACTORY-SPECSUBMIT-001-fix-gate0` (done) fix? Summarize the delta.
- B4: Is there a confirmation/review step before the file lands in `backlog/`? If not, where should it go?

### C. Cloud-to-Local Relay Status

- C1: Re-check the 2026-04-14 cloudnode audit findings: as of today, are any of the recommended relay specs (CLOUDNODE-RELAY-001, CLOUDNODE-QUEUE-001, CLOUDNODE-DISPATCH-001, CLOUDNODE-POLLING-001) in `_done/`, `_active/`, or `backlog/`?
- C2: If no relay is implemented, what is the minimum viable path for cloud -> local spec delivery? Compare WebSocket relay vs polling vs tunnel (ngrok/cloudflared). Pick ONE and justify.
- C3: In `HIVENODE_MODE=local` (Q88N's PC today), does hivenode contact the Railway cloudnode at all? If not, what toggle or config change is required to make it `remote` and start heartbeating?
- C4: Does Railway cloudnode expose a route that a phone (via Vercel proxy) could POST a spec to, which then reaches the local hivenode? If not, that gap is the primary deliverable of a follow-on spec.

### D. Auth & Identity

- D1: How is Q88N's phone authenticated against the Vercel frontend today? Is the JWT from hodeia.me durable across phone reloads?
- D2: Does the cloud-mode hivenode on Railway require JWT on the spec-submit route? If yes, how does Q88N's phone get a token scoped to his node?
- D3: Is there a `node_id` → `user_id` mapping that ensures specs from Q88N's phone only reach Q88N's hivenode (not some other user's)?

### E. Target Flow Concrete Design

Propose a concrete wire-level design for the target flow. For each hop, name the exact endpoint, method, payload, and response:

1. Phone (browser) -> Vercel same-origin chat POST
2. Vercel proxy -> Railway cloudnode route
3. Cloudnode -> local hivenode relay (WebSocket, polling, or tunnel)
4. Hivenode -> file drop in `.deia/hive/queue/backlog/`
5. Response ack flowing back up to the phone

## Deliverables

- Single research report file at `.deia/hive/responses/YYYYMMDD-SPEC-MOBILE-SUBMIT-001-RESPONSE.md`
- Report must include:
  - Answers to every question in sections A through D, with file paths and line numbers as evidence
  - A "Current State" narrative paragraph: what works, what is broken, what is missing
  - Section E: wire-level design for the target flow
  - Ranked list of follow-on implementation specs (at least 3), each with: proposed SPEC-ID, 1-sentence objective, model assignment recommendation, rough effort (small/medium/large), blocking dependencies
  - A minimum viable path (MVP) called out explicitly: the smallest set of follow-on specs that get the basic flow working end-to-end

## Acceptance Criteria

- [ ] Every question A1 through E (items 1-5) has a concrete answer with file:line evidence or a clearly stated "not found" with search scope documented
- [ ] Chat breakage root cause is identified with evidence (stack trace, missing endpoint, auth failure, or similar)
- [ ] Current state narrative is present and accurate
- [ ] Wire-level design for all 5 hops is present
- [ ] At least 3 follow-on specs are proposed, each with SPEC-ID, objective, model, effort, and dependencies
- [ ] MVP path is explicitly called out as a subset of the follow-on specs
- [ ] Report file written to `.deia/hive/responses/` with the standard 8-section response header
- [ ] No code changes — this is read-only research

## Smoke Test

- [ ] Verify the response file exists: test -f .deia/hive/responses/*SPEC-MOBILE-SUBMIT-001*RESPONSE.md
- [ ] Verify the report answers all questions: grep -c "^- A[1-5]:\|^- B[1-4]:\|^- C[1-4]:\|^- D[1-3]:" on the response file returns at least 16
- [ ] Verify at least 3 follow-on specs are listed: grep -c "^[0-9]\+\. SPEC-" on the response file returns at least 3

## Constraints

- No code changes — this is a read-only research audit
- No file modifications of any kind outside the single response file
- No git operations
- No bee dispatches
- Output specs listed in the report are recommendations only — do not create spec files; Q88N will approve before any are written
- Do not re-run the 2026-04-14 cloudnode audit — read its response file and build on it
- Report is the only deliverable
