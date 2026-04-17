# BRIEFING: ESC-002 Scope Update — Lock Down to 8 Concrete Restores

**Date:** 2026-04-10 (post-ESC-001 survey)
**Author:** Q33NR
**Target:** Q33N (simdecisions)
**Status:** READY FOR DISPATCH
**Model Assignment:** Sonnet (one-shot task file edit)
**Priority:** P0 — unblocks ESC-002 dispatch
**Parent:** `2026-04-10-BRIEFING-ESCALATION-CLEANUP.md` (this repo)

---

## Objective

Update the existing task file `.deia/hive/tasks/2026-04-10-TASK-ESC-002-ESCALATION-RESTORE.md` so that it has a fully concrete scope of **exactly 8 specs to restore**, with explicit shiftcenter commit + path pairs for every one. All ambiguity about which specs ESC-002 should touch must be removed before a bee is dispatched.

---

## Context

### ESC-001 Results

TASK-ESC-001 (escalation chain survey) completed on 2026-04-10. Response file: `.deia/hive/responses/20260410-ESC-001-RESPONSE.md`. The survey bee found disposition for all 15 spec families, including 2 specs that needed further git archaeology (RESTORE_WITH_SEARCH).

### Post-Survey Archaeology (Q33NR Direct)

Q33NR ran manual `git log` + `git show` against shiftcenter to resolve the 2 RESTORE_WITH_SEARCH specs:

- **WIKI-V1.1-LLM-WIKI-PATTERN**: First commit `8064d76` shows the spec already had 1 `## Clean Retry` block prepended AND was rejected at Gate 0 for missing Priority and acceptance criteria. Structurally broken from birth. **Killed** by Q88N.
- **GITHUB-005-federalist-papers-upload**: First commit `6887941` shows only a `.rejection.md` file — no clean SPEC file ever existed in git history. The rejection cites path/scope contradictions. Phantom spec. **Killed** by Q88N.

### Q88N Final Disposition

Q88N approved on 2026-04-10: **kill all ambiguous specs, restore only the confirmed clean ones.**

**RESTORE (7 specs):**
| Spec | Source |
|------|--------|
| SPEC-GAMIFICATION-V1 | shiftcenter@dd2eedf:.deia/hive/queue/_stage/SPEC-GAMIFICATION-V1.md |
| SPEC-EVENT-LEDGER-GAMIFICATION | shiftcenter@dd2eedf:.deia/hive/queue/_stage/SPEC-EVENT-LEDGER-GAMIFICATION.md |
| SPEC-ML-TRAINING-V1 | shiftcenter@dd2eedf:.deia/hive/queue/_stage/SPEC-ML-TRAINING-V1.md |
| SPEC-WIKI-SYSTEM | shiftcenter@dd2eedf:.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md |
| SPEC-WIKI-V1 | shiftcenter@dd2eedf:.deia/hive/queue/_stage/SPEC-WIKI-V1.md |
| SPEC-WIKI-103-crud-api-routes | shiftcenter@173b998:.deia/hive/queue/backlog/SPEC-WIKI-103-crud-api-routes.md |
| SPEC-WIKI-108-egg-integration | shiftcenter@173b998:.deia/hive/queue/backlog/SPEC-WIKI-108-egg-integration.md |

**RESTORE_WITH_STRIP (1 spec):**
| Spec | Source | Strip |
|------|--------|-------|
| SPEC-RAIDEN-000-master-coordination | shiftcenter@19ef5cb:.deia/hive/queue/backlog/SPEC-RAIDEN-000-master-coordination.md | Remove 1 prepended `## Clean Retry` block (6 lines) |

**KILL (7 specs — no action from ESC-002 bee; will be cleaned up in ESC-003):**
- SPEC-WIKI-SURVEY-000 (phantom spec, no clean original ever existed)
- SPEC-GITHUB-005-federalist-papers-upload (phantom spec, only rejection files)
- SPEC-WIKI-V1.1-LLM-WIKI-PATTERN (structurally broken from birth — Gate 0 fail for missing Priority + AC)
- SPEC-TRIAGE-ESCALATED-001 (superseded by ESC-001/002 cleanup work itself)
- SPEC-FLAPPY-100-self-learning-v2 (marked `(NEEDS_DAVE)` from birth — unviable)
- SPEC-BL-146-BOT-ACTIVITY-PORT (no clean original, escalated immediately)
- SPEC-MW-VERIFY-001-full-audit (no clean original, escalated from first observation)

