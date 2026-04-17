# SPEC-CAP-01: Unified Bee Capacity from queue.yml

**Priority:** P1
**Complexity:** Haiku
**Estimate:** 30 minutes
**Dependencies:** None

---

## Problem

Bee capacity (max concurrent bees) is defined in multiple places. Three of four consumers now read from `queue.yml`, but the dispatcher daemon still uses a hardcoded CLI default of 10:

| Consumer | Source | Reads queue.yml? |
|----------|--------|-------------------|
| Queue runner (`run_queue.py`) | `config["budget"]["max_parallel_bees"]` | YES |
| Scheduler (`scheduler_daemon.py`) | `load_bee_constraints()` | YES |
| Build monitor (`build_monitor.py`) | `_load_capacity()` | YES |
| **Dispatcher (`dispatcher_daemon.py`)** | **`--max-bees 10` CLI arg** | **NO** |

If you change `queue.yml` to 15 bees, the dispatcher still calculates available slots based on 10.

## Solution

Make the dispatcher read `max_parallel_bees` from `queue.yml`, same as the other three consumers. The CLI `--max-bees` arg becomes an override (if provided and not the default, use CLI value; otherwise read queue.yml).

---

## Implementation

### 1. Add queue.yml reader to dispatcher_daemon.py

In `dispatcher_daemon.py`, add a function (or reuse the scheduler's pattern):

```python
def _load_max_bees_from_config(queue_dir: Path) -> int:
    """Read max_parallel_bees from queue.yml. Default 10."""
    try:
        config_path = queue_dir.parent.parent / "config" / "queue.yml"
        if not config_path.exists():
            # Try relative to project root
            config_path = Path(".deia/config/queue.yml")
        config = yaml.safe_load(config_path.read_text())
        value = config.get("budget", {}).get("max_parallel_bees", 10)
        return max(1, min(20, int(value)))
    except Exception:
        return 10
```

### 2. Update DispatcherDaemon.__init__

In `__init__`, if `max_bees` is the default (10), re-read from queue.yml:

```python
def __init__(self, max_bees: int = 10, ...):
    config_max = _load_max_bees_from_config(queue_dir)
    # CLI override wins only if explicitly set (not default)
    self.max_bees = max_bees if max_bees != 10 else config_max
```

### 3. Re-read on each cycle (hot reload)

In the dispatcher's main loop (`_run_cycle`), re-read queue.yml so changes take effect within 30 seconds:

```python
def _run_cycle(self):
    # Hot-reload capacity from queue.yml
    self.max_bees = _load_max_bees_from_config(self.queue_dir)
    ...
```

This matches the scheduler's pattern — it also re-reads queue.yml every cycle.

## Files to Read First

- `hivenode/scheduler/dispatcher_daemon.py`
- `hivenode/scheduler/scheduler_daemon.py`
- `.deia/config/queue.yml`

## Files to Modify

| File | Change |
|------|--------|
| `hivenode/scheduler/dispatcher_daemon.py` | Add `_load_max_bees_from_config()`, update `__init__` and `_run_cycle` |

## Acceptance Criteria

- [ ] Dispatcher reads `max_parallel_bees` from `.deia/config/queue.yml`
- [ ] CLI `--max-bees` overrides queue.yml when explicitly provided (not default)
- [ ] Dispatcher re-reads queue.yml on each cycle (hot reload)
- [ ] If queue.yml is missing or malformed, defaults to 10
- [ ] Value clamped to 1-20 range
- [ ] Existing `--max-bees` CLI arg still works as override
- [ ] No changes to scheduler, queue runner, or build monitor

## Smoke Test

- [ ] Start dispatcher without `--max-bees` flag → uses queue.yml value
- [ ] Start dispatcher with `--max-bees 5` → uses 5 (CLI override)
- [ ] Change queue.yml `max_parallel_bees` while dispatcher is running → next cycle uses new value
- [ ] Delete queue.yml → dispatcher falls back to 10

## Model Assignment

haiku

## Constraints

- Do NOT modify scheduler_daemon.py, run_queue.py, or build_monitor.py
- Do NOT add new dependencies
- Pattern should match scheduler's `load_bee_constraints()` approach
- `import yaml` is already available in the dispatcher module
