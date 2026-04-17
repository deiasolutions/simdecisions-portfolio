# SPEC-FACTORY-009: Hivenode Service Supervision

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-009
**Created:** 2026-04-09
**Author:** Q88N
**Type:** INFRASTRUCTURE
**Status:** READY
**Wave:** 1 (parallel with other Wave 1)

---

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Purpose

Create a robust service supervision layer for the 5 hivenode services. Services must auto-restart on crash, report health, and alert when degraded. The factory must keep running 24/7 on Dave's always-on PC.

**The 5 Services:**
1. **hivenode API** (port 8420) — FastAPI server, REST endpoints
2. **MCP server** (port 8421) — Model Context Protocol tools
3. **Queue runner** — Dispatches tasks to bees
4. **File watcher** — Monitors task/response directories
5. **SSE stream** — Real-time events to browser

**Deliverable:** PM2/systemd configs + health monitor + alerting (~300 lines total)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   PM2 Process Manager                │
├─────────────────────────────────────────────────────┤
│  hivenode-api     │ hivenode-mcp    │ queue-runner  │
│  port 8420        │ port 8421       │ daemon        │
├───────────────────┼─────────────────┼───────────────┤
│  file-watcher     │ sse-stream      │ health-mon    │
│  watchdog         │ port 8422       │ port 8423     │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Health Monitor       │
              │   - Checks all 5       │
              │   - Alerts on failure  │
              │   - Dashboard endpoint │
              └────────────────────────┘
```

---

## Option A: PM2 (Recommended for Windows + Cross-Platform)

### ecosystem.config.js

```javascript
// hivenode/ecosystem.config.js

module.exports = {
  apps: [
    {
      name: 'hivenode-api',
      script: 'python',
      args: '-m uvicorn main:app --host 0.0.0.0 --port 8420',
      cwd: './hivenode',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 1000,
      env: {
        PYTHONUNBUFFERED: '1',
      },
      error_file: './logs/hivenode-api-error.log',
      out_file: './logs/hivenode-api-out.log',
    },
    {
      name: 'hivenode-mcp',
      script: 'python',
      args: '-m hive_mcp.local_server',
      cwd: './hivenode',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 1000,
      env: {
        MCP_PORT: '8421',
        PYTHONUNBUFFERED: '1',
      },
      error_file: './logs/hivenode-mcp-error.log',
      out_file: './logs/hivenode-mcp-out.log',
    },
    {
      name: 'queue-runner',
      script: 'python',
      args: '-m scripts.queue.run_queue',
      cwd: './.deia/hive',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 5000,  // Longer delay for queue runner
      env: {
        PYTHONUNBUFFERED: '1',
      },
      error_file: './logs/queue-runner-error.log',
      out_file: './logs/queue-runner-out.log',
    },
    {
      name: 'file-watcher',
      script: 'python',
      args: '-m scripts.file_watcher',
      cwd: './.deia/hive',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 1000,
      env: {
        PYTHONUNBUFFERED: '1',
      },
      error_file: './logs/file-watcher-error.log',
      out_file: './logs/file-watcher-out.log',
    },
    {
      name: 'sse-stream',
      script: 'python',
      args: '-m uvicorn sse_server:app --host 0.0.0.0 --port 8422',
      cwd: './hivenode',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 1000,
      env: {
        PYTHONUNBUFFERED: '1',
      },
      error_file: './logs/sse-stream-error.log',
      out_file: './logs/sse-stream-out.log',
    },
    {
      name: 'health-monitor',
      script: 'python',
      args: '-m scripts.health_monitor',
      cwd: './hivenode',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_restarts: 5,
      restart_delay: 10000,
      env: {
        PYTHONUNBUFFERED: '1',
        HEALTH_CHECK_INTERVAL: '30',
        ALERT_WEBHOOK: process.env.ALERT_WEBHOOK || '',
      },
      error_file: './logs/health-monitor-error.log',
      out_file: './logs/health-monitor-out.log',
    },
  ],
};
```

### PM2 Commands

```bash
# Start all services
pm2 start ecosystem.config.js