---

## Scope — Q33N's Task

Edit `.deia/hive/tasks/2026-04-10-TASK-ESC-002-ESCALATION-RESTORE.md` in place to:

1. **Add a new section at the top**, right after `## Context`, titled `## Final Scope (Q88N approved 2026-04-10)` containing:
   - The 7 RESTORE specs with explicit shiftcenter commit + path + target path pairs (use the table above)
   - The 1 RESTORE_WITH_STRIP spec with source commit + path + strip instructions
   - The 7 KILL specs with a clear statement: "These specs require NO action from the ESC-002 bee. They remain in simdecisions `_escalated/` until ESC-003 cleanup."

2. **Remove any language** that suggests the bee should "read the disposition table from ESC-001's response file." Replace with: "The concrete scope is below — read ESC-001 response for context only."

3. **Update the Work Process section** to iterate over exactly the 8 specs by name, with the concrete git show commands baked in. Example:
   ```bash
   cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
   git show dd2eedf:.deia/hive/queue/_stage/SPEC-GAMIFICATION-V1.md > /tmp/clean-GAMIFICATION-V1.md
   cp /tmp/clean-GAMIFICATION-V1.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/SPEC-GAMIFICATION-V1.md
   ```

4. **Add a verification checklist** at the end of the task:
   - [ ] All 8 target files exist in `simdecisions/.deia/hive/queue/_needs_review/`
   - [ ] All 8 target files have NO prepended `## Clean Retry` block
   - [ ] RAIDEN-000 specifically has been stripped
   - [ ] No files touched in `simdecisions/.deia/hive/queue/_escalated/`
   - [ ] No git operations executed in either repo

5. **Keep the time cap at 30 minutes, model at Haiku (unchanged).**

### Out of Scope (Q33N, do NOT do these things)

- Do NOT dispatch the bee yourself (Q33NR will handle dispatch after review)
- Do NOT write any new task files (only edit the existing ESC-002)
- Do NOT modify ESC-001 or the survey response file
- Do NOT touch any files in shiftcenter
- Do NOT modify eggs, primitives, or code — this is a task file edit only

---

## Files to Read First

- `.deia/hive/tasks/2026-04-10-TASK-ESC-002-ESCALATION-RESTORE.md` (the file you will edit)
- `.deia/hive/responses/20260410-ESC-001-RESPONSE.md` (survey results for context)
- `.deia/hive/coordination/2026-04-10-BRIEFING-ESCALATION-CLEANUP.md` (parent briefing)

---

## Constraints

- Q33N does NOT code.
- Q33N edits ONE file: `2026-04-10-TASK-ESC-002-ESCALATION-RESTORE.md`.
- No file over 500 lines (ESC-002 will grow but should stay well under).
- No git write operations.
- No stubs, no TODO markers, no placeholder returns.
- Write a response file with all 8 required sections.

---

## Success Criteria

- [ ] ESC-002 task file has `## Final Scope` section with all 7 RESTORE + 1 RESTORE_WITH_STRIP entries, each with commit + path
- [ ] ESC-002 task file explicitly lists the 7 KILL'd specs as "no action required"
- [ ] ESC-002 Work Process section has concrete `git show` + `cp` commands for all 8 specs
- [ ] ESC-002 verification checklist includes the 5 items listed above
- [ ] Response file written with 8 sections per BOOT.md
- [ ] No files modified besides ESC-002 task file and the response file

---

## Q33N Workflow

1. Read this briefing
2. Read ESC-001 response (for context)
3. Read ESC-002 task file (the edit target)
4. Edit ESC-002 in place per Scope section above
5. Write response file: `.deia/hive/responses/20260410-ESC-002-SCOPE-UPDATE-RESPONSE.md`
6. Return to Q33NR for review

---

## Report To

Q33N → Q33NR (after edit complete, for review before bee dispatch)

---

*2026-04-10-BRIEFING-ESC-002-SCOPE-UPDATE — Q33NR → Q33N — simdecisions canonical*
