# Local Development Guide

**Last Updated:** 2026-04-06

---

## Overview

This guide covers local development setup and common workflows for ShiftCenter. For deployment, see [DEPLOYMENT.md](./DEPLOYMENT.md).

---

## Prerequisites

### Required Software

| Tool | Version | Installation |
|------|---------|--------------|
| **Python** | 3.12+ | https://python.org |
| **Node.js** | 18+ | https://nodejs.org |
| **npm** | 9+ | Included with Node.js |
| **Git** | Latest | https://git-scm.com |

### Optional Tools

| Tool | Purpose |
|------|---------|
| **Railway CLI** | Deploy to Railway from command line |
| **Vercel CLI** | Deploy to Vercel from command line |
| **PostgreSQL** | Local database (optional, SQLite used by default) |

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/deiasolutions/shiftcenter.git
cd shiftcenter
```

### 2. Install Dependencies

**Backend (Python):**
```bash
# Install hivenode in editable mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

**Frontend (Node.js):**
```bash
cd browser
npm install
cd ..
```

### 3. Start Development Servers

**Terminal 1: Backend (hivenode)**
```bash
python -m hivenode
# Starts on http://localhost:8420
```

**Terminal 2: Frontend (Vite)**
```bash
cd browser
npm run dev
# Starts on http://localhost:5173
```

**Terminal 3: Scheduler (optional)**
```bash
python hivenode/scheduler/scheduler_daemon.py --mcp-enabled
# MCP server on port 8422
```

**Terminal 4: Dispatcher (optional)**
```bash
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
# MCP server on port 8423
```

### 4. Access Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8420
- **API Health:** http://localhost:8420/health
- **API Docs:** http://localhost:8420/docs (FastAPI auto-generated)

---

## MCP Queue Notifications

### Running with MCP Enabled (Recommended)

MCP enables real-time queue event notifications for scheduler and dispatcher.

**Terminal 1: Hivenode (includes watcher)**
```bash
python -m hivenode
```

**Terminal 2: Scheduler**
```bash
python hivenode/scheduler/scheduler_daemon.py --mcp-enabled
```

**Terminal 3: Dispatcher**
```bash
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
```

**Expected logs:**
- Hivenode: `Watcher started on .deia/hive/queue/`
- Scheduler: `MCP server started on port 8422`
- Dispatcher: `MCP server started on port 8423`

### Testing MCP Events Manually

