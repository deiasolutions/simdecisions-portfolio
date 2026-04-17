# TASK: BUG-045 — Kill orphaned child node.exe processes after bee finishes

**Date:** 2026-03-18
**Priority:** P0
**Component:** hive/dispatch

---

## Problem

When `dispatch.py` dispatches a bee via `ClaudeCodeCLIAdapter`, the bee spawns child processes (e.g., `vitest`, `vite`, `node` subprocesses). When the bee finishes, `adapter.stop_session()` kills the Claude Code process but **does not kill its child process tree**. Result: orphaned node.exe processes accumulate, each consuming 1-7 GB RAM.

This is a **production-critical memory leak** on the Q88N workstation. 5+ orphaned vitest processes were found consuming 10+ GB total.

## Root Cause

In `dispatch.py` line 346, `adapter.stop_session()` is called, but there is no follow-up to kill child processes spawned by the Claude Code session. The adapter itself (`ClaudeCodeCLIAdapter`) also does not perform child process tree cleanup.

## Fix Required

### 1. In `dispatch.py` — after `adapter.stop_session()` (around line 346)

Add a child process tree kill using `psutil`:

```python
# After adapter.stop_session()
_kill_child_processes(adapter)
```

Add this function to dispatch.py:

```python
def _kill_child_processes(adapter):
    """Kill any orphaned child processes from the adapter's session."""
    try:
        import psutil
    except ImportError:
        print("[DISPATCH] WARNING: psutil not installed, cannot clean up child processes")
        return

    pid = getattr(adapter, '_process_pid', None) or getattr(adapter, 'pid', None)
    if not pid:
        # Fallback: find node.exe processes that started after dispatch and match patterns
        return

    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        print(f"[DISPATCH] Cleaned up {len(children)} child processes")
    except psutil.NoSuchProcess:
        pass
```

### 2. In `ClaudeCodeCLIAdapter` — track the subprocess PID

The adapter spawns Claude Code via subprocess. It must expose the PID so dispatch.py can find and kill children. Check if the adapter already stores this (look at `self._process` or similar). If not, add it.

### 3. Alternative approach if PID tracking isn't feasible

If the adapter doesn't expose the subprocess PID, use a before/after snapshot approach:

```python
def _snapshot_node_pids():
    """Return set of all node.exe PIDs."""
    import psutil
    return {p.pid for p in psutil.process_iter(['name']) if p.info['name'] == 'node.exe'}

# In dispatch_bee():
before_pids = _snapshot_node_pids()
result = adapter.send_task(task_content, timeout=timeout)
adapter.stop_session()
after_pids = _snapshot_node_pids()
orphans = after_pids - before_pids
for pid in orphans:
    try:
        psutil.Process(pid).kill()
    except:
        pass
```

## Files to Read

- `.deia/hive/scripts/dispatch/dispatch.py` — the dispatch script (438 lines)
- `hivenode/adapters/cli/claude_code_cli_adapter.py` — the adapter that spawns Claude Code

## Files to Modify

- `.deia/hive/scripts/dispatch/dispatch.py` — add cleanup after line 346
- `hivenode/adapters/cli/claude_code_cli_adapter.py` — expose subprocess PID if not already

## Acceptance Criteria

- [ ] After a bee completes, ALL child node.exe processes spawned during that session are killed
- [ ] No orphaned vitest/vite/node processes survive after dispatch completes
- [ ] Cleanup is best-effort (never crashes dispatch on failure)
- [ ] psutil is used (already in requirements or add it)
- [ ] Tests: at least 3 tests verifying cleanup logic
- [ ] Works on Windows (the production environment)

## Test Plan

1. Mock psutil.Process and verify children().kill() is called
2. Test fallback when psutil is not installed (warning, no crash)
3. Test snapshot approach (before/after PID diff)
4. Test that NoSuchProcess exceptions are silently caught
