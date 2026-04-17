# SPEC: Repoint Vercel + Railway to ShiftCenter Repo

## Priority
P1

## Objective
Repoint existing Vercel project to shiftcenter/browser/ and Railway service to shiftcenter/hivenode/. Set up dev.shiftcenter.com as dev branch preview.

## Context
Files to read first:
- `docs/DEPLOYMENT-WIRING-NOTES.md`
- `.deia/config/deployment-env.md`
- `browser/vite.config.ts`
- `hivenode/main.py`
- `pyproject.toml`

Old deploy: Vercel from simdecisions-2/, Railway from simdecisions-2/api/
New deploy: Vercel from browser/, Railway from hivenode/

## Acceptance Criteria
- [ ] Vercel project linked to deiasolutions/shiftcenter, root dir browser/
- [ ] Production branch: main. Preview: dev + PR branches.
- [ ] vercel.json in browser/ with SPA fallback rewrites
- [ ] Railway service linked to deiasolutions/shiftcenter, root dir hivenode/
- [ ] Start command: uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT
- [ ] Env vars set per .deia/config/deployment-env.md
- [ ] Health check: GET /health returns 200
- [ ] Do NOT delete old Vercel/Railway projects
- [ ] Do NOT change production DNS yet

## Smoke Test
- [ ] Push to dev -> Vercel builds
- [ ] Push to dev -> Railway builds
- [ ] Staging URL loads chat app in browser
- [ ] Staging API /health returns 200

## Model Assignment
sonnet
