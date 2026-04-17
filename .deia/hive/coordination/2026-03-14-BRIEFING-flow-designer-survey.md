# BRIEFING: Flow Designer Survey

**Date:** 2026-03-14
**From:** Q88NR
**To:** Q33N
**Priority:** P0

## Objective

Survey the Flow Designer codebase in the platform repo and produce a complete inventory of what's there, what it depends on, and where it would go in shiftcenter.

## Source Location

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\`

This is ~17,000 lines of ReactFlow-based visual process editor code. It includes simulation playback, comparison mode, tabletop, checkpoints, and collaboration features.

## What We Need

### Task 1: Directory survey
- List every file in the directory tree with line counts
- Group files by subdirectory / functional area
- Total line count per group and overall

### Task 2: Dependency analysis
- For each file, identify imports that reference code OUTSIDE the flow designer directory
- Catalog all external dependencies (npm packages, internal platform modules, shared types, stores, services)
- Flag which external dependencies already exist in shiftcenter vs which would need porting

### Task 3: Mapping to shiftcenter
- For each functional group, recommend where in `browser/src/` it should land
- Note what already exists in shiftcenter's `browser/src/primitives/canvas/` that overlaps

## Dispatch Plan

Two bees, both sonnet:
1. **TASK-092**: Survey directory tree + line counts + dependency analysis
2. **TASK-093**: Read key files, map to shiftcenter locations, identify overlaps with existing canvas code

## Output

Each bee writes a response to `.deia/hive/responses/`. Q33N consolidates into a single survey report.
