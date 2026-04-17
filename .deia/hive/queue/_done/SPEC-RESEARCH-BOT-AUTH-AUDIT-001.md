# SPEC-RESEARCH-BOT-AUTH-AUDIT-001: Bot Token Infrastructure Assessment

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Audit existing bot token systems across the platform repo (source), current hivenode/hodeia_auth codebase (target), and historical efemera keeper integration to determine what infrastructure exists, what can be ported, and what needs to be built for the CloudNode + BL-146 bot token integration. Research-only: produce a report that enables follow-up implementation specs.

## Files to Read First

- hivenode/routes/auth.py
- hivenode/identity.py
- hodeia_auth/main.py
- hodeia_auth/models.py
- hodeia_auth/routes/__init__.py
- docs/killed-specs-2026-04-10-intent.md
- .deia/hive/queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md

## Acceptance Criteria

- [ ] Report file written to `.deia/hive/responses/` with name `YYYY-MM-DD-HHMM-BEE-<model>-RESEARCH-BOT-AUTH-AUDIT-001.md`
- [ ] Platform bot system documented: `bot_token.py`, `bot_service.py`, `bot.py`, `bot_mutation.py` models/endpoints/fields (sourced from platform/simdecisions-2 repo if accessible; otherwise mark as "external, not accessible")
- [ ] Platform bot test coverage documented: `test_bot.py`, `test_bot_activity.py`, `test_bot_mutate.py` key flows listed
- [ ] Hivenode current auth infrastructure documented: existing models, endpoints, JWT/session flow, permission/scope model
- [ ] Hodeia_auth current schema documented: tables, relationships, routes
- [ ] Bot-adjacent code search completed in hivenode + hodeia_auth (grep for: bot, token, api_key) with results enumerated
- [ ] Efemera keeper historical integration documented: `chat.py` ChatSender/ChatListener architecture, WebSocket flow, @mention parsing, response mechanism (external repo; mark if inaccessible)
- [ ] Integration requirements enumerated: new tables needed in CloudNode, new endpoints, migration strategy (Alembic vs raw SQL)
- [ ] Portability assessment delivered: three lists (direct_port, needs_adaptation, complete_rewrite)
- [ ] Next-steps section lists ordered implementation specs with proposed SPEC IDs and one-line scope
- [ ] Report contains YAML block matching the Output Format schema in this spec
- [ ] No code changes made in either repo

## Smoke Test

- [ ] `ls .deia/hive/responses/ | grep RESEARCH-BOT-AUTH-AUDIT-001` returns exactly one file
- [ ] `grep -c "^- " .deia/hive/responses/*RESEARCH-BOT-AUTH-AUDIT-001*.md` >= 30 (minimum structured content)
- [ ] `git status` shows only the new response file (no other modifications)

## Constraints

- Read-only audit — no code changes in any repo
- Cross-repo access required — platform/simdecisions-2 and platform/efemera are sibling repos. If not accessible from the working tree, document what is needed and mark sections "external, not accessible"
- Time-boxed — 90 minutes maximum wall clock
- No stubs — every section of the report either contains the answer or explicitly states why it cannot be answered (with specific blocker)
- No git operations
- Security focus — document token storage (hashing?), validation flow, scoping/permissions patterns, and rate-limiting approach
- Report must include a "gaps" subsection listing every question that could not be fully answered and why

## Research Questions

### A. Platform Repo Bot Auth System (Source)

**A1:** What bot token models exist in `platform/simdecisions-2/api/`?
- File: `bot_token.py` — fields, constraints, relationships
- File: `bot_service.py` — CRUD operations, validation logic
- Database schema: tables, indexes, foreign keys

**A2:** What bot endpoints exist in `platform/simdecisions-2/api/bot.py`?
- Authentication flow — how do bots present tokens?
- Validation process — how are tokens verified?
- Rate limiting — what limits exist per token/user?
- Scoping — what permissions/capabilities are defined?

**A3:** What bot mutation/activity tracking exists?
- File: `bot_mutation.py` — actions logged
- Audit trail — what gets recorded for compliance
- Status tracking — how are bot operations monitored

**A4:** Test coverage — what flows are validated in `test_bot*.py`?

### B. CloudNode/Hivenode Current State (Target)

**B1:** What auth infrastructure exists?
- Models — User, session, JWT tables
- Endpoints — Login, validate, refresh
- Permission system — Role-based access, scoping

**B2:** Any existing bot-related code?
- Grep for "bot", "token", "api_key"
- Existing bot tables or models
- Validation endpoints that could be extended

**B3:** Database schema details
- PostgreSQL structure — existing tables
- Migration system — Alembic, raw SQL, other
- Connection patterns — SQLAlchemy, asyncpg, other ORM

**B4:** How does hodeia.me currently connect to CloudNode?
- API endpoints
- Request/response format
- Authentication flow

### C. Efemera Bot Integration (Historical)

**C1:** What bot participation existed in efemera?
- Bot posting API
- Authentication method
- Message format differentiation

**C2:** How did keeper `ChatSender`/`ChatListener` work?
- File: `platform/efemera/keeper/chat.py`
- WebSocket integration
- Command parsing — @mention handling
- Response mechanism

**C3:** What broke the bot→efemera integration? When? What changed?

### D. Integration Architecture

**D1:** Minimal CloudNode bot API for BL-146
- Required endpoints — create, validate, revoke, list
- Database additions
- Migration strategy

**D2:** How should hivenode validate bot tokens?
- Sync vs async validation calls
- Caching strategy
- Fallback behavior if CloudNode unreachable

**D3:** Keeper → CloudNode → efemera flow
- Authentication chain
- Command routing
- Response delivery

## Search Locations

### Platform Repo (sibling, external to this working tree)
- platform/simdecisions-2/api/bot_token.py
- platform/simdecisions-2/api/bot_service.py
- platform/simdecisions-2/api/bot.py
- platform/simdecisions-2/api/bot_mutation.py
- platform/simdecisions-2/api/test_bot*.py
- platform/efemera/keeper/chat.py

### Hivenode/Hodeia_auth (this repo)
- hivenode/routes/auth.py
- hivenode/identity.py
- hivenode/keeper/
- hodeia_auth/models.py
- hodeia_auth/routes/
- hodeia_auth/services/
- grep patterns: auth, token, user, jwt, bot, api_key

## Output Format

The report must include a YAML block with this structure:

```yaml
research_id: SPEC-RESEARCH-BOT-AUTH-AUDIT-001
completed_by: bee_id
completed_at: timestamp

platform_bot_system:
  models:
    bot_token: schema_description
    bot_mutation: schema_description
  endpoints:
    - path: endpoint_path
      method: GET_POST_or_DELETE
      purpose: description
  tests:
    coverage: description
    key_flows: list

cloudnode_current:
  auth_infrastructure:
    models: existing_models
    endpoints: existing_endpoints
    database: schema_summary
  bot_support:
    existing_code: yes_or_no_with_details
    extensibility: assessment

efemera_integration:
  historical_pattern: how_bots_worked
  keeper_architecture: chat_sender_listener_details
  broken_dependencies: what_needs_fixing

integration_requirements:
  cloudnode_additions:
    tables: new_tables
    endpoints: new_endpoints
    migrations: strategy
  hivenode_changes:
    validation_client: approach
    keeper_updates: changes
    fallback_strategy: offline_behavior

portability_assessment:
  direct_port: what_copies_as_is
  needs_adaptation: what_needs_changes
  complete_rewrite: what_must_be_built

gaps:
  - question_id_and_blocker_reason

next_steps:
  - spec_id_proposal_and_one_line_scope
```