# View status
pm2 status

# View logs
pm2 logs

# Restart all
pm2 restart all

# Stop all
pm2 stop all

# Save for auto-start on boot
pm2 save
pm2 startup  # Follow instructions for Windows/systemd
```

---

## Health Monitor

### hivenode/scripts/health_monitor.py

```python
"""
Health Monitor — Watches all hivenode services.

Checks every 30s:
- HTTP health endpoints
- Process existence via PM2 API
- Disk space
- Memory usage

Alerts via:
- Console log
- Webhook (Slack/Discord)
- Local notification (optional)
"""

import asyncio
import httpx
import json
import logging
import os
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
ALERT_WEBHOOK = os.getenv("ALERT_WEBHOOK", "")

SERVICES = [
    {
        "name": "hivenode-api",
        "url": "http://localhost:8420/health",
        "critical": True,
    },
    {
        "name": "hivenode-mcp",
        "url": "http://localhost:8421/health",
        "critical": False,  # Factory works without MCP
    },
    {
        "name": "sse-stream",
        "url": "http://localhost:8422/health",
        "critical": False,
    },
    {
        "name": "queue-runner",
        "url": None,  # No HTTP endpoint, check process
        "critical": True,
        "check_type": "process",
    },
    {
        "name": "file-watcher",
        "url": None,
        "critical": False,
        "check_type": "process",
    },
]

# Track consecutive failures
failure_counts = {s["name"]: 0 for s in SERVICES}
ALERT_THRESHOLD = 3  # Alert after 3 consecutive failures


async def check_http_health(service: dict) -> bool:
    """Check HTTP health endpoint."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(service["url"])
            return resp.status_code == 200
    except Exception as e:
        logger.warning(f"{service['name']}: HTTP check failed - {e}")
        return False


async def check_process_health(service: dict) -> bool:
    """Check if process is running via PM2."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "pm2", "jlist",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        processes = json.loads(stdout.decode())
        
        for p in processes:
            if p["name"] == service["name"]:
                return p["pm2_env"]["status"] == "online"
        return False
    except Exception as e:
        logger.warning(f"{service['name']}: Process check failed - {e}")
        return False


async def check_service(service: dict) -> dict:
    """Check a single service."""
    check_type = service.get("check_type", "http")
    
    if check_type == "http":
        healthy = await check_http_health(service)
    else:
        healthy = await check_process_health(service)
    
    # Track failures
    if healthy:
        failure_counts[service["name"]] = 0
    else:
        failure_counts[service["name"]] += 1
    
    return {
        "name": service["name"],
        "healthy": healthy,
        "critical": service["critical"],
        "consecutive_failures": failure_counts[service["name"]],
    }


async def send_alert(message: str, services_down: list):
    """Send alert via webhook."""
    if not ALERT_WEBHOOK:
        logger.warning(f"ALERT (no webhook): {message}")
        return
    
    payload = {
        "text": f"🚨 **Hivenode Alert**\n{message}",
        "services": services_down,
        "timestamp": datetime.now().isoformat(),
    }
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(ALERT_WEBHOOK, json=payload)
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")


async def run_health_checks():
    """Run all health checks."""
    results = await asyncio.gather(*[check_service(s) for s in SERVICES])
    
    # Check for alerts
    critical_down = [r for r in results if not r["healthy"] and r["critical"]]
    non_critical_down = [r for r in results if not r["healthy"] and not r["critical"]]
    
    # Alert on critical failures
    for r in critical_down:
        if r["consecutive_failures"] == ALERT_THRESHOLD:
            await send_alert(
                f"CRITICAL: {r['name']} is down after {ALERT_THRESHOLD} checks",
                [r["name"]]
            )
    
    # Log status
    status_line = " | ".join([
        f"{r['name']}: {'✓' if r['healthy'] else '✗'}"
        for r in results
    ])
    logger.info(f"Health: {status_line}")
    
    return results


