# SPEC-PORTFOLIO-CURATE-001: Portfolio Curation for 1000bulbs Application

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Create curated portfolio materials for 1000bulbs Senior AI Engineer application based on nugget hunt findings. Two primary deliverables: (1) all files for a public teaser repo `deiasolutions/simdecisions-architecture` showcasing architecture + DEIA Hive governance without product code, and (2) a sanitized familybondbot PORTFOLIO-README demonstrating shipped B2B SaaS capability. Also enhance the simdecisions README with badges, diagrams, and correction discipline section. All files written locally — Q88N handles repo creation and push.

## Files to Read First

- docs/portfolio/1000bulbs-portfolio-audit.md
- docs/portfolio/1000bulbs-teaser-README.draft.md
- docs/portfolio/1000bulbs-follow-on-specs.md
- docs/portfolio/1000bulbs-nugget-hunt-recommendation.md
- .deia/BOOT.md
- .deia/HIVE.md
- .deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md

## Acceptance Criteria

### Teaser Repo Files (written to docs/portfolio/teaser-repo/)
- [ ] File `docs/portfolio/teaser-repo/README.md` exists and is >200 lines
- [ ] File `docs/portfolio/teaser-repo/EXECUTIVE-SUMMARY.md` exists using SCIPAB structure (Situation, Complication, Implication, Position, Action, Benefit sections)
- [ ] File `docs/portfolio/teaser-repo/metadata.json` exists with valid Schema.org markup
- [ ] Directory `docs/portfolio/teaser-repo/architecture/` contains 3 files: deployment-architecture.md, hive-coordination.md, validation-pipeline.md
- [ ] Directory `docs/portfolio/teaser-repo/diagrams/` contains 4 Mermaid files: 5-tier-architecture.mmd, agent-chain.mmd, validation-gates.mmd, deployment-flow.mmd
- [ ] Directory `docs/portfolio/teaser-repo/examples/` contains 4 files: process-13-excerpt.md, traceability-example.md, three-currencies-example.md, correction-commit-log.md
- [ ] File `docs/portfolio/teaser-repo/specs/product-loop.prism.md` exists
- [ ] File `docs/portfolio/teaser-repo/LICENSE` contains CC BY 4.0 text
- [ ] File `docs/portfolio/teaser-repo/.github/workflows/validate.yml` exists with Mermaid syntax validation
- [ ] Total file count in teaser-repo/ is >= 17

### Teaser README Content
- [ ] First 500 chars contain JD keywords: multi-tier, 12-factor, AI developer agents, CI/CD, evaluate and correct
- [ ] YAML frontmatter present with keywords array
- [ ] Contains "Multi-Tier, 12-Factor Architecture" section with Mermaid diagram using JD layer names (view, API interface, service/business logic, persistence, database)
- [ ] Contains "Directing AI Developer Agents" section with DEIA Hive chain diagram
- [ ] Contains comparison note positioning DEIA Hive vs other frameworks (comparable in scope, with built-in correction mechanisms)
- [ ] Contains "Evaluating and Correcting AI-Generated Output" section with validation pipeline diagram
- [ ] Contains "CI/CD Pipelines and Deployment" section with Railway/Vercel evidence
- [ ] Contains "Three Currencies" section (CLOCK/COIN/CARBON)
- [ ] Contains "Strangler Fig Pattern: Incremental Delivery" section with 3 examples
- [ ] Contains snapshot date notice: "Architecture snapshot as of April 2026"
- [ ] Contains "Contact" section with LinkedIn + GitHub only (no email)
- [ ] References familybondbot as "full-stack consumer Discord bot with multiple seasons of live usage — private repo available on request"

### Mermaid Diagrams
- [ ] 5-tier-architecture.mmd uses labels: view, API interface, service/business logic, persistence, database
- [ ] agent-chain.mmd shows 4-tier hierarchy: Q88N → Q33NR → Q33N → BEEs with role descriptions
- [ ] validation-gates.mmd shows Gate 0 → Phase 0/1/2 with healing loops and escalation
- [ ] deployment-flow.mmd shows git push → build → deploy → health check pipeline
- [ ] All .mmd files contain valid Mermaid syntax

### familybondbot README
- [ ] File `docs/portfolio/familybondbot-PORTFOLIO-README.md` exists and is >100 lines
- [ ] Contains NO product URLs (api.familybondbot.com, app.familybondbot.com)
- [ ] Contains NO customer names or sensitive domain logic
- [ ] Describes bot as "full-stack consumer Discord bot with multiple seasons of live usage"
- [ ] Uses JD terminology (multi-tier, CI/CD pipelines, tests that validate specification)
- [ ] Contains sections: Multi-Tier Architecture, Directing AI Developer Agents (RAG pipeline), Key Features, Testing, CI/CD Pipelines, Tech Stack

