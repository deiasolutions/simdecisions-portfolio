# BRIEFING: Escalation Chain Cleanup — Rescue Legitimate Specs (Cross-Repo)

**Date:** 2026-04-10
**Author:** Q33NR
**Target:** Q33N (simdecisions)
**Status:** READY FOR DISPATCH
**Model Assignment:** Sonnet (Phase 1 survey), Haiku or Sonnet (Phase 2 restore)
**Priority:** P1 — unblocks legitimate backlog work in the new monorepo

**Governance context:** Per `2026-04-10-DECISION-SIMDECISIONS-CANONICAL` (recorded in shiftcenter `.deia/hive/coordination/`), simdecisions is now the canonical repo and shiftcenter is frozen-legacy. This briefing targets simdecisions.

---

## Objective

Rescue the legitimate specs listed below from the escalation chain pollution that was **inherited from shiftcenter during `3228763 v0.1.0-cutover`**, and restore their canonical originals to the simdecisions `.deia/hive/queue/_needs_review/` directory so the backlog is workable again.

**Do NOT fix the triage daemon in this task.** That is a separate future briefing.

---

## Context — Why This Is Needed

The triage daemon in the old shiftcenter repo entered a recursive escalation loop on 2026-04-09/10:

1. Bee infra produced empty output for several specs.
2. Daemon detected empty output and **prepended** `## Clean Retry` blocks to the spec file itself, then requeued.
3. Retry produced empty output. Daemon prepended ANOTHER `## Clean Retry` block.
4. After 3 retries, daemon escalated to `_escalated/` and created `SPEC-X.rejection.md`.
5. The rejection file itself got re-escalated, creating `SPEC-X.rejection.rejection.md`, etc.
6. Deepest chain observed: 10+ levels (`SPEC-ML-TRAINING-V1.rejection.rejection.rejection.rejection.rejection.rejection.rejection.rejection.rejection.rejection.md`).

**Those polluted files were imported wholesale into simdecisions as part of `3228763 v0.1.0-cutover`.** They are now in simdecisions' `.deia/hive/queue/_escalated/` and `.deia/hive/queue/backlog/` directories.

The original specs are still good — they got caught in infrastructure failure in the old repo. Q88N wants them back in circulation in simdecisions.

**Clean originals live in the shiftcenter git history on branch `wip/factory-refactor-20260411` (commit `dd2eedf` or earlier).** Simdecisions does NOT have shiftcenter's git history (cutover was a fresh import, not a subtree). So Phase 1 survey must read from shiftcenter and Phase 2 restore must copy into simdecisions.

---

## Repo Geometry

- **simdecisions (this repo, target for writes):** `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions`
- **shiftcenter (read-only source of truth for git history):** `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter`
- **shiftcenter forensic branch:** `wip/factory-refactor-20260411` (commit `dd2eedf`)
- **shiftcenter main:** `main` (clean, parent of wip branch)

Operations MUST be scoped by `cd` to the correct repo. Be explicit in every command.

---

## Scope Split Into Phases

### Phase 1 — Survey (Read-Only, Sonnet)

**Bee type:** Sonnet
**Time budget:** 45 minutes
**Branch state:** Read from BOTH repos. Zero writes to either.

**Deliverable:** A single research report at
`.deia/hive/responses/20260410-ESCALATION-SURVEY-RESPONSE.md` (in simdecisions)

**Work:**

