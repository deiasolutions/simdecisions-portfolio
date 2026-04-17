# SPEC-PORTFOLIO-NUGGET-HUNT-001: Portfolio Curation for 1000bulbs Application

## Priority

P0

## Model

sonnet

## Depends On

None

## Objective

Q88N is applying for Senior AI Engineer at 1000bulbs. Applications are **screened on GitHub portfolio before any interview.** This spec does a folder/file-level deep dive of `simdecisions` (the flagship monorepo) plus a secondary reference to familybondbot (a full-stack consumer Discord bot with multiple seasons of live usage), curated and tailored to the 1000bulbs screening criteria.

Prior audit (SPEC-PORTFOLIO-1000BULBS-001) scored at the repo level and missed the point. This redo focuses on individual files and folders as portfolio nuggets.

---

## 1000bulbs Screening Criteria

Portfolio **must** demonstrate:

1. **Multi-tier, 12-factor applications built using teams of AI developer agents**
2. **Clear architectural separation:** view, API interface, service/business logic, persistence, database
3. **CI/CD pipelines** integrated into projects
4. **Evidence that you evaluate and correct AI-generated output**

Additional signals: Strangler Fig, AI orchestration expertise, critical AI evaluation, full-stack ownership.

---

## Orchestration Architecture

```
ORCHESTRATOR (sonnet)
├── reads prior audit + JD criteria + repo structure
├── launches N Sonnet Queens in parallel
│   Each Queen (subagent_type: "general-purpose", model: "sonnet"):
│   ├── launches Sonnet Bees in parallel
│   │   (subagent_type: "Explore" for surveys, "Bash" for probes)
│   ├── reads all bee reports
│   └── writes domain-level nugget report + refactor observations
├── reads ALL queen reports
└── writes 3 deliverables (Phase B)
```

Queens MUST launch bees in parallel. All queens complete before final deliverables.

---

## Phase A — Research

Per nugget found:
```yaml
- path: "absolute path to file or folder"
  kind: README | architecture-doc | code-pattern | spec | test | config | deployment
  jd_signal: "which 1000bulbs criterion (1-4) or 'differentiator'"
  one_line_pitch: "why a reviewer would care"
  share_classification: PUBLIC_TEASER | EXCERPT_OK | REFERENCE_ONLY
  effort_to_extract: "hours to sanitize"
  verbatim_shareable: true | false
```

Per refactor opportunity:
```yaml
- path: "absolute path"
  issue: "what's wrong"
  jd_relevance: "which criterion this strengthens"
  severity: cosmetic | structural | blocker
  effort: "hours to fix"
  recommendation: "what to do"
```

**QUEEN-1: Platform Architecture** — prove multi-tier 12-factor. Survey:
`hivenode/main.py`, `hivenode/routes/`, `hivenode/relay/`, `hivenode/ledger/`,
`hivenode/wiki/`, `hivenode/inventory/`, `hivenode/shell/`,
`simdecisions/des/`, `simdecisions/optimization/`, `simdecisions/phase_ir/`,
`simdecisions/flows/`, `simdecisions/database.py`,
`browser/src/App.tsx`, `browser/src/shell/`, `browser/src/primitives/`,
`browser/src/sets/`, `browser/vite.config.ts`,
`hodeia_auth/main.py`, `pyproject.toml`, `Dockerfile`, `railway.toml`, `vercel.json`

**QUEEN-2: DEIA Hive & AI Orchestration** — prove "teams of AI developer agents." Survey:
`.deia/BOOT.md`, `.deia/HIVE.md`, `.deia/processes/`,
`.deia/config/ethics.yml`, `.deia/config/carbon.yml`,
`hivenode/scheduler/scheduler_daemon.py`,
`hivenode/scheduler/dispatcher_daemon.py`,
`hivenode/scheduler/triage_daemon.py`,
`.deia/hive/queue/_done/` (count specs, sample 5-10), `.deia/hive/queue/_escalated/`