### Sanitization
- [ ] No internal file paths (hivenode/*, .deia/*) appear in any teaser-repo/ file
- [ ] No secrets, API keys, or credentials in any file
- [ ] No product-specific business logic exposed
- [ ] All links point to public GitHub repos or generic documentation

### Bot-Friendly Optimizations
- [ ] YAML frontmatter in teaser README with keywords
- [ ] metadata.json with Schema.org markup and codeRepository field
- [ ] Descriptive file names throughout (no arch-v2.md style names)

## Smoke Test

- [ ] `find docs/portfolio/teaser-repo -type f | wc -l` returns >= 17
- [ ] `head -c 500 docs/portfolio/teaser-repo/README.md | grep -c "multi-tier\|12-factor\|AI developer\|CI/CD\|evaluate and correct"` returns >= 3
- [ ] `python -c "import json; json.load(open('docs/portfolio/teaser-repo/metadata.json'))"` exits 0
- [ ] `grep -r "api.familybondbot.com" docs/portfolio/` returns no matches
- [ ] `grep -r ".deia/" docs/portfolio/teaser-repo/` returns no matches
- [ ] `wc -l < docs/portfolio/teaser-repo/README.md` returns > 200
- [ ] `wc -l < docs/portfolio/familybondbot-PORTFOLIO-README.md` returns > 100

## Constraints

- Sanitization is mandatory — no internal paths, secrets, customer data, or product URLs in any deliverable
- Mermaid syntax must be valid
- CC BY 4.0 license only for teaser repo (documentation, not code)
- JD terminology required — use their exact phrases where applicable (see JD Terminology section below)
- familybondbot phrasing: ALWAYS "full-stack consumer Discord bot with multiple seasons of live usage"
- Contact: LinkedIn + GitHub only, no email
- No git operations — all files written locally under docs/portfolio/. Q88N handles repo creation and push.
- No file over 500 lines
- No stubs — every file complete

## JD Terminology to Use

| Their Term | Where to Use |
|------------|--------------|
| "Multi-tier, 12-factor applications" | README intro, architecture section |
| "AI developer agents" | Agent orchestration section |
| "Strangler Fig pattern" | Strangler Fig section |
| "Clean separation of concerns" | Architecture section |
| "View, API interface, service/business logic, persistence, database" | 5-tier diagram labels |
| "SOLID violations, DRY violations" | AI correction section |
| "Tests that validate specification rather than implementation" | Testing section |
| "Vertical slices" | Architecture section |
| "CI/CD pipelines" | Deployment section |
| "Evaluate and correct AI-generated output" | AI correction section header |
| "Incremental delivery" | Strangler Fig section |
| "Full-stack ownership" | Intro |

## Terms to Avoid

| Term | Why | Alternative |
|------|-----|-------------|
| Amazon Leadership Principles | Amazon proprietary | Describe behaviors without naming |
| BMad-method | External branded methodology | "Constitutional AI governance via DEIA Hive" |
| SCIPAB | Consulting jargon (OK in EXECUTIVE-SUMMARY.md structure, not as label) | "Present recommendations with context, trade-offs, and evidence" |
| LangGraph/CrewAI/AutoGen (as peers) | Positions as user not builder | "DEIA Hive — comparable in scope, with built-in correction mechanisms" |

## Decisions Locked

| Decision | Answer |
|----------|--------|
| Contact info | LinkedIn + GitHub only (no email) |
| familybondbot access | Wait to be asked |
| 2006 materials | Wait to be asked |
| Teaser repo | New standalone repo (files staged locally at docs/portfolio/teaser-repo/) |
| Relationship to live code | Teaser is snapshot as of April 2026; live code at deiasolutions/simdecisions (private) |

## 12-Factor Compliance Evidence

Use this table in the architecture documentation:

| # | Factor | simdecisions Evidence |
|---|--------|----------------------|
| I | Codebase | Single repo → Railway (2 services) + Vercel (4 domains) |
| II | Dependencies | pyproject.toml, package.json, pinned Dockerfile |
| III | Config | railway.toml env vars, no hardcoded secrets |
| IV | Backing Services | PostgreSQL as attached resource |
| V | Build, Release, Run | GitHub → Railway/Vercel CI/CD |
| VI | Processes | Stateless hivenode; state in PostgreSQL |
| VII | Port Binding | FastAPI binds $PORT |
| VIII | Concurrency | Separate scheduler/dispatcher/triage processes |
| IX | Disposability | Watchdog, health checks, resume context |
| X | Dev/Prod Parity | Same Docker image everywhere |
| XI | Logs | Event Ledger as structured stream |
| XII | Admin Processes | _tools/ scripts, one-off bee tasks |
