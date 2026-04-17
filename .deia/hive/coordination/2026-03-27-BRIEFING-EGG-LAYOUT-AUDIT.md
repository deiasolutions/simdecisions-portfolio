# BRIEFING: Audit EGG Files — Do They Reference the New Chrome Primitives?

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-27 evening
**Priority:** P0

## Context

Chrome ADR Waves A-F built new pane primitives: menu-bar, top-bar, status-bar, toolbar, command-palette, bottom-nav, tab-bar. These files exist on disk in `browser/src/primitives/`.

SPEC-CHROME-F5 ("retrofit all 21 existing .egg.md files to the new layout-composition format") was supposed to rewrite every EGG file so their layout trees reference the new chrome primitives. Commit `1b61962` claims this was done.

But the app looks identical to before. The new primitives aren't rendering. The hypothesis is: the EGG files on disk right now do NOT actually reference the new primitives in their layout blocks.

Additionally, the EGGs were supposed to be renamed to SETs (`.set.md` files) and the language renamed to PRISM-IR as part of this work. No `.set.md` files have been found.

## Your Mission

**Read every EGG file. Report what you find. Do not modify anything.**

### 1. Read every EGG file

All EGG files live in `eggs/`. Read every `.egg.md` file in that directory. For each one, report:
- Filename
- What appTypes appear in its layout block (e.g. "terminal", "text-pane", "sim", "menu-bar", "top-bar", "status-bar", etc.)
- Whether it references ANY of the new chrome primitives: `menu-bar`, `top-bar`, `status-bar`, `toolbar`, `command-palette`, `bottom-nav`, `tab-bar`
- Whether it has the new `ui` block format from the Chrome ADR

### 2. Check canvas2.egg.md specifically

This is the one Q88N is looking at. Read it in full and report:
- Does it have menu-bar, top-bar, status-bar in its layout tree?
- What appTypes does it actually reference?
- Compare what's in the file vs what the ADR-SC-CHROME-001-v3 spec says it should have

### 3. Check what CHROME-F5 actually changed

Read the CHROME-F5 response file: `.deia/hive/responses/20260326-QUEUE-TEMP-SPEC-CHROME-F5-retrofit-eggs-RESPONSE.md`

Also check `git show 1b61962 --stat` to see what files that commit actually modified. Then `git show 1b61962 -- eggs/` to see if any egg files were changed in that commit.

### 4. Check APP_REGISTRY

Read `browser/src/apps/index.ts` (or wherever APP_REGISTRY is defined). Report which appTypes are registered. Are `menu-bar`, `top-bar`, `status-bar`, `toolbar`, `command-palette`, `bottom-nav` registered?

### 5. Search for .set.md files

Search the entire repo for any `.set.md` files or references to the SET rename.

## Deliverable

Write to: `.deia/hive/responses/20260327-EGG-LAYOUT-AUDIT.md`

Structure:
1. **EGG inventory** — table of every egg file, what chrome appTypes it references (if any)
2. **canvas2.egg.md deep dive** — full layout analysis
3. **CHROME-F5 commit analysis** — what it actually changed vs what it claimed
4. **APP_REGISTRY status** — which chrome primitives are registered
5. **SET rename status** — any evidence found
6. **Gap analysis** — what's missing for the new chrome to render

## Rules

- READ ONLY. Do not modify any files.
- Be precise. Copy exact appType strings from the EGG files.
- Include file paths and line numbers.
