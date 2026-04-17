# TRIAGE ESCALATION: BL-146

**Date:** 2026-04-10 05:44:28 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-BL-146-BOT-ACTIVITY-PORT.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-09T15:50:45.741425Z — requeued (empty output)
- 2026-04-09T15:55:45.808044Z — requeued (empty output)
- 2026-04-10T05:41:49.956034Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-BL-146: Port Bot Activity + Bot Settings UI

## Objective

Port the bot token system and bot mutation API from platform/simdecisions-2 to shiftcenter. This gives each user a personal bot that can authenticate and act in efemera channels.

## Files to Read First

- hivenode/efemera/store.py
- hivenode/efemera/routes.py
- hivenode/routes/__init__.py

## Files to Modify

- hivenode/efemera/bot_store.py (new)
- hivenode/efemera/bot_routes.py (new)
- hivenode/efemera/keeper.py (new)
- hivenode/routes/__init__.py
- tests/hivenode/test_bot_store.py (new)
- tests/hivenode/test_bot_routes.py (new)

## Deliverables

- [ ] Bot store: hivenode/efemera/bot_store.py -- SQLite tables for bot tokens and mutations
- [ ] Bot routes: hivenode/efemera/bot_routes.py -- CRUD + mutation endpoints
- [ ] Keeper chat: hivenode/efemera/keeper.py -- ChatSender + ChatListener for efemera channels
- [ ] Tests for all of the above

## Acceptance Criteria

- [ ] Bot token CRUD works (create, read, revoke)
- [ ] One active bot per user enforced
- [ ] Token shown once on creation, stored as hash
- [ ] Bot mutation API accepts and validates mutations
- [ ] Keeper ChatSender can post to efemera channels as bot
- [ ] Keeper ChatListener can listen on channels for @mentions
- [ ] Rate limiting enforced (60/hour)
- [ ] All tests passing
- [ ] No stubs

## Smoke Test

- [ ] cd hivenode && python -m pytest tests/hivenode/test_bot_store.py -v -- tests pass
- [ ] cd hivenode && python -m pytest tests/hivenode/test_bot_routes.py -v -- tests pass
- [ ] cd hivenode && python -m pytest tests/ -v -- no regressions

## Constraints

- TDD, 500-line limit per file, Python 3.13
- Port from platform -- don't rewrite
- Use existing efemera store patterns (hivenode/efemera/store.py)
- Bot auth uses bearer token (not JWT)
- Bot token format: `sd_bot_{32_hex_chars}`, stored as SHA-256 hash
- User email format: `username-fr@nk.efemera.com` (internal identity format)

## Context

Source files in the platform repo (not in this repo -- read for porting reference):

**Bot Token System:**
- `platform/simdecisions-2/api/bot_token.py` -- SDBotToken model (1.3 KB)
- `platform/simdecisions-2/api/bot_service.py` -- Token generation, validation, lifecycle (4.7 KB)

**Bot Mutation API:**
- `platform/simdecisions-2/api/bot.py` -- Bot mutation endpoints + activity tracking (23 KB)
- `platform/simdecisions-2/api/bot_mutation.py` -- SDBotMutation model (1.8 KB)

**Keeper Chat (efemera integration):**
- `platform/efemera/keeper/chat.py` -- ChatSender + ChatListener classes (6 KB)

**Tests:**
- `platform/simdecisions-2/api/test_bot.py` -- Token tests (7.7 KB)
- `platform/simdecisions-2/api/test_bot_activity.py` -- Mutation listing/approval/rejection (11 KB)
- `platform/simdecisions-2/api/test_bot_mutate.py` -- Mutation validation + auto-mode (10 KB)

**Database Schema to Port:**
- `sd_bot_tokens` -- id, user_id, name, token_hash, token_prefix, created_at, last_used_at, revoked_at (unique constraint: one active per user)
- `sd_bot_mutations` -- id, bot_token_id, repo, scenario, mutations (JSON), message, status, pr_number, pr_url, commit_sha, commit_url, created_at, resolved_at

## Model Assignment

sonnet

## Priority

P1

## Triage History
- 2026-04-09T15:50:45.741425Z — requeued (empty output)
- 2026-04-09T15:55:45.808044Z — requeued (empty output)
- 2026-04-10T05:41:49.956034Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
