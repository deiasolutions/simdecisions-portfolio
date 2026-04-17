# TASK-243: Global Commons Phase A — Static Content Foundation

## Objective

Create the static content foundation for Global Commons at deiasolutions.org: six markdown files documenting DEIA's constitutional framework, ethics configuration, carbon methodology, and design tokens.

## Context

**What is Global Commons?**

Global Commons is the public-facing documentation and governance reference for DEIA. It makes the constitutional framework visible and auditable by anyone. Phase A is static content only — no dynamic features, no database, no backend.

**Background:**

This is Wave 5 (Ship) Task 5.4. The product must be ready for strangers. Global Commons will eventually be hosted at deiasolutions.org as a public reference for DEIA governance.

**Existing Config Files:**

1. `.deia/config/ethics-default.yml` (21 lines) — Default ethics template (ADR-014)
2. `.deia/config/carbon.yml` (44 lines) — Carbon budgets and model energy estimates (ADR-015)
3. `.deia/config/grace.yml` (20 lines) — Grace period configuration for gate dispositions (ADR-014)
4. `browser/src/shell/shell-themes.css` (756 lines) — All `--sd-*` CSS variables across 5 themes

**What the bee must build:**

Six markdown files in `docs/global-commons/`:
1. `README.md` — Build/deploy instructions
2. `index.md` — Landing page (what is DEIA? what is Global Commons?)
3. `ethics.md` — Human-readable version of ethics-default.yml
4. `carbon.md` — Human-readable version of carbon.yml + grace.yml
5. `design-tokens.md` — Document all CSS variables (default theme only, overview)
6. `design-tokens-themes.md` — Document theme variants (depth, light, monochrome, high-contrast)
7. `governance.md` — Constitutional framework: ethics → governance → execution (the "Federalist Papers")

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\ethics-default.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\carbon.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\grace.yml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-5-SHIP.md`

## Deliverables

### Directory Structure
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\` directory

### README.md
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\README.md`
- [ ] Include build/deploy instructions for static site hosting
- [ ] Include table of contents linking to all documents
- [ ] Under 100 lines

### index.md (Landing Page)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\index.md`
- [ ] Section: What is DEIA? (2-3 paragraphs, from codebase reality)
- [ ] Section: What is Global Commons? (2-3 paragraphs)
- [ ] Section: Constitutional Framework Overview (1 paragraph)
- [ ] Links to all documents (ethics.md, carbon.md, design-tokens.md, governance.md)
- [ ] Under 200 lines

### ethics.md (Ethics Framework)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\ethics.md`
- [ ] Document every field in ethics-default.yml with explanation:
  - [ ] `allowed_domains` — what it does, why it exists, how it's used
  - [ ] `forbidden_actions` — each action explained (delete_production_data, bypass_gate, modify_ethics, impersonate_human, access_pii_unredacted)
  - [ ] `forbidden_targets` — each target explained (system:event-ledger, system:gate-enforcer)
  - [ ] `escalation_triggers` — each trigger explained (security, pii, financial, legal, medical)
  - [ ] `max_autonomy_tier` — what tiers are, what tier 1 means
  - [ ] `requires_rationale` — when rationales are required
  - [ ] `grace_period_seconds` — what grace periods do, why 300s default
- [ ] Include real-world examples of how each rule protects users
- [ ] Under 500 lines

### carbon.md (Carbon Methodology)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\carbon.md`
- [ ] Section: Overview — what carbon accounting is, why DEIA tracks it (ADR-015)
- [ ] Section: Model Energy Estimates — document all 8 models (Claude, GPT, Gemini, Llama) with input/output kWh per 1k tokens
- [ ] Section: Regional Intensity — explain carbon intensity by region (us_average, texas, california, eu_average, france)
- [ ] Section: Budgets — explain daily/weekly/monthly limits, alert thresholds, hard cap behavior
- [ ] Section: Grace Periods — document grace.yml violation types and gate dispositions
- [ ] Section: Calculation Method — how CO2e is calculated from tokens + model + region
- [ ] Under 500 lines