async def health_endpoint():
    """Return health status as JSON (for dashboard)."""
    results = await run_health_checks()
    all_critical_up = all(r["healthy"] for r in results if r["critical"])
    
    return {
        "status": "healthy" if all_critical_up else "degraded",
        "services": results,
        "timestamp": datetime.now().isoformat(),
    }


async def main():
    """Main loop."""
    logger.info(f"Health monitor started. Interval: {CHECK_INTERVAL}s")
    
    while True:
        try:
            await run_health_checks()
        except Exception as e:
            logger.error(f"Health check error: {e}")
        
        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Startup Script

### scripts/start-hivenode.ps1 (Windows)

```powershell
# Start all hivenode services via PM2

Write-Host "Starting Hivenode services..." -ForegroundColor Cyan

# Ensure logs directory exists
New-Item -ItemType Directory -Force -Path ".\logs" | Out-Null

# Check PM2 is installed
if (-not (Get-Command pm2 -ErrorAction SilentlyContinue)) {
    Write-Host "PM2 not found. Installing..." -ForegroundColor Yellow
    npm install -g pm2
}

# Start services
pm2 start ecosystem.config.js

# Show status
pm2 status

Write-Host "`nHivenode services started. Use 'pm2 logs' to view logs." -ForegroundColor Green
```

### scripts/start-hivenode.sh (Mac/Linux)

```bash
#!/bin/bash
# Start all hivenode services via PM2

echo "Starting Hivenode services..."

# Ensure logs directory exists
mkdir -p ./logs

# Check PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "PM2 not found. Installing..."
    npm install -g pm2
fi

# Start services
pm2 start ecosystem.config.js

# Show status
pm2 status

echo ""
echo "Hivenode services started. Use 'pm2 logs' to view logs."
```

---

## Dashboard Endpoint

Add to `hivenode/routes/factory_routes.py`:

```python
@router.get("/services")
async def services_status():
    """
    Get status of all hivenode services.
    Used by mobile dashboard and health monitor.
    """
    from ..scripts.health_monitor import health_endpoint
    return await health_endpoint()
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `ecosystem.config.js` | CREATE | ~100 |
| `hivenode/scripts/health_monitor.py` | CREATE | ~150 |
| `scripts/start-hivenode.ps1` | CREATE | ~25 |
| `scripts/start-hivenode.sh` | CREATE | ~20 |
| `hivenode/routes/factory_routes.py` | MODIFY | +10 |

---

## Reference Files

Read before implementation:
- PM2 documentation: https://pm2.keymetrics.io/docs
- Existing hivenode service entry points
- `.deia/hive/scripts/queue/run_queue.py`
- `hivenode/hive_mcp/local_server.py`

---

## Acceptance Criteria

- [ ] `ecosystem.config.js` defines all 5 services + health monitor
- [ ] `pm2 start ecosystem.config.js` starts all services
- [ ] Services auto-restart on crash (verify by killing one)
- [ ] Health monitor checks all services every 30s
- [ ] Alert sent after 3 consecutive failures (if webhook configured)
- [ ] `/factory/services` returns all service statuses
- [ ] Logs written to `./logs/` directory
- [ ] `pm2 startup` configures auto-start on boot
- [ ] Works on Windows (Dave's always-on PC)

## Smoke Test

```bash
# Start all services
pm2 start ecosystem.config.js
pm2 status

# Check health endpoint
curl http://localhost:8420/factory/services | jq

# Kill a service, verify restart
pm2 stop hivenode-mcp
sleep 5
pm2 status  # Should show restarting

# Check logs
pm2 logs hivenode-api --lines 20

# Verify auto-start setup
pm2 save
pm2 startup
```

## Constraints

- Must work on Windows (Dave's PC)
- PM2 preferred over systemd for cross-platform
- Health checks must not overwhelm services
- Alerts only after threshold (no spam)
- Logs rotated (PM2 handles this)

## Response File

`.deia/hive/responses/20260409-FACTORY-009-RESPONSE.md`

---

*SPEC-FACTORY-009 — Q88N — 2026-04-09*
