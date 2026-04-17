# BRIEFING: FamilyBondBot Deep Dive Discovery

**From:** Q33NR (parent)
**To:** Q33NR-REGENT
**Date:** 2026-03-27
**Mission:** Discovery — explore, understand, report back

## Context

FamilyBondBot (FBB) is an existing product that lives as a peer repo alongside ShiftCenter:

  `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\`

ShiftCenter is a pane-based application shell where every product is an EGG configuration of the same platform. We are exploring what it would take to refactor FBB into the ShiftCenter shell framework — making it an EGG-based product like canvas, efemera, chat, etc.

There are also related repos nearby that may be relevant:
- `familybondbot-backup-season-009`
- `family-bond-chat`
- `familyboundbot`

For reference, ShiftCenter lives at:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\`

Key ShiftCenter concepts you'll want to understand for comparison:
- **EGG files** (`eggs/*.egg.md`) — product definitions as markdown with JSON layout blocks
- **Shell** (`browser/src/shell/`) — pane layout engine, reducer, types
- **Primitives** (`browser/src/primitives/`) — reusable pane types (terminal, text-pane, tree-browser, etc.)
- **Adapters** (`browser/src/apps/`) — bridge between shell and primitives
- **Relay bus** (`browser/src/infrastructure/relay_bus/`) — inter-pane messaging

## Your Mission

**Discover. Do not plan. Do not prescribe. Report what you find.**

1. **Explore the FBB repo thoroughly.** Understand:
   - What is FamilyBondBot? What does it do? Who is it for?
   - Stack: languages, frameworks, database, hosting
   - Repo structure: key directories, entry points, config files
   - Feature inventory: what are the major features/screens/flows?
   - Size: rough file count, line count, complexity
   - Current state: is it deployed? active? what season/version?

2. **Map the overlap with ShiftCenter.** Identify:
   - What FBB features already have ShiftCenter primitive equivalents?
   - What FBB features would need NEW primitives?
   - What is FBB-specific business logic vs. generic shell behavior?
   - Shared dependencies, shared patterns, divergences

3. **Assess the related repos.** Quick scan of the other family* repos — what are they? Are they relevant to the migration?

4. **Identify risks and unknowns.** What would be hard? What might break? What needs Q88N's input?

## Deliverable

Write your findings to:
  `.deia/hive/coordination/2026-03-27-REPORT-FBB-DISCOVERY.md`

Structure it however makes sense for what you find. Be thorough but concise. Include file paths and specific examples. This report will be used to plan the actual migration.

## Rules

- READ ONLY. Do not modify any files in either repo.
- Do not write code. Do not create specs. Do not plan implementation.
- You are a regent Q33NR — you report to the parent Q33NR, not directly to Q88N.
- Take your time. Thoroughness matters more than speed.