**1. Move a spec to _done/**
```bash
# Create a test spec
echo "# SPEC-TEST-001" > .deia/hive/queue/_active/SPEC-TEST-001.md

# Move to _done/ (triggers event)
mv .deia/hive/queue/_active/SPEC-TEST-001.md .deia/hive/queue/_done/
```

**2. Check event log**
```bash
tail -f .deia/hive/queue_events.jsonl
```

**Expected output:**
```json
{"event":"queue.spec_done","spec_file":"SPEC-TEST-001.md","task_id":"TEST-001","timestamp":"2026-04-06T12:34:56Z","directory":"_done"}
```

**3. Verify scheduler woke**
```bash
tail -f .deia/hive/schedule_log.jsonl
```

**Expected latency:** <2s from file move to schedule update

**4. Verify dispatcher reacted**
```bash
tail -f .deia/hive/dispatcher_log.jsonl
```

**Expected:** Counter decremented, slots recalculated

### Disabling MCP (for debugging)

To revert to polling-only mode (original behavior):

```bash
# Scheduler with polling (30s interval)
python hivenode/scheduler/scheduler_daemon.py --mcp-enabled=false

# Dispatcher with polling (10s interval)
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled=false
```

**When to disable MCP:**
- Debugging scheduler/dispatcher logic
- Testing fallback polling behavior
- Investigating event delivery issues

---

## Configuration

### Environment Variables (Local)

Create a `.env` file in repo root (optional):

```bash
# Hivenode mode
HIVENODE_MODE=local

# API keys (optional, for AI features)
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=...

# MCP configuration (optional)
MCP_ENABLED=true
SCHEDULER_MCP_PORT=8422
DISPATCHER_MCP_PORT=8423
```

### Port Configuration

| Service | Default Port | Override Variable |
|---------|--------------|-------------------|
| Hivenode | 8420 | `PORT` |
| Vite dev server | 5173 | `--port` flag |
| Scheduler MCP | 8422 | `SCHEDULER_MCP_PORT` |
| Dispatcher MCP | 8423 | `DISPATCHER_MCP_PORT` |

**Change ports:**
```bash
# Hivenode
PORT=9000 python -m hivenode

# Vite
cd browser
npm run dev -- --port 3000
```

---

## Development Workflows

### Running Tests

**Backend tests (pytest):**
```bash
# All tests
pytest

# Specific test file
pytest tests/hivenode/scheduler/test_scheduler_daemon.py

# With coverage
pytest --cov=hivenode --cov-report=html

# Integration tests (slow)
pytest tests/integration/ -v
```

**Frontend tests (vitest):**
```bash
cd browser
npm run test

# Watch mode
npm run test:watch
```

### Code Quality

**Backend linting:**
```bash
# Ruff (linter + formatter)
ruff check .
ruff format .

# Type checking (mypy)
mypy hivenode/
```

**Frontend linting:**
```bash
cd browser
npm run lint

# Auto-fix
npm run lint:fix
```

### Building for Production

**Backend (no build step):**
```bash
# Install production dependencies only
pip install .
```

**Frontend:**
```bash
cd browser
npm run build

# Output: browser/dist/
```

**Verify build:**
```bash
ls browser/dist/*.egg.md
# Should list: apps.egg.md, canvas.egg.md, chat.egg.md, etc.
```

---

## Database

### SQLite (Default)

Hivenode uses SQLite by default for local development. Database file: `.deia/data/hivenode.db`

**Reset database:**
```bash
rm .deia/data/hivenode.db
python -m hivenode
# Database recreated on startup
```

### PostgreSQL (Optional)

To use PostgreSQL locally:

1. **Install PostgreSQL** (https://postgresql.org)
2. **Create database:**
   ```bash
   createdb shiftcenter_dev
   ```
3. **Set environment variable:**
   ```bash
   export DATABASE_URL=postgresql://localhost/shiftcenter_dev
   python -m hivenode
   ```

**Inventory database** (separate):
```bash
export INVENTORY_DATABASE_URL=postgresql://localhost/shiftcenter_inventory
```

---

## Queue Runner

The queue runner watches `.deia/hive/queue/` and dispatches specs to regent bots.

### Start Queue Runner

```bash
python .deia/hive/scripts/queue/run_queue.py --watch
```

**Expected behavior:**
- Watches for `SPEC-*.md` files in queue/
- Dispatches specs using Fibonacci backoff polling
- Moves completed specs to `_done/`
- Triggers MCP events on file moves

### Check Queue Status

```bash
curl http://localhost:8420/build/status | python -m json.tool
```

**Response:**
```json
{
  "active": [
    {
      "task_id": "MW-031",
      "model": "sonnet",
      "status": "in_progress",
      "last_seen": "2026-04-06T12:34:56Z"
    }
  ],
  "queued": 3,
  "completed": 12
}
```

---

## Common Issues

### Port Already in Use

**Symptom:** `Error: Address already in use`

**Fix:**
```bash
# Find process using port 8420
lsof -i :8420

# Kill process
kill -9 <pid>

# Or use different port
PORT=9000 python -m hivenode
```

### MCP Events Not Delivered

**Symptom:** Scheduler not waking on spec completion

**Diagnosis:**
```bash
# Check MCP server health
curl http://localhost:8422/health

# Check event log
tail -n 20 .deia/hive/queue_events.jsonl

# Check scheduler logs
tail -f .deia/hive/schedule_log.jsonl
```

**Fix:**
- Restart hivenode (watcher may have crashed)
- Restart scheduler/dispatcher
- Disable MCP temporarily: `--mcp-enabled=false`

### Frontend Not Loading EGG Files

**Symptom:** `404 Not Found` for `*.egg.md` files

**Diagnosis:**
```bash
# Check EGG files exist
ls eggs/*.egg.md

# Check Vite server logs for plugin errors
```

**Fix:**
- Verify `serveEggs()` plugin in `browser/vite.config.ts`
- Restart Vite dev server
- Clear Vite cache: `rm -rf browser/node_modules/.vite`

### Database Migration Errors

**Symptom:** `Table does not exist` errors

**Fix:**
```bash
# Reset SQLite database
rm .deia/data/hivenode.db
python -m hivenode

# Or run migrations manually (if migration scripts exist)
alembic upgrade head
```

---

## Useful Commands

### Inventory Management

```bash
# Show feature inventory stats
python _tools/inventory.py stats

# Add to backlog
python _tools/inventory.py backlog add --id BL-XXX --title "..." --category enhancement --priority P1 --source Q88N-direct --notes "Size: M. ..."

# Export inventory to markdown
python _tools/inventory.py export-md
```

### Deployment Testing

```bash
# Test Railway start command locally
python -m hivenode

# Test Vercel build locally
cd browser && npm run build

# Deploy to staging (Vercel)
cd browser && vercel --prod=false

# Deploy to staging (Railway)
railway up
```

---

## References

- **Deployment Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Process Library:** `.deia/processes/PROCESS-LIBRARY-V2.md`
- **Scheduler Process:** `.deia/processes/P-SCHEDULER.md`
- **Dispatcher Process:** `.deia/processes/P-DISPATCHER.md`
- **MCP Design:** `.deia/specs/SPEC-MCP-QUEUE-NOTIFICATIONS.md`

---

**END OF LOCAL DEV GUIDE**
