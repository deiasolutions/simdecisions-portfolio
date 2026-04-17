# SPEC-WIKI-RECON-001: Wiki Infrastructure & Content Audit

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Determine the current state of wiki infrastructure and content in the simdecisions repository so Q88N and Q33NR can assess whether wiki-first durable context should be prioritized over the recon-then-swarm ephemeral-digest pattern proposed in `docs/proposals/2026-04-16-recon-swarm-and-decision-skill.md`. This is a read-only research audit — no code changes. The output is a YAML findings block plus actionable recommendations. This spec was drafted by Mr. AI (second-opinion reviewer) and adapted to the DEIA SUBMISSION-CHECKLIST format; the original intent and question set are preserved verbatim.

## Files to Read First

- hivenode/wiki/routes.py
- hivenode/wiki/operations.py
- hivenode/wiki/operations_routes.py
- hivenode/wiki/parser.py
- hivenode/wiki/schemas.py
- hivenode/wiki/store.py
- hivenode/wiki/onet_seed.py
- hivenode/wiki/tests
- hivenode/main.py
- browser/src/primitives/wiki/WikiPane.tsx
- browser/src/primitives/wiki/MarkdownViewer.tsx
- browser/src/primitives/wiki/BacklinksPanel.tsx
- browser/src/primitives/wiki/wikiAdapter.ts
- browser/src/apps/wikiPaneAdapter.tsx
- .deia/hive/queue/_done/SPEC-WIKI-V1.md
- .deia/hive/queue/_done/SPEC-WIKI-V1.1-LLM-WIKI-PATTERN.md
- .deia/hive/queue/_done/SPEC-WIKI-SYSTEM.md
- .deia/hive/queue/_done/SPEC-WIKI-101-database-schema-tables.md
- .deia/hive/queue/_done/SPEC-WIKI-102-wikilink-parser.md
- .deia/hive/queue/_done/SPEC-WIKI-103-crud-api-routes.md
- .deia/hive/queue/_done/SPEC-WIKI-104-backlinks-query.md
- .deia/hive/queue/_done/SPEC-WIKI-105-wikipane-primitive.md
- .deia/hive/queue/_done/SPEC-WIKI-106-markdown-viewer.md
- .deia/hive/queue/_done/SPEC-WIKI-107-backlinks-panel.md
- .deia/hive/queue/_done/SPEC-WIKI-109-enablement-exploration.md
- .deia/hive/queue/_done/SPEC-WIKI-110-status-survey.md
- docs/proposals/2026-04-16-recon-swarm-and-decision-skill.md

## Research Questions

### Infrastructure

- Q1: What does the most current wiki spec (V1, V1.1, or the WIKI-SYSTEM consolidation) specify as deliverables? Summarize the intended scope.
- Q2: Which WikiPane primitives exist and what is their functional state?
  - WikiViewer / MarkdownViewer — renders markdown, resolves wikilinks
  - WikiTree — navigable hierarchy
  - WikiEditor — create/edit pages
  - WikiBacklinks — incoming link discovery
  - WikiSearch — full-text or keyword search
  For each: status (functional / stub / missing), evidence file:line, notes.
- Q3: What is the backend state?
  - Is `hivenode/wiki/routes.py` serving pages? What endpoints exist?
  - Is the search index populated (or does search functionality exist at all)?
  - Do backlinks resolve via `hivenode/wiki/parser.py` + `operations.py`?
  - Which API endpoints are mounted in `hivenode/main.py`?
  - What is the persistence backend (SQLite? PostgreSQL? in-memory)?
- Q4: Is a wiki deployment live (wiki.shiftcenter.com, wiki.hodeia.me, or any subdomain of the Vercel frontend)? Cite evidence from `vercel.json`, deployment docs, or confirm "no deployment found."

### Content

