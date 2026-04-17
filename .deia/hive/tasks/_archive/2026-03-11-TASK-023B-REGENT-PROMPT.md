# TASK-023B: Regent Bot Prompt Template

## Objective
Create the regent bot system prompt template at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\regent-bot-prompt.md` — a mechanical review checklist and process guide for Q88NR-bot.

## Context
This is part of SPEC-BUILD-QUEUE-001 Phase 1. Q88NR-bot (the cheap LLM that runs overnight) gets this prompt injected when processing specs. It's NOT a task file — it's a reusable system prompt that tells the bot how to behave mechanically. The bot reads specs, writes briefings, dispatches Q33N, reviews task files, and creates fix specs. It does NOT make strategic decisions or write code.

The prompt must be concise (100-200 lines), mechanical, and follow the HIVE.md chain of command.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-BUILD-QUEUE-001.md` (sections 4, 7)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\HIVE.md` (full workflow)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\BOOT.md` (10 hard rules for injection)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\regent-bot-prompt.md`
- [ ] Section 1: Identity ("You are Q88NR-bot, a mechanical regent. You follow HIVE.md exactly.")
- [ ] Section 2: Abbreviated chain of command (Q88NR-bot → briefing → Q33N → bees → results)
- [ ] Section 3: Mechanical review checklist for Q33N's task files (deliverables match spec? file paths absolute? test requirements present? CSS var(--sd-*)? files under 500 lines? no stubs/TODOs?)
- [ ] Section 4: Correction rule (max 2 correction cycles on Q33N's tasks, then approve with ⚠️ APPROVED_WITH_WARNINGS)
- [ ] Section 5: Fix cycle rule (if bees fail tests, create P0 fix spec, max 2 fix cycles, then flag NEEDS_DAVE)
- [ ] Section 6: Budget awareness ("Queue runner enforces limits. Report costs accurately.")
- [ ] Section 7: What you NEVER do (strategic decisions, modify specs, override hard rules, write code, skip Q33N)
- [ ] Keep to 100-200 lines, concise and mechanical

## Test Requirements
- [ ] Write test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_regent_prompt.py`
- [ ] Test: File exists and is valid markdown
- [ ] Test: Contains required sections (identity, chain of command, review checklist, correction rule, fix cycle rule, budget, never do)
- [ ] Test: Line count between 50 and 300 (allowing some margin)
- [ ] Test: Contains keywords: "Q88NR-bot", "Q33N", "briefing", "mechanical", "APPROVED_WITH_WARNINGS", "NEEDS_DAVE", "fix cycle"
- [ ] Test: Does NOT contain strategic language like "decide", "choose approach", "design", "architect" (it's mechanical, not strategic)
- [ ] Minimum 5 tests

## Constraints
- 100-200 lines target (hard max: 300)
- Markdown format
- No stubs
- Mechanical tone — no philosophy, no strategic guidance
- Focus on process execution, not decision-making

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260311-TASK-023B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
