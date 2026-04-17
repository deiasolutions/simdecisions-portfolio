# TASK-040: 8os Remaining CLI Commands

**Role:** BEE (coder)
**Model:** Sonnet
**Parent:** SPEC-HIVENODE-E2E-001 Wave 4
**Spec section:** 2.1 (remaining commands)
**Date:** 2026-03-12
**Estimated tests:** ~10

---

## Objective

Wire the remaining 8os CLI commands that aren't yet implemented. Complete the CLI tool with queue, dispatch, indexing, inventory, volumes, and node management commands.

**This is backend-only Python work. No browser changes.**

---

## What Already Exists

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`

**Existing commands:**

- `8os up` — start local hivenode
- `8os down` — stop local hivenode
- `8os status` — show hivenode status
- `8os sync` — trigger sync cycle
- `8os sync --status` — show sync status

**Infrastructure:**

- Queue runner: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`
- Dispatch script: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch.py`
- Repo indexer: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\build_index.py`
- Inventory CLI: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`
- VolumeRegistry: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py`
- Node client (built in TASK-039): `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\client.py`

---

## What to Add

**All commands added to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`.**

### 1. `8os queue` — Run Build Queue

**Command:** `8os queue`

**Implementation:**

```python
@main.command()
@click.option("--status", is_flag=True, help="Show queue status")
def queue(status):
    """Run build queue or show queue status."""
    if status:
        _show_queue_status()
    else:
        _run_queue()
