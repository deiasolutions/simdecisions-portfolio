# TASK-ESC-001: Escalation Chain Survey — Cross-Repo Forensics

## Objective
Produce a forensic survey report identifying canonical sources for 15 spec families polluted by recursive escalation loop, with dispositions for Phase 2 restore.

## Context

During 2026-04-09/10, a triage daemon in shiftcenter entered a recursive escalation loop:
- Empty bee output → prepend `## Clean Retry` → requeue
- Retry fails → prepend ANOTHER `## Clean Retry`
- After 3 retries → escalate to `_escalated/`, create `.rejection.md`
- Rejection file itself gets re-escalated → `.rejection.rejection.md`, etc.
- Deepest chain: 10+ levels

These polluted files were imported into simdecisions via `3228763 v0.1.0-cutover`. Original clean specs exist in shiftcenter git history on branch `wip/factory-refactor-20260411` (commit `dd2eedf` or earlier).

**Your job:** Survey BOTH repos (read-only), identify canonical sources, determine disposition for each spec family.

**Repo Geometry:**
- **simdecisions (target for Phase 2 writes):** `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions`
- **shiftcenter (read-only forensic source):** `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter`
- **shiftcenter forensic branch:** `wip/factory-refactor-20260411` (commit `dd2eedf`)

## Files to Read First

**In simdecisions working tree:**
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_escalated/` — polluted originals
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/backlog/` — rejection chains
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/` — check for newer versions
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_done/` — check if already built
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/docs/specs/` — check for existing implementations

**In shiftcenter (read-only via git only):**
- Use `git show wip/factory-refactor-20260411:<path>` or `git show <commit>:<path>` — NEVER checkout
- Use `git log --follow --all --oneline -- '.deia/hive/queue/**/*<name>*'` to find history

## Deliverables

- [ ] Forensic survey report: `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260410-ESC-001-RESPONSE.md`
- [ ] Disposition table covering all 15 spec families (see table below)
- [ ] For each `RESTORE` disposition: cite shiftcenter commit + path
- [ ] For each `SKIP_*` or `KILL` disposition: cite superseding file or implementation path

## Spec Families to Survey (15 total)

| Spec Family | Simdecisions Path Candidate |
|-------------|-----------------------------|
| GAMIFICATION-V1 | `.deia/hive/queue/_escalated/SPEC-GAMIFICATION-V1.md` |
| EVENT-LEDGER-GAMIFICATION | `.deia/hive/queue/_escalated/SPEC-EVENT-LEDGER-GAMIFICATION.md` |
| ML-TRAINING-V1 | `.deia/hive/queue/_escalated/SPEC-ML-TRAINING-V1.md` |
| FLAPPY-100 | `.deia/hive/queue/_escalated/SPEC-FLAPPY-100-self-learning-v2.md` |
| BL-146 | `.deia/hive/queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md` |
| WIKI-SYSTEM | `.deia/hive/queue/_escalated/SPEC-WIKI-SYSTEM.md` |
| WIKI-V1 | `.deia/hive/queue/_escalated/SPEC-WIKI-V1.md` |
| WIKI-V1.1-LLM-WIKI-PATTERN | `.deia/hive/queue/_escalated/SPEC-WIKI-V1.1-LLM-WIKI-PATTERN.md` |
| WIKI-103 | `.deia/hive/queue/_escalated/SPEC-WIKI-103-crud-api-routes.md` |
| WIKI-108 | `.deia/hive/queue/_escalated/SPEC-WIKI-108-egg-integration.md` |
| WIKI-SURVEY-000 | search `.deia/hive/queue/` for `*WIKI-SURVEY*` |
| MW-VERIFY-001 | `.deia/hive/queue/_escalated/SPEC-MW-VERIFY-001-full-audit.md` |
| RAIDEN-000 | `.deia/hive/queue/_escalated/SPEC-RAIDEN-000-master-coordination.md` |
| GITHUB-005 | search for `*GITHUB-005*` |
| TRIAGE-ESCALATED-001 | `.deia/hive/queue/_escalated/SPEC-TRIAGE-ESCALATED-001.md` |

## Disposition Options

For each spec family, assign ONE disposition:

- **RESTORE** — canonical clean version found in shiftcenter git, restore to simdecisions `_needs_review/`
- **RESTORE_WITH_STRIP** — simdecisions version has prepended pollution, strip it and restore
- **SKIP_SUPERSEDED** — newer version exists in simdecisions, no action needed
- **SKIP_BUILT** — already implemented in simdecisions codebase
- **HOLD_Q88N** — no clean original, ambiguous content, Q88N must decide
- **KILL** — spec is obsolete or broken beyond rescue

## Work Process

For each spec family:

1. **Inspect simdecisions current state:**
   ```bash
   cd C:/Users/davee/OneDrive/Documents/GitHub/simdecisions
   ls -la .deia/hive/queue/_escalated/SPEC-<name>*
   cat .deia/hive/queue/_escalated/SPEC-<name>.md | head -100
   ```

2. **Check for prepended pollution:**
   - Count `## Clean Retry` blocks
   - Count `## Triage History` sections
   - Identify line/byte offset where real spec starts