1. For each spec family below, inspect its current state in simdecisions:

   | Spec Family | Simdecisions Path Candidate |
   |-------------|-----------------------------|
   | GAMIFICATION-V1 | `.deia/hive/queue/_escalated/SPEC-GAMIFICATION-V1.md` |
   | EVENT-LEDGER-GAMIFICATION | `.deia/hive/queue/_escalated/SPEC-EVENT-LEDGER-GAMIFICATION.md` |
   | ML-TRAINING-V1 | `.deia/hive/queue/_escalated/SPEC-ML-TRAINING-V1.md` |
   | FLAPPY-100 | `.deia/hive/queue/_escalated/SPEC-FLAPPY-100-self-learning-v2.md` |
   | BL-146 | `.deia/hive/queue/_escalated/SPEC-BL-146-BOT-ACTIVITY-PORT.md` |
   | WIKI-SYSTEM | `.deia/hive/queue/_escalated/SPEC-WIKI-SYSTEM.md` (if present) |
   | WIKI-V1 | `.deia/hive/queue/_escalated/SPEC-WIKI-V1.md` (if present) |
   | WIKI-V1.1-LLM-WIKI-PATTERN | `.deia/hive/queue/_escalated/SPEC-WIKI-V1.1-LLM-WIKI-PATTERN.md` (if present) |
   | WIKI-103 | `.deia/hive/queue/_escalated/SPEC-WIKI-103-crud-api-routes.md` |
   | WIKI-108 | `.deia/hive/queue/_escalated/SPEC-WIKI-108-egg-integration.md` |
   | WIKI-SURVEY-000 | search `.deia/hive/queue/` for `*WIKI-SURVEY*` |
   | MW-VERIFY-001 | `.deia/hive/queue/_escalated/SPEC-MW-VERIFY-001-full-audit.md` |
   | RAIDEN-000 | `.deia/hive/queue/_escalated/SPEC-RAIDEN-000-master-coordination.md` |
   | GITHUB-005 | search for `*GITHUB-005*` |
   | TRIAGE-ESCALATED-001 | `.deia/hive/queue/_escalated/SPEC-TRIAGE-ESCALATED-001.md` |

2. For each spec family, determine:
   - **Canonical content start:** How many prepended `## Clean Retry` blocks precede the real spec? Identify the byte/line offset where the real spec starts.
   - **Is there a cleaner version in shiftcenter git history?** Use:
     ```
     cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
     git log --follow --all --oneline -- '.deia/hive/queue/**/*<name>*'
     git show <earliest-clean-commit>:.deia/hive/queue/<path>
     ```
     The earliest commit BEFORE the daemon loop started is the target.
   - **Is there a newer version in simdecisions `backlog/`?** Check `.deia/hive/queue/backlog/` and `.deia/hive/queue/_needs_review/`.
   - **Is the spec already built?** Check simdecisions `_done/`, `docs/specs/`, and current code for implementation.

3. Produce a disposition table with one row per spec family:

   ```
   | Spec Family | Canonical Source | Status | Disposition | Evidence |
   |-------------|------------------|--------|-------------|----------|
   | GAMIFICATION-V1 | shiftcenter@<commit>:.deia/hive/queue/_needs_review/SPEC-GAMIFICATION-V1.md | CLEAN_ORIG_FOUND | RESTORE | ... |
   ```

   **Disposition options:**
   - `RESTORE` — canonical is clean, restore to simdecisions `_needs_review/`
   - `RESTORE_WITH_STRIP` — strip prepended Clean Retry blocks, then restore
   - `SKIP_SUPERSEDED` — newer version exists in simdecisions, no action
   - `SKIP_BUILT` — already implemented in simdecisions
   - `HOLD_Q88N` — no clean original exists and content is ambiguous; Q88N must decide
   - `KILL` — spec is obsolete or broken beyond rescue

4. For `SKIP_*` and `KILL` dispositions, cite the superseding file or implementation path.

5. **Constraints:**
   - **Read-only.** Zero writes to either repo.
   - **No git checkout** in shiftcenter (it is frozen-legacy). Use `git show wip/factory-refactor-20260411:<path>` and `git show <commit>:<path>` exclusively.
   - **No git operations whatsoever** in simdecisions during Phase 1 (reading working tree files is fine).
   - **No code.** Zero implementation changes.
   - **Cap at 45 min.** Scope down rather than overrun.
   - Every command must include an explicit `cd` to make the working repo obvious.

6. Response file must contain all 8 required sections per BOOT.md.

