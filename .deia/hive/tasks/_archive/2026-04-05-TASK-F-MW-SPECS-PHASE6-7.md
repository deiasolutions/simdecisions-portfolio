# TASK-F: Generate MW Spec Files — Phase 6-7 Terminal + Integration

## Objective
Generate spec files for Phase 6 (terminal enhancements) and Phase 7 (integration tasks). Total: 9 spec files.

## Context
Phase 6 adds TF-IDF suggestion system to terminal for context-aware command suggestions. Phase 7 integrates everything: wires Shell.tsx for responsive layout, creates workdesk.set.md egg config, integrates new primitives with RTD bus, defines PRISM-IR vocabulary, and runs E2E tests.

**Phase 6 (Terminal Enhancements):**
- MW-034: BUILD: TF-IDF suggestion index
- MW-035: BUILD: Pill UI + scrollable list
- MW-036: BUILD: Context weighting logic

**Phase 7 (Integration):**
- MW-037: BUILD: Shell.tsx responsive wiring
- MW-038: BUILD: workdesk.set.md authoring
- MW-039: BUILD: RTD bus integration for new primitives
- MW-040: BUILD: PRISM-IR command vocabulary definition
- MW-041: TEST: Voice → command → PRISM-IR E2E flow
- MW-042: VERIFY: End-to-end mobile device test

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — task registry
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S01-command-interpreter.md` — spec template
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/` — existing terminal component
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/shell/Shell.tsx` — shell structure (MW-037)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/eggs/` — EGG config examples (MW-038)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/bus/` — RTD bus system (MW-039)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/prism/ir.py` — PRISM-IR spec (MW-040)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/e2e/` — E2E test patterns (MW-041, MW-042)

## Deliverables
Write 9 spec files to `.deia/hive/queue/backlog/`:

**Phase 6:**
- [ ] `SPEC-MW-034-tfidf-index.md`
- [ ] `SPEC-MW-035-pill-ui.md`
- [ ] `SPEC-MW-036-context-weighting.md`

**Phase 7:**
- [ ] `SPEC-MW-037-shell-responsive.md`
- [ ] `SPEC-MW-038-workdesk-egg.md`
- [ ] `SPEC-MW-039-rtd-bus-integration.md`
- [ ] `SPEC-MW-040-prism-ir-vocabulary.md`
- [ ] `SPEC-MW-041-e2e-voice-flow.md`
- [ ] `SPEC-MW-042-verify-mobile-e2e.md`

## Spec Writing Guidelines
**Phase 6 (TF-IDF):**
- MW-034: Build TF-IDF index for terminal command history. Use Python's scikit-learn or simple TF-IDF implementation. Backend task.
- MW-035: React component for pill UI (horizontal scrollable list, pill buttons with tap handlers). Frontend task.
- MW-036: Weighting logic that combines TF-IDF score + current context (active pane, recent commands). Backend + frontend integration.

**Phase 7 (Integration):**
- MW-037: Shell.tsx responsive wiring — add breakpoints, swap layouts (desktop: sidebar, mobile: drawer), hide/show components based on viewport.
- MW-038: Write `workdesk.set.md` EGG config that composes all mobile primitives into a working product. Reference existing EGG files in `eggs/` for format.
- MW-039: RTD bus integration — wire new primitives (quick-actions-fab, mobile-nav, notification-pane, queue-pane, diff-viewer) to RTD bus events. Subscribe/publish patterns.
- MW-040: Define PRISM-IR command vocabulary (e.g., `{ "command": "open", "target": "terminal" }` → IR structure). Formal schema.
- MW-041: E2E test (Playwright or Cypress) that exercises voice → command-interpreter → PRISM-IR → execution flow. End-to-end happy path.
- MW-042: Full mobile device E2E test. Use real device (Chrome DevTools remote debugging) or emulator. Test all primitives, gestures, navigation.

**TEST/VERIFY specs:** MW-041 and MW-042 are test specs. Describe what to test, how to set up test environment, what E2E scenarios to cover.

## Test Requirements
N/A — spec-writing task.

## Acceptance Criteria
- [ ] 9 spec files created in `.deia/hive/queue/backlog/`
- [ ] Each spec is 50-100 lines (VERIFY/TEST specs 40-70)
- [ ] Each spec has real content (not boilerplate)
- [ ] "Files to Read First" lists actual source files
- [ ] Dependencies match scheduler_mobile_workdesk.py
- [ ] All specs use "sonnet" model
- [ ] Naming: `SPEC-MW-{ID}-{short-description}.md`

## Smoke Test
- [ ] All 9 files exist in `.deia/hive/queue/backlog/`
- [ ] Each file has all required sections
- [ ] Dependencies match TASKS list
- [ ] Open MW-037 spec — describes Shell.tsx responsive layout changes (breakpoints, drawer, hidden elements)
- [ ] Open MW-038 spec — describes EGG file format, lists primitives to include, composition structure
- [ ] Open MW-041 spec — describes E2E test steps (trigger voice input, parse command, emit IR, verify execution)

## Constraints
- Output location: `.deia/hive/queue/backlog/`
- Each BUILD spec: 50-100 lines
- Each TEST/VERIFY spec: 40-70 lines
- NO STUBS — write real content
- Read codebase first (Shell.tsx, eggs/, bus/, prism/ir.py, e2e/)
- Use absolute paths

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-F-MW-SPECS-PHASE6-7-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A
5. **Build Verification** — N/A
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