3. **Search shiftcenter git history:**
   ```bash
   cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
   git log --follow --all --oneline -- '.deia/hive/queue/**/*<name>*'
   git show <earliest-clean-commit>:.deia/hive/queue/<path>
   ```
   Target: earliest commit BEFORE daemon loop (likely on main or wip/factory-refactor-20260411 before escalation started)

4. **Check for newer versions in simdecisions:**
   ```bash
   cd C:/Users/davee/OneDrive/Documents/GitHub/simdecisions
   ls -la .deia/hive/queue/backlog/*<name>*
   ls -la .deia/hive/queue/_needs_review/*<name>*
   ```

5. **Check if already built:**
   ```bash
   cd C:/Users/davee/OneDrive/Documents/GitHub/simdecisions
   ls -la .deia/hive/queue/_done/*<name>*
   ls -la docs/specs/*<name>*
   grep -r "<feature-name>" packages/*/src/
   ```

6. **Record findings in disposition table** (see Test Requirements)

## Test Requirements

- [ ] Disposition table complete with one row per spec family
- [ ] Every `RESTORE` has shiftcenter commit + path cited
- [ ] Every `SKIP_*` and `KILL` has superseding file or implementation path cited
- [ ] Evidence column populated for all 15 rows
- [ ] Table format matches example below

**Disposition Table Format:**

```markdown
| Spec Family | Canonical Source | Status | Disposition | Evidence |
|-------------|------------------|--------|-------------|----------|
| GAMIFICATION-V1 | shiftcenter@dd2eedf:.deia/hive/queue/_needs_review/SPEC-GAMIFICATION-V1.md | CLEAN_ORIG_FOUND | RESTORE | No prepended blocks in shiftcenter@dd2eedf, 3 Clean Retry blocks in simdecisions _escalated/ |
| ML-TRAINING-V1 | shiftcenter@<commit>:<path> | CLEAN_ORIG_FOUND | RESTORE_WITH_STRIP | ... |
| WIKI-103 | simdecisions:.deia/hive/queue/backlog/SPEC-WIKI-104-backlinks-query.md | SUPERSEDED | SKIP_SUPERSEDED | WIKI-104 is the updated version |
| ... | ... | ... | ... | ... |
```

## Constraints

- **Read-only.** Zero writes to either repo.
- **No git checkout** in shiftcenter — use `git show <commit>:<path>` exclusively
- **No git operations** in simdecisions (reading working tree files is fine)
- **No code.** Zero implementation changes.
- **Cap at 45 min.** Scope down rather than overrun. If you can't complete all 15 in 45 min, prioritize the top 8 by file size in _escalated/.
- **Every command must include explicit `cd`** to make working repo obvious

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260410-ESC-001-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — should be ZERO (read-only task)
3. **What Was Done** — bullet list of concrete forensic findings
4. **Test Results** — N/A (no tests for research task)
5. **Build Verification** — N/A (no build for research task)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended Phase 2 approach

DO NOT skip any section.
