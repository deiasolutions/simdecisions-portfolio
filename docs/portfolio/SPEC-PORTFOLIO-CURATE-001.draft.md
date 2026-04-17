# SPEC-PORTFOLIO-CURATE-001: Portfolio Curation for 1000bulbs Application

## Priority
P0 — Required before job application submission

## Model
sonnet

## Depends On
SPEC-PORTFOLIO-NUGGET-HUNT-001 (complete)

## Objective

Create curated portfolio materials for 1000bulbs Senior AI Engineer application based on nugget hunt findings. Two primary deliverables: (1) Public teaser repo showcasing simdecisions architecture + DEIA Hive governance without product code, (2) Sanitized familybondbot README demonstrating shipped B2B SaaS capability.

---

## Context

Prior work (SPEC-PORTFOLIO-NUGGET-HUNT-001) identified 15 high-signal nuggets across:
- Platform architecture (multi-tier, 12-factor)
- AI orchestration (DEIA Hive, 1,358 completed specs)
- Correction mechanisms (3-phase validation, calibration, watchdog)
- Live deployments (Railway 5.2-day uptime, Vercel multi-domain routing)
- familybondbot (LIVE B2B SaaS, RAG pipeline, HIPAA compliance)

1000bulbs screens portfolios on four criteria:
1. Multi-tier, 12-factor apps built with AI agent teams
2. Clean architectural separation (view/API/service/persistence/database)
3. CI/CD pipelines visible in repos
4. Evidence of evaluating and correcting AI output

**Coverage:** All four criteria proven with ≥2 nuggets each. No gaps.

---

## Deliverables

### D1: Public Teaser Repo Structure

