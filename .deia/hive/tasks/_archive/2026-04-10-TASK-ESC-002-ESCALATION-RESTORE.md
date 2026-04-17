# TASK-ESC-002: Escalation Restore — Clean Specs to _needs_review

## Objective
Restore clean spec originals from shiftcenter git history to simdecisions `_needs_review/` working tree based on Phase 1 disposition table.

## Context

**Prerequisite:** TASK-ESC-001 (Phase 1 survey) completed 2026-04-10. ESC-001 identified canonical sources for 15 spec families. Q88N manual git archaeology resolved the 2 RESTORE_WITH_SEARCH specs (both KILL'd).

This task executes restore operations for the 8 specs with confirmed clean sources: 7 RESTORE + 1 RESTORE_WITH_STRIP.

## Final Scope (Q88N approved 2026-04-10)

**The concrete scope is below. Read `.deia/hive/responses/20260410-ESC-001-RESPONSE.md` for context only.**

### RESTORE (7 specs)

Clean originals exist in shiftcenter git history. Direct restore with `git show`:

| Spec | Source Commit | Source Path | Target Path |
|------|---------------|-------------|-------------|
| SPEC-GAMIFICATION-V1 | dd2eedf | .deia/hive/queue/_stage/SPEC-GAMIFICATION-V1.md | .deia/hive/queue/_needs_review/SPEC-GAMIFICATION-V1.md |
| SPEC-EVENT-LEDGER-GAMIFICATION | dd2eedf | .deia/hive/queue/_stage/SPEC-EVENT-LEDGER-GAMIFICATION.md | .deia/hive/queue/_needs_review/SPEC-EVENT-LEDGER-GAMIFICATION.md |
| SPEC-ML-TRAINING-V1 | dd2eedf | .deia/hive/queue/_stage/SPEC-ML-TRAINING-V1.md | .deia/hive/queue/_needs_review/SPEC-ML-TRAINING-V1.md |
| SPEC-WIKI-SYSTEM | dd2eedf | .deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md | .deia/hive/queue/_needs_review/SPEC-WIKI-SYSTEM.md |
| SPEC-WIKI-V1 | dd2eedf | .deia/hive/queue/_stage/SPEC-WIKI-V1.md | .deia/hive/queue/_needs_review/SPEC-WIKI-V1.md |
| SPEC-WIKI-103-crud-api-routes | 173b998 | .deia/hive/queue/backlog/SPEC-WIKI-103-crud-api-routes.md | .deia/hive/queue/_needs_review/SPEC-WIKI-103-crud-api-routes.md |
| SPEC-WIKI-108-egg-integration | 173b998 | .deia/hive/queue/backlog/SPEC-WIKI-108-egg-integration.md | .deia/hive/queue/_needs_review/SPEC-WIKI-108-egg-integration.md |

### RESTORE_WITH_STRIP (1 spec)

Clean version exists with 1 prepended `## Clean Retry` block (6 lines). Strip before restore:

| Spec | Source Commit | Source Path | Strip Instructions | Target Path |
|------|---------------|-------------|-------------------|-------------|
| SPEC-RAIDEN-000-master-coordination | 19ef5cb | .deia/hive/queue/backlog/SPEC-RAIDEN-000-master-coordination.md | Remove first 6 lines (1x "## Clean Retry" block + separator) | .deia/hive/queue/_needs_review/SPEC-RAIDEN-000-master-coordination.md |

### KILL (7 specs — NO ACTION REQUIRED FROM ESC-002 BEE)

These specs require **no action** from the ESC-002 bee. They remain in simdecisions `_escalated/` until ESC-003 cleanup:

1. **SPEC-WIKI-SURVEY-000** — phantom spec, no clean original ever existed (only rejection chains)
2. **SPEC-GITHUB-005-federalist-papers-upload** — phantom spec, only `.rejection.md` file ever existed in git history (commit 6887941 shows path/scope contradictions at birth)
3. **SPEC-WIKI-V1.1-LLM-WIKI-PATTERN** — structurally broken from birth (commit 8064d76 shows Gate 0 fail for missing Priority + acceptance criteria, already had 1 prepended "Clean Retry" block in first commit)
4. **SPEC-TRIAGE-ESCALATED-001** — superseded by ESC-001/002 cleanup work itself (meta-irony: triage spec got escalated)
5. **SPEC-FLAPPY-100-self-learning-v2** — marked `(NEEDS_DAVE)` from birth (commit 99428a6), unviable spec
6. **SPEC-BL-146-BOT-ACTIVITY-PORT** — no clean original found (first commit bc17fb9 shows spec already in `_escalated/`)
7. **SPEC-MW-VERIFY-001-full-audit** — no clean original found (earliest commits 19ef5cb, dd2eedf show already escalated)

**Q88N decision (2026-04-10):** Kill all ambiguous specs. ESC-003 will handle cleanup.

**Repo Geometry:**
- **simdecisions (target for writes):** `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions`
- **shiftcenter (read-only source):** `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter`

## Files to Read First

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260410-ESC-001-RESPONSE.md` — Phase 1 survey results (for context; disposition table in this task file supersedes it after Q88N archaeology)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/coordination/2026-04-10-BRIEFING-ESC-002-SCOPE-UPDATE.md` — Q33NR briefing explaining the Q88N manual archaeology that resolved the 2 RESTORE_WITH_SEARCH specs

## Deliverables

- [ ] All `RESTORE` dispositions: clean originals copied from shiftcenter to simdecisions `_needs_review/`
- [ ] All `RESTORE_WITH_STRIP` dispositions: cleaned content written to simdecisions `_needs_review/`
- [ ] Response file: `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260410-ESC-002-RESPONSE.md`
- [ ] Working tree changes left uncommitted for Q88N review

## Work Process

### Step 1: Restore 7 RESTORE Specs

Execute the following commands in sequence to restore clean originals from shiftcenter to simdecisions `_needs_review/`:

```bash
# SPEC-GAMIFICATION-V1
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show dd2eedf:.deia/hive/queue/_stage/SPEC-GAMIFICATION-V1.md > /tmp/clean-GAMIFICATION-V1.md
cp /tmp/clean-GAMIFICATION-V1.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-GAMIFICATION-V1.md

# SPEC-EVENT-LEDGER-GAMIFICATION
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show dd2eedf:.deia/hive/queue/_stage/SPEC-EVENT-LEDGER-GAMIFICATION.md > /tmp/clean-EVENT-LEDGER-GAMIFICATION.md
cp /tmp/clean-EVENT-LEDGER-GAMIFICATION.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-EVENT-LEDGER-GAMIFICATION.md

# SPEC-ML-TRAINING-V1
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show dd2eedf:.deia/hive/queue/_stage/SPEC-ML-TRAINING-V1.md > /tmp/clean-ML-TRAINING-V1.md
cp /tmp/clean-ML-TRAINING-V1.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-ML-TRAINING-V1.md

# SPEC-WIKI-SYSTEM
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show dd2eedf:.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md > /tmp/clean-WIKI-SYSTEM.md
cp /tmp/clean-WIKI-SYSTEM.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-WIKI-SYSTEM.md

# SPEC-WIKI-V1
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show dd2eedf:.deia/hive/queue/_stage/SPEC-WIKI-V1.md > /tmp/clean-WIKI-V1.md
cp /tmp/clean-WIKI-V1.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-WIKI-V1.md

# SPEC-WIKI-103-crud-api-routes
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show 173b998:.deia/hive/queue/backlog/SPEC-WIKI-103-crud-api-routes.md > /tmp/clean-WIKI-103.md
cp /tmp/clean-WIKI-103.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-WIKI-103-crud-api-routes.md

# SPEC-WIKI-108-egg-integration
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show 173b998:.deia/hive/queue/backlog/SPEC-WIKI-108-egg-integration.md > /tmp/clean-WIKI-108.md
cp /tmp/clean-WIKI-108.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-WIKI-108-egg-integration.md
```

### Step 2: Restore 1 RESTORE_WITH_STRIP Spec

SPEC-RAIDEN-000 has 1 prepended `## Clean Retry` block (6 lines). Strip the first 6 lines after extracting from git:

```bash
# SPEC-RAIDEN-000-master-coordination
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
git show 19ef5cb:.deia/hive/queue/backlog/SPEC-RAIDEN-000-master-coordination.md > /tmp/polluted-RAIDEN-000.md

# Strip first 6 lines (## Clean Retry block)
tail -n +7 /tmp/polluted-RAIDEN-000.md > /tmp/clean-RAIDEN-000.md

cp /tmp/clean-RAIDEN-000.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-RAIDEN-000-master-coordination.md
```

### Step 3: Verify All 8 Files Restored

Run verification commands (see Verification Checklist below).

### For KILL Dispositions (7 specs)

**No action required.** The 7 KILL'd specs remain in simdecisions `_escalated/` until ESC-003 cleanup. List them in the response file under "Issues / Follow-ups".

## Test Requirements

Run these verification commands and include output in response file:

```bash
# Count files in _needs_review/ before restore
cd C:/Users/davee/OneDrive/Documents/GitHub/simdecisions
ls -1 .deia/hive/queue/_needs_review/ | wc -l

# After restore, count again (should increase by 8)
ls -1 .deia/hive/queue/_needs_review/ | wc -l

# Verify all 8 target files exist
ls -lh .deia/hive/queue/_needs_review/SPEC-GAMIFICATION-V1.md
ls -lh .deia/hive/queue/_needs_review/SPEC-EVENT-LEDGER-GAMIFICATION.md
ls -lh .deia/hive/queue/_needs_review/SPEC-ML-TRAINING-V1.md
ls -lh .deia/hive/queue/_needs_review/SPEC-WIKI-SYSTEM.md
ls -lh .deia/hive/queue/_needs_review/SPEC-WIKI-V1.md
ls -lh .deia/hive/queue/_needs_review/SPEC-WIKI-103-crud-api-routes.md
ls -lh .deia/hive/queue/_needs_review/SPEC-WIKI-108-egg-integration.md
ls -lh .deia/hive/queue/_needs_review/SPEC-RAIDEN-000-master-coordination.md

# Verify RAIDEN-000 has NO "## Clean Retry" pollution
head -n 20 .deia/hive/queue/_needs_review/SPEC-RAIDEN-000-master-coordination.md | grep "Clean Retry"
# (should return empty — no match)

# Verify _escalated/ untouched (forensic preservation)
git status .deia/hive/queue/_escalated/
# (should show no changes)

# Verify no git operations executed
git status
# (should show only _needs_review/ files as untracked or modified)
```

### Verification Checklist (mark in response file)

- [ ] All 8 target files exist in `simdecisions/.deia/hive/queue/_needs_review/`
- [ ] All 8 target files have NO prepended `## Clean Retry` block (verify with `head` + `grep`)
- [ ] RAIDEN-000 specifically has been stripped (first 6 lines removed)
- [ ] No files touched in `simdecisions/.deia/hive/queue/_escalated/`
- [ ] No git operations executed in either repo (working tree changes only in simdecisions)

## Acceptance Criteria

- [ ] All 7 RESTORE specs copied from shiftcenter to simdecisions `_needs_review/`
  - SPEC-GAMIFICATION-V1 (from dd2eedf)
  - SPEC-EVENT-LEDGER-GAMIFICATION (from dd2eedf)
  - SPEC-ML-TRAINING-V1 (from dd2eedf)
  - SPEC-WIKI-SYSTEM (from dd2eedf)
  - SPEC-WIKI-V1 (from dd2eedf)
  - SPEC-WIKI-103-crud-api-routes (from 173b998)
  - SPEC-WIKI-108-egg-integration (from 173b998)
- [ ] 1 RESTORE_WITH_STRIP spec completed with pollution removed
  - SPEC-RAIDEN-000-master-coordination (stripped first 6 lines from 19ef5cb source)
- [ ] All 8 restored files verified to have NO `## Clean Retry` blocks
- [ ] 7 KILL'd specs noted in response with justification (no action taken on them)
- [ ] Working tree changes left uncommitted (no `git commit`, no `git push`)
- [ ] `_escalated/` directory untouched (forensic preservation for ESC-003)
- [ ] Response file contains all 8 required sections

## Constraints

- **Write ONLY to simdecisions `_needs_review/`.** No writes to `_escalated/`, `backlog/`, or any other queue directory.
- **Do NOT commit.** **Do NOT push.** Leave restored files as uncommitted working-tree changes.
- **Do NOT touch `_escalated/` directory** in simdecisions — leave polluted originals as forensic evidence.
- **No git operations in shiftcenter** — read-only via `git show` only.
- **Every command must include explicit `cd`** to make working repo obvious.
- **No file over 500 lines** (verify restored specs)
- **Cap at 30 min.** If restore operations take longer, prioritize top dispositions by size/importance.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/responses/20260410-ESC-002-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created in `_needs_review/`, full paths
3. **What Was Done** — bullet list per disposition: RESTORE from commit X, RESTORE_WITH_STRIP from _escalated/Y
4. **Test Results** — File count verification: `ls -1 _needs_review/ | wc -l` before/after
5. **Build Verification** — N/A (no build for file ops)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — Any HOLD_Q88N items, any restore failures, recommended Phase 3 approach

DO NOT skip any section.
