# TASK-C: Generate MW Spec Files — Phase 1-2 Builds

## Objective
Generate spec files for Phase 1 (command-interpreter build) and Phase 2 (input surfaces build) tasks. Total: 14 spec files.

## Context
Phase 1 is the command-interpreter foundation — must complete before other components can integrate. Phase 2 builds the input surfaces (voice, FAB, conversation pane) on top of the command-interpreter.

**Phase 1 (Command-Interpreter Build):**
- MW-001: BUILD: command-interpreter core parser + fuzzy
- MW-002: BUILD: command-interpreter PRISM-IR emission
- MW-003: BUILD: command-interpreter confirm + ambiguity
- MW-V01: VERIFY: command-interpreter

**Phase 2 (Input Surfaces Build):**
- MW-004: BUILD: voice-input Web Speech API wrapper
- MW-005: BUILD: voice-input command-interpreter integration
- MW-V02: VERIFY: voice-input
- MW-006: BUILD: quick-actions FAB component
- MW-007: BUILD: quick-actions mic + keyboard buttons
- MW-V03: VERIFY: quick-actions
- MW-008: BUILD: conversation-pane multi-input rendering
- MW-009: BUILD: conversation-pane multi-LLM routing
- MW-010: BUILD: conversation-pane output surfaces
- MW-V04: VERIFY: conversation-pane

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — task registry
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/_active/SPEC-MW-S01-command-interpreter.md` — spec template
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/prism/ir.py` — PRISM-IR spec (target output for command-interpreter)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/` — existing command routing pattern
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/` — existing conversation pane (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/hooks/` — existing hooks patterns

## Deliverables
Write 14 spec files to `.deia/hive/queue/backlog/`:
- [ ] `SPEC-MW-001-command-interpreter-core.md`
- [ ] `SPEC-MW-002-command-interpreter-prism-ir.md`
- [ ] `SPEC-MW-003-command-interpreter-confirm.md`
- [ ] `SPEC-MW-V01-verify-command-interpreter.md`
- [ ] `SPEC-MW-004-voice-input-api-wrapper.md`
- [ ] `SPEC-MW-005-voice-input-integration.md`
- [ ] `SPEC-MW-V02-verify-voice-input.md`
- [ ] `SPEC-MW-006-quick-actions-fab.md`
- [ ] `SPEC-MW-007-quick-actions-buttons.md`
- [ ] `SPEC-MW-V03-verify-quick-actions.md`
- [ ] `SPEC-MW-008-conversation-pane-rendering.md`
- [ ] `SPEC-MW-009-conversation-pane-llm-routing.md`
- [ ] `SPEC-MW-010-conversation-pane-output.md`
- [ ] `SPEC-MW-V04-verify-conversation-pane.md`

## Spec Writing Guidelines
Same as TASK-B:
1. **## Priority** — P1
2. **## Objective** — concrete deliverable (BUILD or VERIFY task)
3. **## Context** — what gets built, dependencies on prior tasks, integration points
4. **## Files to Read First** — absolute paths to relevant files (PRISM-IR, command-palette, hooks, tests)
5. **## Acceptance Criteria** — 8-12 concrete deliverables
6. **## Smoke Test** — 4-6 verification steps
7. **## Model Assignment** — "sonnet"
8. **## Constraints** — file locations, max 500 lines, CSS variables, TDD, no stubs

**BUILD tasks:** Describe the implementation (what code to write, what tests to write first, what files to create).

**VERIFY tasks:** Describe E2E smoke tests, integration tests, manual testing steps, coverage verification. VERIFY specs are shorter (30-50 lines) but must list all critical paths to test.

**Dependencies:**
- MW-001 depends on MW-T01 (test written first)
- MW-002 depends on MW-001 (sequential build)
- MW-003 depends on MW-002
- MW-V01 depends on MW-003
- MW-004 depends on MW-T02 and MW-V01
- MW-005 depends on MW-004
- And so on...

Use the TASKS list in `scheduler_mobile_workdesk.py` as the source of truth for dependencies.

## Test Requirements
N/A — spec-writing task.

## Acceptance Criteria
- [ ] 14 spec files created in `.deia/hive/queue/backlog/`
- [ ] Each spec is 50-100 lines (VERIFY specs can be 30-50)
- [ ] Each spec has real content (not boilerplate)
- [ ] "Files to Read First" lists actual source files
- [ ] Dependencies match scheduler_mobile_workdesk.py
- [ ] All specs use "sonnet" model
- [ ] Naming: `SPEC-MW-{ID}-{short-description}.md`

## Smoke Test
- [ ] All 14 files exist in `.deia/hive/queue/backlog/`
- [ ] Each file has all required sections
- [ ] Dependencies match TASKS list
- [ ] Open MW-001 spec — describes fuzzy matching implementation, not just "implement parser"

## Constraints
- Output location: `.deia/hive/queue/backlog/`
- Each BUILD spec: 50-100 lines
- Each VERIFY spec: 30-50 lines
- NO STUBS — write real content
- Read codebase first
- Use absolute paths

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-C-MW-SPECS-PHASE1-2-RESPONSE.md`

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
