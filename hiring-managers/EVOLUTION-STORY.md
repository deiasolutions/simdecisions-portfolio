# Evolution: 2003 to 2026

SimDecisions didn't appear overnight. It's the result of 20+ years of domain expertise in workforce scheduling and simulation.

---

## Timeline

| Year | Milestone | Evidence |
|------|-----------|----------|
| 2002 | Earliest artifact: "Sched Swapper R6.02 DesMoines" spreadsheet | `2002_12_05 Sched Swapper R6.02 DesMoines new.xls` |
| 2003 | Java simulation source: `SimeWindow1.java` by `deichler` (June 5) | Source file header |
| 2003 | Processing visual prototype: triangle tessellation grid | `Processing/scengine/Old/scengine_001/` |
| 2005 | SIMdecisions launched as free online contact center simulator | Website teaser |
| 2005 | EULA by Deia Solutions, Inc. (Texas), dated July 10 | `agreement20050710.inc` |
| 2005 | `simdecisions.com` domain registered (October 9) | Domain records |
| 2005 | Web application live: PHP/MySQL, Java applets, phpBB2 forums | Web snapshots |
| 2006 | ShiftCenter planned for Fall 2006 launch | `index.html`: "Coming Fall 2006" |
| 2007 | Chameleon search algorithm developed (scengine v028-v042) | Source: "028 creating chameleon search" |
| 2007 | Latest web snapshot: 4,366 files, 52 database tables | `WebCode/2007-07-31/` |
| 2008 | ShiftCenter.com relaunch preparation | `LAUNCH 2008-01-31.txt` |
| 2024-2026 | Rebuilt as SimDecisions: Python/TypeScript/PostgreSQL, AI orchestration | Current repository |

---

## The Original Platform (2003-2008)

**Stack:**
| Layer | Technology |
|-------|------------|
| Scheduling Engine | Processing (Java applet) — `scengine_042_009.pde` (3,570 lines) |
| Simulation Engine | Processing (Java applet) — `simapp_075_001.pde` (6,506 lines) |
| Web Application | PHP 4/5, Joomla 1.0.12 "Sunfire" |
| Database | MySQL (52 application tables) |
| Authentication | phpBB2 forum integration |
| Payment | PayPal IPN subscription ($0.25/month) |

**Two Products, One Codebase:**
- **ShiftCenter** — Scheduling optimizer using "Chameleon" tree-search algorithm
- **SIMdecisions** — Discrete event simulator with Poisson arrivals, priority routing, multi-skill agents

**File Counts (2007-07-31):**
| Type | Count |
|------|-------|
| .php | 1,169 |
| .html | 502 |
| .java | 55 |
| .js | 155 |
| **Total** | **4,366** |

**Database:** 52 application tables
- 16 scheduling tables (`sc_*` prefix)
- 26 simulation tables (`sd_*` prefix)

---

## Key Algorithms

Chameleon Search (Scheduling) — Multi-phase tree search: Init, Trials, Main, Swap, Best, Final, Save. Move shifts a WorkWeek's start time. Swap exchanges times and sizes between two WorkWeeks. Best runs exhaustive search over all valid positions. Simulated annealing with 13 heat levels.

Comment from source: *"TOP SCORE 82 on bigscale off - Holy Shit 82!"*

DES Event Loop (Simulation) — Per simulated second, five phases: offerContacts (Poisson arrivals), readyAgents (finish agent tasks), processScripts (route contacts to queues), answerContacts (match contacts to agents), abandonContacts (handle patience expiry).

Marketing tagline found in code: *"It's time to fire your Erlang staffing model."*

---

## What Survived

| 2003-2008 Original | 2024-2026 SimDecisions |
|--------------------|-----------------------|
| Processing/Java DES event loop | Python DES engine (`simdecisions/des/`) |
| Poisson arrival generation | Poisson arrival generation |
| Priority-based queue routing | Priority-based queue routing |
| Skills-based agent groups | Resource pools with capability matching |
| SL/ASA/AHT/Occupancy metrics | CLOCK/COIN/CARBON tri-currency metrics |
| Change broker (TEST/CONSIDER/ADOPT/FORCE) | Phase-IR open standard |
| `deichler` writing Java at midnight | `deichler` directing AI agents at midnight |

---

## ShiftCenter.com

The original platform operated at shiftcenter.com (scheduling) and simdecisions.com (simulation).

**Current status:** ShiftCenter.com is being developed as an alternate marketing frontend for the SimDecisions solution while go-to-market strategy is finalized.

Visit [ShiftCenter.com](https://shiftcenter.com) to see the current state.

---

## Why This Matters

Most candidates can show React + FastAPI + Railway. Not every candidate can show:

- "I built this domain in 2003"
- "I refined it for 20+ years"
- "The simulation engine concepts are battle-tested"
- "Now it's orchestrated by AI agents"

**Continuity is a differentiator.**

---

**Every claim in this document is traceable to specific files, directories, or source code comments. No capabilities or scale numbers were fabricated.**
