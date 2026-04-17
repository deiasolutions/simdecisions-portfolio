# TASK-243: Global Commons Phase A — Static Content Documentation

## Objective
Create the static content for Global Commons at deiasolutions.org: the DEIA founding documents (Federalist Papers), design tokens reference, ethics framework, and carbon budget documentation.

## Context
Wave 5 Ship. Global Commons is the public-facing documentation and governance reference for DEIA. Phase A is static content only — no dynamic features, no API endpoints, no database changes. This is what makes the constitutional framework visible and auditable by anyone.

The content must be derived from actual config files (ethics.yml, carbon.yml, grace.yml) and actual CSS variables in the codebase. No invented content.

## Source Spec
From `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-243-global-commons-phase-a.md`
Reference: `docs/specs/WAVE-5-SHIP.md` — Task 5.4

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\ethics.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\carbon.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\grace.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

## Files You May Create (NEW FILES ONLY)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\index.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\ethics.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\design-tokens.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\carbon.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\governance.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\README.md`

## Files You Must NOT Modify
- Any existing files in `docs/` (only create NEW files in `docs/global-commons/`)
- Any files in `browser/` directory
- Any files in `hivenode/` directory
- Any files in `engine/` directory
- Any config files in `.deia/config/` (read only, do not modify)

## Deliverables
- [ ] Create `docs/global-commons/` directory
- [ ] Write `index.md`:
  - What is DEIA? (1-2 paragraphs)
  - What is Global Commons? (1-2 paragraphs)
  - Links to all other documents in this directory
  - Clean, professional tone
- [ ] Write `ethics.md`:
  - Render the ethics framework from `.deia/config/ethics.yml`
  - Human-readable explanation of each rule
  - Include rule IDs, severity levels, descriptions
  - Formatted as clean markdown tables + prose
- [ ] Write `design-tokens.md`:
  - Document all `--sd-*` CSS variables from `shell-themes.css`
  - Group by category (colors, spacing, typography, etc.)
  - Include variable name, default value, description
  - Formatted as markdown tables
- [ ] Write `carbon.md`:
  - Render the carbon budget framework from `.deia/config/carbon.yml`
  - Explain what CARBON currency means
  - Include budget limits, thresholds, penalties
  - Human-readable prose + tables
- [ ] Write `governance.md`:
  - Explain how the constitutional framework works
  - Flow: ethics → governance → execution
  - How policies are enforced via gate_enforcer
  - Reference to ethics.yml and carbon.yml
- [ ] Write `README.md`:
  - Build/deploy instructions for static site
  - How to update content when config files change
  - Contribution guidelines

## Test Requirements
- [ ] No tests required (pure documentation)
- [ ] Verify all markdown renders correctly in a markdown previewer
- [ ] Verify all links between docs work correctly
- [ ] Verify all content is factually derived from source files

## Constraints
- No file over 500 lines (split documents if needed)
- No stubs — every document must be complete
- Content must be factual — derived from actual config files
- Professional tone, suitable for public documentation

## Acceptance Criteria
- [ ] All 6 markdown files created in `docs/global-commons/`
- [ ] `index.md` explains DEIA and Global Commons with links to all other docs
- [ ] `ethics.md` accurately renders all rules from `ethics.yml`
- [ ] `design-tokens.md` documents all `--sd-*` variables from `shell-themes.css`
- [ ] `carbon.md` accurately renders carbon budget from `carbon.yml`
- [ ] `governance.md` explains the constitutional framework flow
- [ ] `README.md` includes build/deploy instructions
- [ ] All markdown renders cleanly (no syntax errors)
- [ ] All internal links work
- [ ] No invented content — everything traceable to source files

## Model Assignment
sonnet

## Priority
P2

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-243-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — "No tests required (pure documentation)" + manual verification summary
5. **Build Verification** — markdown syntax check, link verification
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, future enhancements, recommended next tasks

DO NOT skip any section.
