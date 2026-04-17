# SPEC-HYG-008-SPLIT-001

**MODE: EXECUTE**

**Spec ID:** SPEC-HYG-008-SPLIT-001
**Created:** 2026-04-14
**Author:** Q88N
**Type:** META — split failed spec into individual specs
**Status:** READY

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Purpose

SPEC-HYG-008 tried to fix 7 TypeScript error categories in one pass and failed — too much scope. The bee managed to eliminate TS2591 (32→0) and partially reduce TS2741 and TS2345, but ran out of time/budget.

Your job: audit the current TypeScript error state and write individual specs for each remaining category, then place them in the factory backlog.

---

## Task

### Step 1: Audit Current Error State

Run from `browser/`:

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -oP 'TS\d+' | sort | uniq -c | sort -rn | head -20
```

Record the exact count for each error code.

### Step 2: Write Individual Specs

For each error category with > 5 errors, create a spec file in `.deia/hive/queue/backlog/`. Use this template:

**Filename:** `SPEC-HYG-008{letter}-ts-{error-code}.md` where letter is A, B, C, etc.

Each spec MUST have:
- `## Priority` — P2
- `## Depends On` — None
- `## Model Assignment` — haiku (these are mechanical fixes)
- `## Objective` — Fix TS{XXXX} errors. State what the error means, current count, target: 50% reduction.
- `## Files to Read First` — List the top 5-10 files with the most errors of this type (get from tsc output)
- `## Acceptance Criteria` — Current count → target count, no new errors, tests pass
- `## Smoke Test` — `cd browser && npx tsc --noEmit 2>&1 | grep -c "TS{XXXX}"` reports fewer than N
- `## Constraints` — No `@ts-ignore`, no `as any`, no stubs, fix root cause, prefer fixing test mocks over production types, no file over 500 lines

Include guidance specific to the error type:
- **TS2345** (argument type): Fix function call argument types to match signatures
- **TS2741** (missing required property): Add missing properties to object literals and mocks
- **TS2353** (object literal may only specify known properties): Remove extra properties or update type definitions
- **TS2739** (type missing properties): Add all required properties when implementing interfaces
- **TS2683** (unsafe 'this' context): Use arrow functions or explicit this-parameter typing
- **TS2740** (type missing properties from target): Fix type assignments to include all required fields

### Step 3: Verify Specs Parse

For each spec you write, confirm it has all required factory headers by checking the file exists and contains `## Model Assignment` and `## Smoke Test`.

### Step 4: Report

List all specs created with their error codes and target reductions.

---

## Acceptance Criteria

- [ ] `npx tsc --noEmit` run and current error counts recorded
- [ ] One spec per error category (minimum 5 specs, maximum 8)
- [ ] Each spec targets 50% reduction of its error category
- [ ] All specs placed in `.deia/hive/queue/backlog/`
- [ ] All specs have required factory headers (Priority, Model Assignment, Smoke Test, Constraints)
- [ ] No spec tries to fix more than one error category

## Smoke Test

```bash
ls .deia/hive/queue/backlog/SPEC-HYG-008*.md | wc -l
# Expected: >= 5
```

## Constraints

- Do NOT fix any TypeScript errors yourself — only write specs
- Each spec must be self-contained — a bee with no context should be able to execute it
- Model assignment: haiku for all (these are mechanical fixes)
- Do not create specs for error categories with fewer than 5 occurrences
- Write specs to `.deia/hive/queue/backlog/` — NOT `_active/`, NOT root queue

## Response File

`.deia/hive/responses/20260414-HYG-008-SPLIT-RESPONSE.md`

---

*SPEC-HYG-008-SPLIT-001 — Q88N — 2026-04-14*
