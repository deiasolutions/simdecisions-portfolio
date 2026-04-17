# SimDecisions Portfolio — Quick Start

**Author:** Dave Eichler
**LinkedIn:** [linkedin.com/in/daaaave-atx](https://linkedin.com/in/daaaave-atx)
**GitHub:** [DAAAAVE-ATX](https://github.com/DAAAAVE-ATX)

---

## What Is This?

This is a **public portfolio mirror** of the simdecisions monorepo. All directory structures, file names, and architectural patterns are preserved exactly. Source files are represented as **descriptive stubs** (not actual source code).

---

## Quick Navigation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Overview, directory structure, working systems, hive explanation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 5 Mermaid diagrams with plain-English explanations |
| [llms.txt](llms.txt) | Machine-readable summary for AI crawlers |
| [metadata.json](metadata.json) | Schema.org markup |

---

## Key Directories

| Directory | Contents |
|-----------|----------|
| `hivenode/` | FastAPI backend (847 Python stubs) |
| `simdecisions/` | DES engine, Phase-IR, optimization (Python stubs) |
| `browser/` | React frontend (1014 TypeScript stubs) |
| `hodeia_auth/` | Auth service (Python stubs) |
| `_tools/` | Dev tooling: inventory CLI, estimates, etc. |
| `tests/` | Test suite mirroring source tree |
| `docs/` | Specs, ADRs, architecture docs (copied verbatim) |
| `.deia/` | Hive coordination files (queue, tasks, responses) |

---

## What Are "Stubs"?

Each Python and TypeScript source file is replaced with a **stub** that includes:

- Original docstring or inferred purpose (extracted from reading the actual file)
- Import list (first 10 imports)
- Class names with one-sentence descriptions
- Function signatures with one-sentence descriptions
- Footer: "SOURCE AVAILABLE ON REQUEST — Contact: Dave Eichler"

**Example Python stub:**
```python
"""
main
====

Hivenode FastAPI application.

Dependencies:
- import asyncio
- import logging
- from fastapi import FastAPI

Functions:
- _find_repo_root(): Find git repository root by walking up from hivenode directory.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
```

---

## Working Systems (Evidence-Based)

| System | Status | Evidence |
|--------|--------|----------|
| Factory Loop (scheduler + dispatcher + queue runner) | ✅ Operational | 17+ specs processed, auto-commit working |
| DES Engine | ✅ Operational | Tests passing, checkpoints working |
| Phase-IR Loader | ✅ Operational | Tests passing, flow validation working |
| Hive Coordination | ✅ Operational | Task dispatch, response collection, archival |
| Build Monitor | ✅ Operational | Live on simdecisions.com |
| Event Ledger | ✅ Operational | Append-only event log, writer + reader |
| Volume Registry (home://, cloud://, etc.) | ✅ Operational | File transport working |

---

## Architecture Highlights

### 5-Tier Stack
1. **View:** React components (browser/src/primitives/, browser/src/apps/)
2. **API:** FastAPI routes (hivenode/routes/)
3. **Service:** Business logic (hivenode/scheduler/, hivenode/inventory/)
4. **Persistence:** SQLAlchemy stores (hivenode/ledger/, hivenode/inventory/store.py)
5. **Database:** PostgreSQL (Railway cloud), SQLite (local edge)

### Hive System (AI Agent Coordination)
- **Q88N (Dave):** Human sovereign — sets direction, approves plans
- **Q33NR (Queen Regent):** Live session — writes briefings, reviews task files, reports results. **Does NOT write code.**
- **Q33N (Queen Coordinator):** Headless — reads briefings, writes task files, dispatches bees. **Does NOT write code unless approved.**
- **BEEs (Workers):** Headless — write code, run tests, write response files. **Do NOT orchestrate.**

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed Mermaid diagrams.

---

## Technology Stack

**Frontend:**
- React 18+
- Vite
- TypeScript
- Custom pane-based shell

**Backend:**
- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL (Railway) / SQLite (local)

**Deployment:**
- Vercel (frontend)
- Railway (backend: hivenode + hodeia-auth)
- JWT auth via hodeia.me (cross-app SSO)

---

## Source Code Access

All files in this portfolio are **stubs**. To request full source code:

**Dave Eichler**
LinkedIn: [linkedin.com/in/daaaave-atx](https://linkedin.com/in/daaaave-atx)
GitHub: [DAAAAVE-ATX](https://github.com/DAAAAVE-ATX)

---

## Statistics

- **Python stubs:** 847
- **TypeScript stubs:** 1014
- **INDEX.md files:** 363 (one per directory)
- **Configuration files:** Copied verbatim (secrets scrubbed)
- **Documentation:** ARCHITECTURE.md, README.md, llms.txt, metadata.json

---

**Generated:** 2026-04-17
**Repository:** [github.com/DAAAAVE-ATX/simdecisions-portfolio](https://github.com/DAAAAVE-ATX/simdecisions-portfolio)
