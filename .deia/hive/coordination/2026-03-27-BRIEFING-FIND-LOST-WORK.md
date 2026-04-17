# BRIEFING: Find the Lost Chrome ADR Work

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-27 evening
**Priority:** P0 — We may have lost days of work

## Situation

Over the last 24-48 hours, we dispatched Chrome ADR Waves A-F — approximately 36 bee specs that implemented a massive rewrite of the ShiftCenter shell:

- Shell chrome (menu bar, top bar, status bar, toolbar, command palette, tab bar, bottom nav) refactored into pane primitives
- EGG format renamed to SET (`.set.md`)
- Language renamed to PRISM-IR
- All existing eggs retrofitted to the new standard (SPEC-CHROME-F5)
- Legacy chrome deleted (SPEC-CHROME-F1)
- Mobile responsive modes (immersive, compact)
- Design mode, autosave, close recovery prompts
- SDK docs updated to v0.3.0

Bees reported COMPLETE on all specs. Commits exist in git history. But the running app shows ZERO changes — screenshots from 7:35 AM and 7:31 PM today are identical. The old UI is still rendering.

We know the auto-commit bug (`auto_commit.py`) was eating source files — committing response files but not the actual code bees wrote. The question is: **where is the actual code?**

## Your Mission

**Find every trace of the lost work. Do not fix anything. Report what you find.**

### 1. Search git for the actual code changes

For every Chrome ADR commit in the last 48 hours, run `git show --stat <hash>` to see what files were actually in each commit. List which commits have REAL source code changes vs which only have response files / metadata.

Relevant commits (from `git log --since="2026-03-26T00:00" --oneline --all`):
- All commits with `[BEE-SONNET]` or `[BEE-HAIKU]` prefixes
- The merge commits
- The stash entries

### 2. Search git stash

Run `git stash list`. The build-fix briefing from this morning mentions files were "restored from git stash". There may be MORE stashed work that wasn't restored. Check every stash entry.

### 3. Search the working tree for uncommitted files

Run `git status` to see if there are uncommitted files from bee work that never got staged. Also check for files that exist on disk but aren't tracked.

### 4. Search for branch remnants

Check all branches: `git branch -a`. The bees may have written code on branches that were never merged.

### 5. Search bee raw output logs

The dispatch script saves raw Claude output to `.deia/hive/responses/*-RAW.txt`. These contain the FULL transcript of what each bee did — including every file it wrote. Even if the auto-commit lost the files, the raw logs show what WAS written.

For the last 24 hours, read every RAW file and catalog:
- What files the bee claimed to create/modify
- Whether those files exist on disk right now

Focus on these spec groups:
- CHROME-A (A1-A3): error boundaries, pane chrome, seamless verify
- CHROME-B (B1-B7): top-bar, menu-bar, status-bar, tab-bar, bottom-nav, command-palette, bus permissions
- CHROME-C (C1-C4): floating toolbar, docked toolbar, toolbar egg parsing
- CHROME-D (D1-D4): chrome mode, immersive mode, compact mode, mobile gestures
- CHROME-E (E1-E4): design mode, save-as-derived-egg, autosave, close recovery
- CHROME-F (F1-F6): delete legacy chrome, remove flags, retrofit eggs to new format, SDK update

### 6. Check for the SET rename

The EGG-to-SET rename was part of this work. Look for:
- Any `.set.md` files anywhere in the repo
- Any references to "set.md" or "PRISM-IR" in source code
- The SPEC-CHROME-F5 retrofit spec and its bee output

### 7. Check OneDrive / filesystem timestamps

Files on disk may have been written by bees but overwritten by OneDrive sync or git operations. Check filesystem timestamps on key directories:
- `browser/src/primitives/menu-bar/`
- `browser/src/primitives/top-bar/`
- `browser/src/primitives/status-bar/`
- `browser/src/primitives/command-palette/`
- `browser/src/primitives/toolbar/`
- `browser/src/primitives/bottom-nav/`
- `eggs/` (for any .set.md files)

## Deliverable

Write your findings to:
`.deia/hive/responses/20260327-FIND-LOST-WORK-REPORT.md`

Structure:
1. **Commits with real code** — list of commits that contain actual source file changes
2. **Commits with only metadata** — list of commits that only have response files
3. **Stash contents** — what's in each stash entry
4. **Uncommitted files** — anything on disk that isn't in git
5. **Branch inventory** — all branches and what they contain
6. **Raw log evidence** — for each spec, what files the bee wrote (from RAW logs)
7. **Files found vs files missing** — comparison table: what should exist vs what does
8. **SET/PRISM-IR rename status** — any evidence of the rename anywhere
9. **Recovery recommendation** — can the work be recovered? From where?

## Rules

- READ ONLY. Do not modify any files.
- Do not fix anything. Do not write code.
- Be thorough. Check every source listed above.
- Include exact file paths, commit hashes, and line numbers as evidence.