**QUEEN-3: AI Correction Evidence** — prove "evaluate and correct AI output." Survey:
`git log --oneline -100` for correction patterns,
`.deia/processes/` for Gate 0 / triage logic,
`_tools/inventory.py`, `_tools/ir_density.py`, `_tools/estimates_db.py`,
`tests/hivenode/`, `tests/simdecisions/`, `CLAUDE.md`

**QUEEN-4: Live Services Verification** — probe with curl:
`https://hodeia.me/health`, `https://hodeia.me/jwks.json`,
Vercel URL (from `vercel.json`), Railway URL (from `railway.toml`).
Record HTTP status codes, response times. Output deployment truth table. No overclaiming.

**QUEEN-5: familybondbot** — assess as shipped end-to-end product evidence.
Repo: `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\`
Survey structure, README, features, code quality. Do NOT link to product URL.

---

## Phase B — Synthesis

**B1.** Write `docs/portfolio/1000bulbs-nugget-hunt-recommendation.md` containing:
top 10-15 nuggets ranked by signal strength x extraction effort,
JD signal coverage matrix (4 criteria + differentiators, ≥2 nuggets each),
deployment truth table, 5-minute story arc, familybondbot assessment,
recommended showcase format, cost-benefit table, 3-5 Q88N decisions needed.

**B2.** Write `docs/portfolio/SPEC-PORTFOLIO-CURATE-001.draft.md` containing:
SPEC-ID `SPEC-PORTFOLIO-CURATE-001`, files to create/modify with absolute paths,
sanitization spec, familybondbot README section, crisp AC referencing JD criteria.

**B3.** Write `docs/portfolio/SPEC-PORTFOLIO-REFACTOR-001.draft.md` containing:
SPEC-ID `SPEC-PORTFOLIO-REFACTOR-001`, aggregated refactor observations,
ranked by blockers > structural > cosmetic, grouped into dispatchable units (≤4 hrs each).

---

## Deliverables

- Write `docs/portfolio/1000bulbs-nugget-hunt-recommendation.md` — portfolio recommendation report for Q88N
- Write `docs/portfolio/SPEC-PORTFOLIO-CURATE-001.draft.md` — follow-on curation spec for factory dispatch
- Write `docs/portfolio/SPEC-PORTFOLIO-REFACTOR-001.draft.md` — follow-on refactor spec for factory dispatch

---

## Acceptance Criteria

**AC-1: Research phase completes**
- [ ] Read `docs/portfolio/1000bulbs-portfolio-audit.md` for prior audit context
- [ ] Read `docs/portfolio/1000bulbs-teaser-README.draft.md` for prior draft
- [ ] Read `.deia/BOOT.md` for hive operating rules
- [ ] Read `CLAUDE.md` for repo conventions
- [ ] Survey `hivenode/main.py` for API routes and architecture patterns
- [ ] Survey `hivenode/routes/` directory for route definitions
- [ ] Survey `hivenode/relay/` directory for relay architecture
- [ ] Survey `hivenode/ledger/` directory for ledger implementation
- [ ] Survey `hivenode/wiki/` directory for wiki subsystem
- [ ] Survey `hivenode/inventory/` directory for inventory management
- [ ] Survey `hivenode/shell/` directory for shell interface
- [ ] Survey `simdecisions/des/` directory for simulation engine
- [ ] Survey `simdecisions/optimization/` directory for optimization module
- [ ] Survey `simdecisions/phase_ir/` directory for Phase-IR standard
- [ ] Survey `simdecisions/flows/` directory for flow definitions
- [ ] Read `simdecisions/database.py` for persistence layer
- [ ] Survey `browser/src/App.tsx` for React entry point
- [ ] Survey `browser/src/shell/` directory for shell components
- [ ] Survey `browser/src/primitives/` directory for UI primitives
- [ ] Survey `browser/src/sets/` directory for set loader system
- [ ] Read `browser/vite.config.ts` for build configuration
- [ ] Survey `hodeia_auth/main.py` for auth service architecture
- [ ] Read `pyproject.toml` for 12-factor evidence
- [ ] Read `Dockerfile` for containerization
- [ ] Read `railway.toml` for Railway deployment config
- [ ] Read `vercel.json` for Vercel deployment config
- [ ] Survey `.deia/BOOT.md` for orchestration evidence
- [ ] Survey `.deia/HIVE.md` for chain of command documentation
- [ ] Survey `.deia/processes/` for AI correction processes
- [ ] Read `.deia/config/ethics.yml` for ethics configuration
- [ ] Read `.deia/config/carbon.yml` for carbon tracking config
- [ ] Survey `hivenode/scheduler/scheduler_daemon.py` for scheduling logic
- [ ] Survey `hivenode/scheduler/dispatcher_daemon.py` for dispatch logic
- [ ] Survey `hivenode/scheduler/triage_daemon.py` for triage logic
- [ ] Count specs in `.deia/hive/queue/_done/` and sample 5-10 for diversity
- [ ] Count rejections in `.deia/hive/queue/_escalated/`
- [ ] Run `git log --oneline -100` — find 5-10 AI correction examples
- [ ] Survey `_tools/inventory.py` for feature tracking patterns
- [ ] Survey `_tools/ir_density.py` for spec quality scoring
- [ ] Survey `tests/hivenode/` for test structure and coverage
- [ ] Survey `tests/simdecisions/` for test structure and coverage
- [ ] Probe `https://hodeia.me/health` — record HTTP status code
- [ ] Probe `https://hodeia.me/jwks.json` — record HTTP status code
- [ ] Probe Vercel frontend URL — record HTTP status and render state
- [ ] Probe Railway hivenode URL — record HTTP status code
- [ ] Survey familybondbot repo for structure, README, features, code quality
**AC-2: Recommendation report produced**
- [ ] Write `docs/portfolio/1000bulbs-nugget-hunt-recommendation.md`
- [ ] Report contains top 10-15 nuggets ranked by signal x effort
- [ ] Report contains JD signal coverage matrix (≥2 nuggets per criterion)
- [ ] Report contains deployment truth table (live vs not)
- [ ] Report contains 5-minute story arc narrative
- [ ] Report contains familybondbot assessment
- [ ] Report contains recommended showcase format (one choice, justified)
- [ ] Report contains cost-benefit table (hours-to-ship per nugget)
- [ ] Report contains 3-5 Q88N decisions needed
**AC-3: Portfolio curation spec produced**
- [ ] Write `docs/portfolio/SPEC-PORTFOLIO-CURATE-001.draft.md`
- [ ] Spec lists files to create/modify with absolute paths
- [ ] Spec specifies sanitization needed (secrets, internal paths)
- [ ] Spec includes familybondbot README section if recommended
- [ ] Spec has crisp acceptance criteria referencing JD criteria
**AC-4: Refactor spec produced**
- [ ] Write `docs/portfolio/SPEC-PORTFOLIO-REFACTOR-001.draft.md`
- [ ] Spec aggregates all refactor observations from research
- [ ] Spec ranks by: blockers > structural > cosmetic
- [ ] Spec groups into dispatchable work units (≤4 hrs each)
- [ ] Each unit lists files, changes, JD signal strengthened, AC

---

## Smoke Test

- [ ] File `docs/portfolio/1000bulbs-nugget-hunt-recommendation.md` exists and is >200 lines
- [ ] File `docs/portfolio/SPEC-PORTFOLIO-CURATE-001.draft.md` exists and contains `## Acceptance Criteria`
- [ ] File `docs/portfolio/SPEC-PORTFOLIO-REFACTOR-001.draft.md` exists and contains `## Acceptance Criteria`
- [ ] Recommendation report contains text "JD signal coverage"
- [ ] Recommendation report contains text "deployment truth table"
- [ ] No familybondbot product URLs appear in any output file
- [ ] No reference to `federalist-papers-ai` in any output file

---

## Constraints

- Curation = saying no. Do NOT propose >15 total nuggets.
- No overclaiming. If `https://hodeia.me` login is broken, say so.
- No `federalist-papers-ai`. Excluded, do not reference.
- familybondbot: no URL. Refer to it as "a full-stack consumer Discord bot with multiple seasons of live usage."
- Time is a goal, not a hard limit.

---

**END OF SPEC**
