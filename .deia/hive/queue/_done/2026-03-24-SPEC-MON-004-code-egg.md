# SPEC: MON-004 code.shiftcenter.com EGG

## Priority
P1

## Depends On
- SPEC-MON-001-monaco-applet-component
- SPEC-MON-002-monaco-volume-adapter
- SPEC-MON-003-monaco-relay-bus

## Objective
Assemble code.shiftcenter.com — the ShiftCenter code editing product as an EGG config with two tab layouts: code-default (editor + log-viewer) and code-zen (editor only, no chrome).

## Context
With the Monaco applet built and wired (MON-001/002/003), this task creates the EGG file and registers the code subdomain in the EGG router. Both tabs share nodeId "editor-main" so document content survives tab swaps.

## Files to Read First
- eggs/canvas2.egg.md
- eggs/efemera.egg.md
- browser/src/eggs/eggResolver.ts

## Task File
Full task spec with acceptance criteria and file locations:
.deia/hive/queue/_stage/2026-03-24-TASK-MON-004-code-egg.md

Read the task file above — it contains the complete scope, file locations, constraints, and acceptance criteria. Follow it exactly.

## Deliverables
1. eggs/code.egg.md — EGG definition with code-default and code-zen tabs
2. browser/src/eggs/eggResolver.ts — add code subdomain routing
3. browser/src/eggs/__tests__/codeEgg.test.ts — EGG inflate test (min 5 tests)

## Acceptance Criteria
- [ ] code.egg.md inflates without errors via EGG loader
- [ ] code-default tab renders editor + log-viewer side by side
- [ ] code-zen tab renders editor only with activity bar hidden
- [ ] Switching between tabs preserves editor content (shared nodeId)
- [ ] code subdomain routes correctly in EGG router
- [ ] All tests pass (minimum 5 tests)
- [ ] npx vite build passes

## Response File
.deia/hive/responses/20260324-TASK-MON-004-RESPONSE.md
