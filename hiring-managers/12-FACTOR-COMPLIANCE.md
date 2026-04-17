# 12-Factor Compliance

Verified against actual codebase files.

| # | Factor | Requirement | Evidence | File |
|---|--------|-------------|----------|------|
| I | Codebase | One codebase, many deploys | Single repo → Railway + Vercel | `railway.toml`, `vercel.json` |
| II | Dependencies | Explicitly declare and isolate | All deps in manifest | `pyproject.toml`, `package.json` |
| III | Config | Store config in environment | Env vars, no hardcoded secrets | `hivenode/config.py`, `railway.toml` |
| IV | Backing Services | Treat as attached resources | PostgreSQL via connection string | `DATABASE_URL` env var |
| V | Build, Release, Run | Strictly separate stages | Dockerfile build, Railway release, container run | `Dockerfile` |
| VI | Processes | Execute as stateless processes | No local state; all state in PostgreSQL | `hivenode/` design |
| VII | Port Binding | Export services via port binding | FastAPI binds `$PORT` | `hivenode/main.py` |
| VIII | Concurrency | Scale out via process model | Separate scheduler/dispatcher/triage processes | `_tools/restart-services.sh` |
| IX | Disposability | Maximize robustness with fast startup/shutdown | Health checks, graceful shutdown | `/health` endpoint |
| X | Dev/Prod Parity | Keep development and production similar | Same Dockerfile everywhere | `Dockerfile` |
| XI | Logs | Treat logs as event streams | Structured logging to stdout | `hivenode/` logging config |
| XII | Admin Processes | Run admin tasks as one-off processes | `_tools/` scripts | `_tools/*.py` |

---

**All 12 factors verified against actual files in the repository.**