```

**`_run_queue()`:**

```python
def _run_queue():
    """Run the build queue."""
    from .deia.hive.scripts.queue.run_queue import run_queue

    click.echo("Running build queue...")
    try:
        result = run_queue()  # Assumes run_queue() returns count or summary
        click.echo(f"Queue complete: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
```

**`_show_queue_status()`:**

```python
def _show_queue_status():
    """Show queue status (pending tasks)."""
    from pathlib import Path

    queue_dir = Path(".deia/hive/tasks")
    if not queue_dir.exists():
        click.echo("Queue directory not found")
        return

    # Count pending tasks (not in _archive/)
    pending = [f for f in queue_dir.glob("TASK-*.md") if f.is_file()]
    archived = list((queue_dir / "_archive").glob("TASK-*.md")) if (queue_dir / "_archive").exists() else []

    click.echo(f"Pending: {len(pending)}")
    click.echo(f"Archived: {len(archived)}")

    if pending:
        click.echo("\nPending tasks:")
        for task in sorted(pending):
            click.echo(f"  - {task.name}")
```

---

### 2. `8os dispatch` — Dispatch Single Task

**Command:** `8os dispatch <task_file>`

**Options:**

- `--model` — model to use (haiku, sonnet, opus)
- `--role` — bot role (bee, queen, oracle)
- `--inject-boot` — inject .deia/BOOT.md

**Implementation:**

```python
@main.command()
@click.argument("task_file", type=click.Path(exists=True))
@click.option("--model", type=click.Choice(["haiku", "sonnet", "opus"]), default="sonnet")
@click.option("--role", type=click.Choice(["bee", "queen", "oracle"]), default="bee")
@click.option("--inject-boot", is_flag=True, help="Inject BOOT.md into prompt")
def dispatch(task_file, model, role, inject_boot):
    """Dispatch a single task file."""
    from pathlib import Path
    import subprocess

    dispatch_script = Path(".deia/hive/scripts/dispatch.py")
    if not dispatch_script.exists():
        click.echo("Error: dispatch.py not found", err=True)
        sys.exit(1)

    # Build command
    cmd = [
        sys.executable,
        str(dispatch_script),
        task_file,
        "--model", model,
        "--role", role
    ]

    if inject_boot:
        cmd.append("--inject-boot")

    click.echo(f"Dispatching {Path(task_file).name}...")

    # Run dispatch.py
    try:
        result = subprocess.run(cmd, check=True)
        click.echo("Dispatch complete")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: Dispatch failed with code {e.returncode}", err=True)
        sys.exit(1)
```

---

### 3. `8os index` — Rebuild Repo Semantic Search Index

**Command:** `8os index`

**Options:**

- `--full` — full rebuild (not incremental)

**Implementation:**

```python
@main.command()
@click.option("--full", is_flag=True, help="Full rebuild (not incremental)")
def index(full):
    """Rebuild repo semantic search index."""
    from pathlib import Path
    import subprocess

    index_script = Path("_tools/build_index.py")
    if not index_script.exists():
        click.echo("Error: build_index.py not found", err=True)
        sys.exit(1)

    cmd = [sys.executable, str(index_script)]

    if full:
        cmd.append("--full")

    click.echo("Building repo index...")

    try:
        subprocess.run(cmd, check=True)
        click.echo("Index complete")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: Index build failed with code {e.returncode}", err=True)
        sys.exit(1)
```

---

### 4. `8os inventory` — Passthrough to Inventory CLI

**Command:** `8os inventory [args...]`

**Passthrough all args to `_tools/inventory.py`.**

**Implementation:**

```python
@main.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def inventory(args):
    """Manage feature inventory (passthrough to _tools/inventory.py)."""
    from pathlib import Path
    import subprocess

    inventory_script = Path("_tools/inventory.py")
    if not inventory_script.exists():
        click.echo("Error: inventory.py not found", err=True)
        sys.exit(1)

    cmd = [sys.executable, str(inventory_script)] + list(args)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
```

**Examples:**

- `8os inventory stats` → `python _tools/inventory.py stats`
- `8os inventory add --id FT-050 --title "New feature" --layer browser --tests 5`
- `8os inventory bug add --id BUG-010 --title "Fix login"`

---

### 5. `8os volumes` — List Mounted Volumes

**Command:** `8os volumes`

**Show volume name, type (local/cloud), path, online/offline status.**

**Implementation:**

```python
@main.command()
def volumes():
    """List mounted volumes and their status."""
    try:
        # Call local hivenode /storage/volumes endpoint (assumes route exists)
        response = httpx.get(
            "http://localhost:8420/storage/volumes",
            timeout=10.0
        )
        response.raise_for_status()

        # Parse response
        data = response.json()
        vols = data.get("volumes", [])

        if not vols:
            click.echo("No volumes mounted")
            return

        # Print table
        click.echo(f"{'Volume':<15} {'Type':<10} {'Status':<10} {'Path'}")
        click.echo("-" * 60)

        for vol in vols:
            name = vol.get("name", "")
            vol_type = vol.get("type", "")
            online = vol.get("online", False)
            path = vol.get("path", "")

            status = "online" if online else "offline"
            click.echo(f"{name:<15} {vol_type:<10} {status:<10} {path}")

    except httpx.ConnectError:
        click.echo("Error: Hivenode is not running", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
```

**New route needed:**

Add to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage.py`:

```python
@router.get("/volumes", response_model=VolumesResponse)
async def list_volumes(
    registry: VolumeRegistry = Depends(get_volume_registry)
):
    """List all mounted volumes with status."""
    volumes = []

    for name, adapter in registry._adapters.items():
        vol_info = {
            "name": name,
            "type": adapter.adapter_type,  # "local" or "cloud"
            "online": adapter.is_online(),  # Assumes adapters have is_online()
            "path": str(adapter.base_path) if hasattr(adapter, "base_path") else ""
        }
        volumes.append(vol_info)

    return VolumesResponse(volumes=volumes)
```

**New schema:**

Add to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py`:

```python
class VolumeInfo(BaseModel):
    name: str
    type: str
    online: bool
    path: str

class VolumesResponse(BaseModel):
    volumes: List[VolumeInfo]
```

---

### 6. `8os node list` — Show Connected Nodes

**Command:** `8os node list`

**Show table of connected nodes (from cloud discover).**

**Implementation:**

```python
@main.group()
def node():
    """Node management commands."""
    pass

@node.command("list")
def node_list():
    """List connected nodes."""
    try:
        # Call local hivenode /node/peers endpoint (built in TASK-039)
        response = httpx.get(
            "http://localhost:8420/node/peers",
            timeout=10.0
        )
        response.raise_for_status()

        # Parse response
        data = response.json()
        nodes = data.get("nodes", [])

        if not nodes:
            click.echo("No nodes connected")
            return

        # Print table
        click.echo(f"{'Node ID':<20} {'Mode':<10} {'IP':<15} {'Status':<10} {'Last Seen'}")
        click.echo("-" * 80)

        for node in nodes:
            node_id = node.get("node_id", "")[:18]
            mode = node.get("mode", "")
            ip = node.get("ip", "")
            online = node.get("online", False)
            last_seen = node.get("last_seen", "")

            status = "online" if online else "offline"

            # Format last_seen as relative time (e.g., "2m ago")
            try:
                from datetime import datetime, UTC
                last_dt = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
                now = datetime.now(UTC)
                delta = now - last_dt
                if delta.total_seconds() < 60:
                    last_seen_fmt = "just now"
                elif delta.total_seconds() < 3600:
                    last_seen_fmt = f"{int(delta.total_seconds() / 60)}m ago"
                elif delta.total_seconds() < 86400:
                    last_seen_fmt = f"{int(delta.total_seconds() / 3600)}h ago"
                else:
                    last_seen_fmt = f"{int(delta.total_seconds() / 86400)}d ago"
            except:
                last_seen_fmt = last_seen

            click.echo(f"{node_id:<20} {mode:<10} {ip:<15} {status:<10} {last_seen_fmt}")

    except httpx.ConnectError:
        click.echo("Error: Hivenode is not running", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
```

---

### 7. `8os node announce` — Force Re-Announce

**Command:** `8os node announce`

**Force re-announce to cloud (useful after network change).**

**Implementation:**

```python
@node.command("announce")
def node_announce():
    """Force re-announce to cloud."""
    try:
        # Call local hivenode /node/announce endpoint (assumes local route exists)
        response = httpx.post(
            "http://localhost:8420/node/announce",
            timeout=10.0
        )
        response.raise_for_status()

        data = response.json()
        announced_at = data.get("announced_at", "")

        click.echo(f"Announced to cloud at {announced_at}")

    except httpx.ConnectError:
        click.echo("Error: Hivenode is not running", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
```

**New route needed:**

Add to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node_local.py`:

```python
@router.post("/announce", response_model=NodeAnnounceResponse)
async def force_announce(
    client: NodeAnnouncementClient = Depends(get_node_client)
):
    """Force re-announce to cloud."""
    announced_at = await client.announce()

    if not announced_at:
        raise HTTPException(status_code=503, detail="Failed to announce to cloud")

    return NodeAnnounceResponse(ok=True, announced_at=announced_at)
```

---

## File Structure

```
hivenode/
├── cli.py                [MODIFY] Add all new commands
├── routes/
│   ├── storage.py        [MODIFY] Add GET /storage/volumes
│   └── node_local.py     [MODIFY] Add POST /node/announce
└── schemas.py            [MODIFY] Add VolumeInfo, VolumesResponse

tests/hivenode/
└── test_cli_commands.py  [CREATE] Test suite
```

---

## Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cli_commands.py`

**Coverage (~10 tests):**

1. **Queue:**
   - ✓ `8os queue --status` shows pending/archived counts
   - ✓ `8os queue` runs queue runner (mock run_queue())

2. **Dispatch:**
   - ✓ `8os dispatch TASK.md` calls dispatch.py with correct args
   - ✓ `--model`, `--role`, `--inject-boot` flags passed through

3. **Index:**
   - ✓ `8os index` calls build_index.py (mock subprocess)
   - ✓ `--full` flag passed through

4. **Inventory:**
   - ✓ `8os inventory stats` calls inventory.py stats (mock subprocess)
   - ✓ Args passed through correctly

5. **Volumes:**
   - ✓ `8os volumes` shows volume list (mock /storage/volumes response)
   - ✓ Handles hivenode not running gracefully

6. **Node:**
   - ✓ `8os node list` shows node table (mock /node/peers response)
   - ✓ `8os node announce` forces re-announce (mock /node/announce response)

**Test utilities:**

- Use `click.testing.CliRunner()` for CLI tests
- Mock `subprocess.run()` for passthrough commands
- Mock `httpx.get()/post()` for hivenode API calls
- Mock `run_queue()` function
- Use `pytest` fixtures for temp directories

---

## Acceptance Criteria

1. ✅ `8os queue` runs build queue
2. ✅ `8os queue --status` shows pending/archived counts
3. ✅ `8os dispatch TASK.md` dispatches single task with options
4. ✅ `8os index` rebuilds repo index (incremental)
5. ✅ `8os index --full` rebuilds repo index (full)
6. ✅ `8os inventory` passes args to inventory.py
7. ✅ `8os volumes` shows volume list with online/offline status
8. ✅ `8os node list` shows connected nodes
9. ✅ `8os node announce` forces re-announce to cloud
10. ✅ All commands handle "hivenode not running" gracefully
11. ✅ All tests pass (10/10)

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs — every function fully implemented
- CLI commands must handle "hivenode not running" gracefully (exit code 1, error message)
- Passthrough commands (dispatch, index, inventory) use `subprocess.run()`, NOT imports (avoid import cycles)
- Error messages go to stderr (`err=True` in click.echo())

---

## Dependencies

**Required before start:**
- Queue runner (already built)
- Dispatch script (already built)
- Inventory CLI (already built)
- VolumeRegistry (already built)
- Node client (TASK-039) — for node commands

**Blocks:**
- None (final Wave 4 task)

---

## Notes

- Some commands require new routes (`/storage/volumes`, `/node/announce` in local mode) — add these routes as part of this task
- Node commands assume TASK-039 is complete (node_local.py routes exist)
- `8os inventory` is a passthrough — ALL args forwarded to inventory.py unchanged
- Volume online/offline detection assumes adapters have `is_online()` method — if not, stub it to always return `True`
- Queue status is simple file count — no need to parse YAML front matter
- Dispatch command does NOT wait for completion — just fires and forgets (dispatch.py is async)
