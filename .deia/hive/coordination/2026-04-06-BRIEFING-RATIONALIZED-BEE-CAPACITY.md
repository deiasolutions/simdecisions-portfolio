# BRIEFING: Rationalized Bee Capacity Configuration

**From:** Q33NR
**To:** Q88N / Mr. AI
**Date:** 2026-04-06
**Priority:** P2

## Problem

Bee capacity (max concurrent bees) is defined in 3 places with no single source of truth:

| Location | Field | Value | Purpose |
|----------|-------|-------|---------|
| `.deia/config/queue.yml` | `budget.max_parallel_bees` | 10 | **Actual enforcement** — queue runner ThreadPoolExecutor cap |
| `.deia/hive/schedule.json` | `constraints.max_bees` | 10 | OR-Tools solver planning — not enforced at runtime |
| `hivenode/routes/build_monitor.py` | `slot_capacity` | 10 | Display only — shows available slots in UI |

If you change `queue.yml` to 15, the scheduler still plans for 10 and the build monitor still shows 10 slots. If you change `schedule.json`, the queue runner still caps at 10. No single knob controls all three.

## Current Data Flow

```
queue.yml (max_parallel_bees: 10)
    │
    └──► run_queue.py reads at startup
         └──► queue_pool.py ThreadPoolExecutor(max_workers=10)
              └──► ACTUAL ENFORCEMENT

schedule.json (max_bees: 10)
    │
    └──► scheduler_daemon.py reads at startup
         └──► OR-Tools solver constraint (planning only)

build_monitor.py (slot_capacity = 10)
    │
    └──► Hardcoded class attribute
         └──► Display in /build/claims endpoint
```

## Proposed Solution

### Single Source: `queue.yml`

`queue.yml` is already the operational config file. Make everything read from it:

```yaml
# .deia/config/queue.yml
budget:
  max_parallel_bees: 10    # <-- THE number. Everything reads this.
  min_parallel_bees: 5     # <-- Floor for scheduler solver
```

### Consumers

**1. Queue Runner** (already works)
```python
# run_queue.py — no change needed
max_parallel = config["budget"].get("max_parallel_bees", 1)
```

**2. Scheduler Daemon** — read from queue.yml instead of hardcoding
```python
# scheduler_daemon.py — change
import yaml

def _load_bee_constraints(self):
    config_path = Path(".deia/config/queue.yml")
    config = yaml.safe_load(config_path.read_text())
    self.max_bees = config["budget"].get("max_parallel_bees", 10)
    self.min_bees = config["budget"].get("min_parallel_bees", 5)
```

Then feed `self.max_bees` / `self.min_bees` to the OR-Tools solver instead of the current hardcoded values.

**3. Build Monitor** — read from queue.yml at startup
```python
# build_monitor.py — change
class BuildState:
    def __init__(self, ...):
        self.slot_capacity = self._load_capacity()

    @staticmethod
    def _load_capacity() -> int:
        try:
            config = yaml.safe_load(Path(".deia/config/queue.yml").read_text())
            return config["budget"].get("max_parallel_bees", 10)
        except Exception:
            return 10
```

**4. Schedule.json** — scheduler writes it from queue.yml values
```json
{
  "constraints": {
    "min_bees": 5,   // from queue.yml budget.min_parallel_bees
    "max_bees": 10   // from queue.yml budget.max_parallel_bees
  }
}
```

### Hot Reload (Optional, Phase 2)

The queue runner already has hot-reload for queue.yml (`test_run_queue_hot_reload.py` exists). Extend to:
- Scheduler: re-read queue.yml on every daemon cycle (already runs every 30s)
- Build monitor: re-read on `/build/status` calls (cheap — one YAML parse per 5s poll)

This means changing `max_parallel_bees` in queue.yml takes effect within 30 seconds across the entire pipeline, no restarts needed.

### Migration

1. Add `min_parallel_bees: 5` to queue.yml (new field, default 5)
2. Modify scheduler_daemon.py to read from queue.yml
3. Modify build_monitor.py to read from queue.yml
4. Remove hardcoded `slot_capacity = 10` from BuildState
5. Remove hardcoded constraints from schedule.json template

### What Does NOT Change

- queue.yml format (just one new optional field)
- Queue runner behavior (already reads queue.yml)
- Build monitor API shape (slot_capacity still exists, just sourced differently)
- Scheduler solver logic (same constraints, different source)

## Scope

Small task — ~50 lines of code changes across 3 files. No new dependencies. Could be a haiku spec.

## Open Questions

1. Should we add `max_parallel_bees` validation to the scheduler? (Recommendation: yes, clamp to 1-20 range)
2. Should hot-reload be Phase 1 or Phase 2? (Recommendation: Phase 1 for scheduler since it already rescans every 30s, Phase 2 for build monitor)
3. Should the build monitor dashboard (BMON-01) show the configured capacity alongside current utilization? (Recommendation: yes — "8/10 bees" is more useful than just "8 bees")