### design-tokens.md (CSS Variables — Default Theme)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\design-tokens.md`
- [ ] Section: Overview — what design tokens are, why they exist
- [ ] Section: Color System — document all `--sd-*` color variables from default theme
- [ ] Section: Typography — document font variables (sans, mono, sizes)
- [ ] Section: Shadows — document shadow system (sm, md, lg, xl, 2xl)
- [ ] Section: Gradients — document gradient variables
- [ ] Section: Glass Effects — document glass backgrounds and blur
- [ ] Section: Usage Patterns — show real examples (which components use which variables)
- [ ] Under 500 lines

### design-tokens-themes.md (CSS Variables — Theme Variants)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\design-tokens-themes.md`
- [ ] Section: Theme System Overview — how themes work (data-theme attribute)
- [ ] Section: Depth Theme — document color overrides for chromatic depth theme
- [ ] Section: Light Theme — document color overrides for light theme
- [ ] Section: Monochrome Theme — document color overrides for monochrome theme
- [ ] Section: High Contrast Theme — document color overrides for high-contrast theme
- [ ] Include comparison table showing key differences
- [ ] Under 500 lines

### governance.md (Constitutional Framework — The Federalist Papers)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\governance.md`
- [ ] Section: Introduction — what the constitutional framework is, why it exists
- [ ] Section: Three-Layer Model — ethics → governance → execution
- [ ] Section: Ethics Layer — forbidden actions, forbidden targets, escalation triggers (derived from ethics-default.yml)
- [ ] Section: Governance Layer — gate enforcer, five dispositions (ALLOW, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN)
- [ ] Section: Execution Layer — event ledger, audit trail, accountability
- [ ] Section: Checks and Balances — how the layers interact, what prevents abuse
- [ ] Section: Grace Periods — how violations trigger cooldowns vs immediate blocks
- [ ] Section: Transparency — why this is public, how strangers can audit governance
- [ ] Philosophical grounding: why these rules, what they protect against
- [ ] Under 500 lines
- [ ] CRITICAL: Do NOT invent governance rules. Document only what exists in the codebase. If something is not implemented, do not claim it exists.

## Test Requirements

This is a documentation-only task. No tests required. TDD does not apply.

## Constraints

- **No code.** Pure markdown documentation only.
- **No dynamic features.** Static content only. No APIs, no database, no React components.
- **No fabrication.** If governance rules are not documented in the codebase, do not invent them. Document what exists.
- **File paths must be absolute** in all documentation.
- **Hard Rule 4:** No file over 500 lines. Files are already scoped to stay under limit.
- **Factual accuracy:** Every statement must be traceable to actual config files or code.
- **Clarity:** Written for strangers. No internal jargon without definition.
- **Completeness:** Every field in ethics.yml, carbon.yml, grace.yml must be explained.

## Acceptance Criteria

- [ ] Directory `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\global-commons\` exists
- [ ] `README.md` exists with build/deploy instructions (<100 lines)
- [ ] `index.md` exists with landing page content (<200 lines)
- [ ] `ethics.md` exists with all ethics-default.yml fields explained (<500 lines)
- [ ] `carbon.md` exists with all carbon.yml and grace.yml fields explained (<500 lines)
- [ ] `design-tokens.md` exists with default theme CSS variables documented (<500 lines)
- [ ] `design-tokens-themes.md` exists with theme variants documented (<500 lines)
- [ ] `governance.md` exists with constitutional framework explained (<500 lines)
- [ ] All content derived from actual config files and code (no fabrication)
- [ ] All file paths are absolute
- [ ] No file exceeds 500 lines
- [ ] Every field in ethics-default.yml is documented
- [ ] Every field in carbon.yml is documented
- [ ] Every field in grace.yml is documented
- [ ] All CSS variables from shell-themes.css are documented
- [ ] governance.md provides philosophical grounding without inventing rules

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-243-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — "N/A — Documentation-only task, no tests required."
5. **Build Verification** — "N/A — Documentation-only task, no build step."
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Notes

- This is **Wave 5 (Ship)** work. The product must be ready for strangers.
- Global Commons is a public-facing artifact. Quality matters.
- This is the foundation for deiasolutions.org — the place where DEIA governance becomes auditable.
- Estimated effort: 2 hours (from WAVE-5-SHIP.md)
- This is a Sonnet task (requires high-quality writing and synthesis).