---

### Phase 2 — Restore (File Ops Only, Haiku or Sonnet)

**Bee type:** Haiku (sufficient for file ops) unless Phase 1 reveals complexity
**Time budget:** 30 minutes
**Branch state:** Write to simdecisions working tree. No git commits.

**Work:**

1. For each `RESTORE` disposition:
   ```
   cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
   git show <commit>:<path> > /tmp/clean-<spec>.md
   cp /tmp/clean-<spec>.md C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/.deia/hive/queue/_needs_review/<spec>.md
   ```

2. For each `RESTORE_WITH_STRIP` disposition:
   - Read the polluted file
   - Strip any prepended `## Clean Retry` blocks, `## Triage History` sections, and automated escalation headers (delimited by `---` separators)
   - Write the cleaned content to simdecisions `.deia/hive/queue/_needs_review/<spec>.md`

3. For `HOLD_Q88N`: do nothing, list in the Phase 2 response for Q88N follow-up.

4. For `KILL` and `SKIP_*`: do nothing. Note in response.

5. **Do NOT commit.** **Do NOT push.** Leave restored files as uncommitted working-tree changes in simdecisions. Q88N will review before any commit.

6. **Do NOT touch the `_escalated/` directory in simdecisions.** Leave the polluted originals in place as forensic evidence until Q88N signs off on the restores. Phase 3 (separate briefing) will decide whether to delete them.

7. Response file must contain all 8 required sections.

---

### Phase 3 (Future, Out of Scope Here)

- Daemon fix in simdecisions (prevent recursive escalation loop from recurring)
- Forensic cleanup of `_escalated/` polluted originals (after Q88N approves restores)
- Possible archival of shiftcenter wip branch tarball for long-term cold storage

These will be separate briefings after Phase 2 completes and Q88N confirms the restored specs are acceptable.

---

## Files to Read First

**In simdecisions (working tree):**
- `.deia/hive/queue/_escalated/` (entire directory)
- `.deia/hive/queue/backlog/` (see what's still actively queued, what has `.rejection.*.md` chains)
- `.deia/hive/queue/_needs_review/` (existing rejection records)
- `.deia/hive/queue/_done/_archive_old_factory/` (already-built specs)

**In shiftcenter (read-only, via git only):**
- `wip/factory-refactor-20260411` at commit `dd2eedf`: use `git show` for all reads
- `main` branch: for any comparison if needed
- `git log --follow --all --oneline -- <path>` for history traversal

---

## Constraints

- Q33N does NOT code.
- No file over 500 lines.
- No git write operations in either repo without Q88N approval.
- No daemon restart.
- No touching shiftcenter working tree at all (read-only via git show).
- Response file required per BOOT.md 8-section template.
- `cd` to the correct repo in every shell command. Never assume pwd.

---

## Model Assignment

- **Phase 1:** Sonnet (requires judgment on canonical vs corrupted, cross-repo navigation)
- **Phase 2:** Haiku (pure file operations; upgrade to Sonnet if Phase 1 flags complexity)

---

## Success Criteria

- [ ] Phase 1 report exists in simdecisions `.deia/hive/responses/` with disposition table covering all 15 spec families
- [ ] Q33NR reviews Phase 1 report and approves Phase 2 dispositions
- [ ] Phase 2 restores clean originals to simdecisions `_needs_review/` working tree (uncommitted)
- [ ] Q88N reviews restored specs before any commit
- [ ] shiftcenter `wip/factory-refactor-20260411` remains untouched as forensic archive
- [ ] simdecisions `_escalated/` directory remains untouched until Phase 3

---

## Report To

Q33N → Q33NR after Phase 1 complete (for disposition review).
Q33N → Q33NR after Phase 2 complete (for final sign-off).
Q33NR → Q88N (final report with restored spec list).

---

*2026-04-10-BRIEFING-ESCALATION-CLEANUP — Q33NR → Q33N — simdecisions canonical*