- Q5: How many wiki pages exist currently? Where is wiki content stored (filesystem path, database table, or both)? Count concretely.
- Q6: What repo areas have wiki coverage vs. undocumented? List by subsystem: hivenode/scheduler, hivenode/wiki, simdecisions/des, simdecisions/phase_ir, browser/primitives, browser/apps, factory queue conventions, etc.
- Q7: Is there a content template or style guide for wiki pages? If yes, cite path. If no, say so.
- Q8: Are bees currently reading wiki pages as context? Search dispatch flow (`dispatch.py`, `run_queue.py`, boot injection files in `.deia/config/injections/`) for wiki references. If not wired, why not?

### Gaps

- Q9: What is blocking wiki adoption as primary bee context?
  - Missing primitives?
  - Content too sparse?
  - Discoverability problem (no index, no table of contents)?
  - No integration with dispatch flow / spec references?
  - Authentication barrier (phone can't reach it)?
  - Other?
- Q10: What is the estimated effort to reach "wiki-first viable" — meaning bees can cite wiki pages as context in specs and actually retrieve them during a run? Express as: number of follow-on specs, short title of each, rough size (small/medium/large).

## Output Format

The response file MUST include a YAML findings block matching this schema:

```yaml
infrastructure:
  spec_version: string           # "V1", "V1.1", "WIKI-SYSTEM", etc
  primitives:
    WikiViewer: { status: functional | stub | missing, evidence: "file:line", notes: "" }
    WikiTree: { status: functional | stub | missing, evidence: "file:line", notes: "" }
    WikiEditor: { status: functional | stub | missing, evidence: "file:line", notes: "" }
    WikiBacklinks: { status: functional | stub | missing, evidence: "file:line", notes: "" }
    WikiSearch: { status: functional | stub | missing, evidence: "file:line", notes: "" }
  backend:
    serving_pages: true | false
    search_functional: true | false
    backlinks_functional: true | false
    persistence: string          # "sqlite" | "postgres" | "filesystem" | "none"
    api_endpoints: [string]      # list of mounted wiki routes
  deployment:
    subdomain: string | null
    accessible: true | false
    evidence: "file:line or url"

content:
  page_count: integer
  storage_location: string
  coverage:
    documented_areas: [string]
    undocumented_areas: [string]
  template_exists: true | false
  style_guide_exists: true | false

adoption:
  bees_reading_wiki: true | false
  blocking_factors: [string]
  dispatch_flow_references: [string]   # grep results or "none"

gap_assessment:
  blocking_issues:
    - severity: P0 | P1 | P2
      issue: string
  estimated_effort_to_viable:
    follow_on_specs: integer
    descriptions: [string]

recommendations:
  - priority: P0 | P1 | P2
    action: string
    rationale: string
    supersedes_recon_proposal: true | false | partial
```

## Acceptance Criteria

- [ ] All 10 research questions answered with file:line evidence or explicit "not found" noting search scope
- [ ] YAML findings block present, valid, and complete (all top-level keys populated)
- [ ] Primitive status for all 5 WikiPane primitives reported with evidence
- [ ] Backend endpoint list matches what is actually mounted in `hivenode/main.py`
- [ ] Page count is concrete (a number, not "several")
- [ ] Coverage breakdown lists at least 5 documented areas and 5 undocumented areas or states the full set
- [ ] Recommendations section evaluates whether durable wiki-first context supersedes, partially supersedes, or is orthogonal to the ephemeral recon-then-swarm proposal
- [ ] Response file written to `.deia/hive/responses/` with the standard 8-section response header
- [ ] No code changes, no file modifications outside the response file

## Smoke Test

- [ ] Verify response file exists: test -f .deia/hive/responses/*SPEC-WIKI-RECON-001*RESPONSE.md
- [ ] Verify YAML block present: grep -c "^infrastructure:\|^content:\|^adoption:\|^gap_assessment:\|^recommendations:" on response file returns 5
- [ ] Verify all 10 questions answered: grep -c "^- Q[1-9][0:]\|^- Q10[0:]" on response file returns 10

## Constraints

- No code changes — this is a read-only research audit
- No file modifications of any kind outside the single response file
- No git operations
- No bee dispatches
- Timebox: target 90 minutes of model time; if underscoped, return partial answers with "needs deeper investigation" rather than over-run
- Output specs recommended in the report are suggestions only — do not create spec files; Q88N will approve before any are written
- Report is the only deliverable