Create directory structure at `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\` with:

```
teaser-repo/
├── README.md                        # Main showcase document
├── architecture/
│   ├── deployment-architecture.md   # Multi-tier separation + 12-factor
│   ├── hive-coordination.md         # DEIA Hive agent orchestration
│   └── validation-pipeline.md       # AI correction discipline
├── diagrams/
│   ├── 5-tier-architecture.mmd      # Mermaid: browser → hivenode → engine → ORM → database
│   ├── agent-chain.mmd              # Mermaid: Q88N → Q33NR → Q33N → BEEs
│   ├── validation-gates.mmd         # Mermaid: Gate 0 → Phase 0/1/2 with healing loops
│   └── deployment-flow.mmd          # Mermaid: git push → Vercel/Railway → health checks
├── examples/
│   ├── process-13-excerpt.md        # Gate 0 + Phase 0/1/2 definitions
│   ├── traceability-example.md      # REQ → SPEC → TASK → CODE → TEST chain
│   ├── three-currencies-example.md  # Clock/Cost/Carbon response file
│   └── correction-commit-log.md     # 5 correction commits with explanations
└── LICENSE                          # CC BY 4.0
```

**Content sources:**
- README.md: Synthesize from `docs/portfolio/1000bulbs-teaser-README.draft.md` + nugget hunt findings
- Architecture docs: Extract from `.deia/HIVE.md`, `.deia/BOOT.md`, `PROCESS-0013-BUILD-INTEGRITY-3PHASE.md`
- Diagrams: Create Mermaid from verbal descriptions in teaser README draft
- Examples: Sanitize excerpts (remove internal paths, secrets, product-specific logic)

### D2: Sanitized familybondbot README

Create `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\PORTFOLIO-README.md` with:

**Sections:**
1. **Overview** — "A full-stack consumer Discord bot with multiple seasons of live usage"
2. **Architecture** — 3-tier (React SPA → FastAPI backend → PostgreSQL), Railway + Vercel deployment
3. **Key Features** — Multi-stakeholder design (3 user tiers), RAG pipeline, crisis detection, HIPAA compliance
4. **AI Orchestration** — Embedding service → retrieval → enhanced reranking → LLM, multi-provider failover (Claude → GPT-4)
5. **Testing** — 40 test files, E2E coverage, crisis detection validation
6. **Deployment** — GitHub Actions auto-merge workflow, Railway health checks, Vercel production build
7. **Tech Stack** — Python 3.12, FastAPI, SQLAlchemy, Discord.py, React, TypeScript, Vite

**Sanitization rules:**
- ❌ NO product URLs (api.familybondbot.com, app.familybondbot.com)
- ❌ NO internal file paths (use generic `backend-v2/src/services/` format)
- ❌ NO customer names or sensitive domain logic
- ✅ YES architecture patterns, tech stack, deployment evidence
- ✅ YES test counts, service counts, feature counts
- ✅ YES "full-stack consumer Discord bot" phrasing

### D3: simdecisions README Enhancements

Modify `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\README.md` to add:

**3.1. CI/CD Badges Section** (after title)
```markdown
[![Railway Deploy](https://img.shields.io/badge/Railway-Deployed-success)](https://railway.app)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-success)](https://vercel.com)
[![Tests](https://img.shields.io/badge/tests-347%20files-blue)](#)
[![Uptime](https://img.shields.io/badge/uptime-5.2%20days-green)](#)
```

**3.2. Architecture Diagrams Section** (after "What This Is")
Insert Mermaid diagrams:
- 5-tier architecture (browser → hivenode → engine → ORM → PostgreSQL)
- Agent chain (Q88N → Q33NR → Q33N → BEEs)

**3.3. AI Correction Discipline Section** (new section before "Development")
- Gate 0 (prompt → SPEC validation)
- Phase 0/1/2 (coverage, fidelity checks)
- Healing loops (max 3 retries)
- Traceability IDs (REQ → SPEC → TASK → CODE → TEST)
- Link to full PROCESS-13 doc

**3.4. Strangler Fig Section** (new section after "Architecture")
- packages/ flatten (2026-04-12)
- DEF → SIM → EXE pipeline
- 2006 call center → 2026 Phase-IR evolution

**3.5. Correction Commit Examples Section** (new section in "Development")
Link to 5 correction commits:
- SPEC-MW-051-menubar-dropdown-fix
- SPEC-DISPATCH-001-watchdog-restart-fix
- SPEC-RAG-DEDUP-001-fix-dual-routing
- SPEC-HYG-008C-ts-2345 (TypeScript hygiene)
- fix: explicit setuptools package discovery

---

## Acceptance Criteria

### AC1: Teaser Repo Structure Created
- [ ] Directory `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\` exists
- [ ] File `teaser-repo/README.md` exists and is >150 lines
- [ ] Directory `teaser-repo/architecture/` contains 3 markdown files
- [ ] Directory `teaser-repo/diagrams/` contains 4 Mermaid files (.mmd)
- [ ] Directory `teaser-repo/examples/` contains 4 example files
- [ ] File `teaser-repo/LICENSE` exists with CC BY 4.0 license text

### AC2: Teaser README Content Complete
- [ ] README contains 5-minute overview narrative (hook, problem, solution, evidence, close)
- [ ] README contains "Multi-Tier Architecture" section with embedded Mermaid diagram
- [ ] README contains "AI Agent Orchestration" section with DEIA Hive chain diagram
- [ ] README contains "AI Correction Discipline" section with validation pipeline diagram
- [ ] README contains "Deployment Evidence" section with Railway/Vercel proof
- [ ] README contains "Three Currencies" section (CLOCK/COIN/CARBON)
- [ ] README contains "Contact" section with GitHub links (no email/LinkedIn unless Q88N provides)
- [ ] README contains disclaimer: "Full private repos available on request"
- [ ] README references familybondbot as "full-stack consumer Discord bot with multiple seasons of live usage" (NO URL)
- [ ] README total length >200 lines

### AC3: Architecture Documentation Complete
- [ ] File `architecture/deployment-architecture.md` documents 5-tier separation + 12-factor signals (6 observed)
- [ ] File `architecture/hive-coordination.md` documents Q88N → Q33NR → Q33N → BEEs chain with 10 hard rules
- [ ] File `architecture/validation-pipeline.md` documents Gate 0 + Phase 0/1/2 with healing loops

### AC4: Mermaid Diagrams Created
- [ ] File `diagrams/5-tier-architecture.mmd` shows browser → hivenode → engine → ORM → database with styling
- [ ] File `diagrams/agent-chain.mmd` shows 4-tier command hierarchy with role descriptions
- [ ] File `diagrams/validation-gates.mmd` shows Gate 0 → Phase 0/1/2 with healing loops and escalation paths
- [ ] File `diagrams/deployment-flow.mmd` shows git push → build → deploy → health check pipeline

### AC5: Example Files Sanitized
- [ ] File `examples/process-13-excerpt.md` contains Gate 0 definition (no internal paths)
- [ ] File `examples/traceability-example.md` contains REQ → SPEC → TASK → CODE → TEST chain with sample IDs
- [ ] File `examples/three-currencies-example.md` contains response file template with Clock/Cost/Carbon section
- [ ] File `examples/correction-commit-log.md` contains 5 correction commits with descriptions (sanitized)

### AC6: familybondbot README Sanitized
- [ ] File `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\PORTFOLIO-README.md` exists
- [ ] README is >100 lines
- [ ] README contains NO product URLs (api.familybondbot.com, app.familybondbot.com)
- [ ] README contains NO customer names or sensitive logic
- [ ] README describes bot as "full-stack consumer Discord bot with multiple seasons of live usage"
- [ ] README contains "Architecture" section (3-tier: React → FastAPI → PostgreSQL)
- [ ] README contains "AI Orchestration" section (RAG pipeline: embedding → retrieval → reranking → LLM)
- [ ] README contains "Key Features" section (3 user tiers, crisis detection, HIPAA compliance)
- [ ] README contains "Testing" section (40 test files)
- [ ] README contains "Deployment" section (GitHub Actions, Railway, Vercel)
- [ ] README contains "Tech Stack" section

### AC7: simdecisions README Enhanced
- [ ] File `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\README.md` updated
- [ ] README contains CI/CD badges section (4 badges: Railway, Vercel, Tests, Uptime)
- [ ] README contains embedded Mermaid diagram for 5-tier architecture
- [ ] README contains embedded Mermaid diagram for agent chain
- [ ] README contains new section "AI Correction Discipline" with Gate 0 + Phase 0/1/2 description
- [ ] README contains new section "Strangler Fig Thinking" with 3 examples (flatten, DEF→SIM→EXE, 2006→2026)
- [ ] README contains new section "Correction Commit Examples" with links to 5 commits

### AC8: Sanitization Validated
- [ ] No internal file paths in teaser repo (use generic `hivenode/`, `simdecisions/` format)
- [ ] No secrets, API keys, or credentials in teaser repo
- [ ] No product-specific business logic in teaser repo
- [ ] No customer names or sensitive data in familybondbot README
- [ ] All links point to public GitHub repos or generic documentation
- [ ] License file (CC BY 4.0) present in teaser repo

### AC9: JD Signal Mapping Verified
- [ ] Teaser README explicitly maps to all 4 1000bulbs criteria (multi-tier, orchestration, correction, CI/CD)
- [ ] Each criterion has ≥2 concrete examples cited
- [ ] Deployment evidence includes HTTP 200 proof from Railway/Vercel health checks
- [ ] AI correction section includes measurable outcomes (coverage threshold 100%, fidelity ≥0.85, $0.08 per build)

---

## Files to Create

**Teaser Repo:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\README.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\architecture\deployment-architecture.md`
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\architecture\hive-coordination.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\architecture\validation-pipeline.md`
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\diagrams\5-tier-architecture.mmd`
6. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\diagrams\agent-chain.mmd`
7. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\diagrams\validation-gates.mmd`
8. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\diagrams\deployment-flow.mmd`
9. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\examples\process-13-excerpt.md`
10. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\examples\traceability-example.md`
11. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\examples\three-currencies-example.md`
12. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\examples\correction-commit-log.md`
13. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\portfolio\teaser-repo\LICENSE`

**familybondbot:**
14. `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\PORTFOLIO-README.md`

**simdecisions README modifications:**
15. Modify `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\README.md` (AC7 criteria)

---

## Smoke Tests

- [ ] Teaser repo README renders correctly in GitHub markdown preview (Mermaid diagrams visible)
- [ ] All Mermaid diagrams compile without syntax errors
- [ ] No broken links in teaser repo README
- [ ] familybondbot PORTFOLIO-README.md contains text "full-stack consumer Discord bot"
- [ ] familybondbot PORTFOLIO-README.md does NOT contain "api.familybondbot.com" or "app.familybondbot.com"
- [ ] simdecisions README contains badge section with 4 badges
- [ ] simdecisions README contains text "AI Correction Discipline"
- [ ] simdecisions README contains text "Strangler Fig Thinking"
- [ ] File count in teaser-repo/ is ≥13 files

---

## Constraints

- **Sanitization is mandatory.** No internal paths, secrets, customer data, or product URLs.
- **Mermaid syntax must be valid.** Test diagrams in a Mermaid live editor before committing.
- **CC BY 4.0 license only.** Teaser repo is documentation, not code.
- **familybondbot phrasing:** ALWAYS "full-stack consumer Discord bot with multiple seasons of live usage" (NO URL).
- **No git operations.** This spec creates files only. Q88N will review before commit.

---

## Success Criteria

Portfolio materials ready for 1000bulbs application if:
1. ✅ Public teaser repo structure complete (13 files)
2. ✅ Teaser README >200 lines with all 4 JD signals mapped
3. ✅ 4 Mermaid diagrams compile and render
4. ✅ familybondbot README sanitized (NO URLs)
5. ✅ simdecisions README enhanced with badges, diagrams, correction section
6. ✅ No sanitization violations (verified by manual review)

**Next step after this spec:** SPEC-PORTFOLIO-REFACTOR-001 (optional improvements)

---

**END OF SPEC**
