# Nightly Build Launch Checklist

**Process:** Q33NR follows this checklist at **4:55 PM** to launch the nightly build at 5:00 PM.

---

## T-5 min (4:55 PM) — Pre-flight

### 1. Verify specs are in backlog

```bash
ls .deia/hive/queue/backlog/SPEC-*.md
```

- [ ] All intended specs are in `backlog/` (not `_stage/`, not `queue/` root)
- [ ] Each spec passes the SUBMISSION-CHECKLIST.md gate:
  - Filename: `SPEC-{ID}-{description}.md`
  - Has `## Priority`, `## Model Assignment`, `## Depends On`, `## Acceptance Criteria`
  - Acceptance criteria use `- [ ]` format (not backticks, not numbered)
- [ ] No specs stuck in `_active/` from previous runs (move back to backlog if so)
- [ ] No orphan specs in `queue/` root (runner will dispatch these immediately)

### 2. Verify queue/ root is empty

```bash
ls .deia/hive/queue/SPEC-*.md 2>/dev/null
```

Queue root must be empty before launch. Any specs here will be dispatched immediately when hivenode starts, bypassing the scheduler.

### 3. Start hivenode (if not running)

```bash
curl -s http://127.0.0.1:8420/health
```

If down:
```bash
cd shiftcenter && python -m uvicorn hivenode.main:app --host 127.0.0.1 --port 8420
```

Verify:
- [ ] `/health` returns `{"status":"ok"}`
- [ ] `/build/queue-runner-status` returns `{"running":true,"embedded":true}`

If queue runner shows `running: false`:
```bash
curl -s -X POST http://127.0.0.1:8420/build/queue-wake
```

### 4. Start scheduler daemon

```bash
cd shiftcenter && python -m hivenode.scheduler.scheduler_daemon
```

Verify:
- [ ] Logs show `Scanned backlog: N specs found`
- [ ] `schedule.json` is written to `.deia/hive/`

### 5. Start dispatcher daemon

```bash
cd shiftcenter && python -m hivenode.scheduler.dispatcher_daemon
```

Verify:
- [ ] Logs show it reading `schedule.json`
- [ ] Specs start moving from `backlog/` to `queue/` root

---

## T-0 (5:00 PM) — Build active

### 6. Verify dispatch is flowing

```bash
curl -s http://127.0.0.1:8420/build/queue-runner-status
curl -s http://127.0.0.1:8420/build/status
```

- [ ] Queue runner: `running: true`
- [ ] Specs appearing in `_active/`
- [ ] Build monitor shows active bees

### 7. Monitor (periodic)

```bash
# Quick status
curl -s http://127.0.0.1:8420/build/status | python -m json.tool

# What's where
ls .deia/hive/queue/backlog/       # waiting
ls .deia/hive/queue/SPEC-*.md      # queued for runner
ls .deia/hive/queue/_active/       # dispatched, in flight
ls .deia/hive/queue/_done/         # completed
```

---

## Post-build — Teardown

### 8. Check results

- [ ] All expected specs in `_done/`
- [ ] No specs stuck in `_active/` (check for zombies)
- [ ] Review bee responses in `.deia/hive/responses/`
- [ ] Session log written: `queue/session-YYYY-MM-DD-HHMM.json`

### 9. Stop services (optional — if not running overnight)

Stop dispatcher and scheduler (Ctrl+C or kill PID). Hivenode can stay up.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Scheduler finds 0 specs | Files not in `backlog/` or not named `SPEC-*.md` | Move to `backlog/`, rename |
| Dispatcher not moving specs | Dispatcher daemon not running | Start `dispatcher_daemon.py` |
| Runner shows `running: false` | Runner thread died | `POST /build/queue-wake` (auto-restarts up to 5x) |
| Spec false-completed | `extract_task_id()` collision | Check task IDs are unique after extraction |
| Spec stuck in `_active/` | Bee died mid-dispatch | Move back to `queue/` root or `backlog/` |

---

**Services summary:**

| Service | Command | Port | Role |
|---------|---------|------|------|
| Hivenode | `python -m uvicorn hivenode.main:app --host 127.0.0.1 --port 8420` | 8420 | Queue runner, API, build monitor |
| Scheduler | `python -m hivenode.scheduler.scheduler_daemon` | — | Scans backlog, writes schedule.json |
| Dispatcher | `python -m hivenode.scheduler.dispatcher_daemon` | — | Moves specs backlog → queue root |
| Vite | `npx vite --host` (from `browser/`) | 5173 | Frontend dev server |
