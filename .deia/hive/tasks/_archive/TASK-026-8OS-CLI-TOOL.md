# TASK-026: 8os CLI Tool (up/down/status)

**Assigned to:** BEE (Sonnet)
**From:** Q33N
**Date:** 2026-03-12
**Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Sections 2.1–2.3)
**Part of:** SPEC-HIVENODE-E2E-001 Wave 1

---

## Objective

Create the `8os` CLI tool for managing the local ShiftCenter hivenode. This wave implements only three commands: `up`, `down`, and `status`. The CLI uses `click` for subcommands and integrates into `pyproject.toml` as a script entry point.

---

## Requirements

### Functionality

1. **`8os up`**: Start the hivenode server as a background process
   - Run `uvicorn hivenode.main:app --host 0.0.0.0 --port 8420` as a background process
   - Store PID at `~/.shiftcenter/hivenode.pid`
   - Create `~/.shiftcenter/config.yml` on first run if it doesn't exist
   - Output: "Hivenode started on port 8420 (PID: <pid>)"
   - If already running: "Hivenode already running (PID: <pid>)"

2. **`8os down`**: Stop the hivenode server
   - Read PID from `~/.shiftcenter/hivenode.pid`
   - Kill the process gracefully (SIGTERM on Unix, TerminateProcess on Windows)
   - Remove PID file after successful kill
   - Output: "Hivenode stopped (PID: <pid>)"
   - If not running: "Hivenode is not running"

3. **`8os status`**: Check hivenode status
   - Read PID from `~/.shiftcenter/hivenode.pid`
   - Check if process is alive
   - Output if running: "Hivenode is running (PID: <pid>, Port: 8420)"
   - Output if stopped: "Hivenode is not running"

4. **Config file generation** (`~/.shiftcenter/config.yml`):
   - Generated on first `8os up` if it doesn't exist
   - Schema (from spec Section 2.3):
     ```yaml
     node_id: "node-<random-8-chars>"  # Auto-generated UUID-like string
     mode: "local"
     port: 8420
     cloud_url: "https://api.shiftcenter.com"
     volumes:
       home: "<platform-specific-default>"  # C:\Users\<user>\ShiftCenter on Windows, /Users/<user>/ShiftCenter on Mac
     sync:
       enabled: true
       interval_seconds: 300
       on_write: true
     ```
   - Use `platform.system()` to detect OS and set appropriate default home path
   - Generate random node_id with format `node-<8 hex chars>` (use `secrets.token_hex(4)`)

### Platform Compatibility

- **Windows**: Use `subprocess.Popen` with `creationflags=subprocess.CREATE_NEW_PROCESS_GROUP` to detach process. Use `psutil.Process(pid).terminate()` for graceful shutdown.
- **Unix/Mac**: Use `subprocess.Popen` with `start_new_session=True`. Use `os.kill(pid, signal.SIGTERM)`.
- **PID file path**: `Path.home() / ".shiftcenter" / "hivenode.pid"`
- **Config file path**: `Path.home() / ".shiftcenter" / "config.yml"`

### Dependencies

- Add `click>=8.0` to `[project.dependencies]` in `pyproject.toml`
- Add `psutil>=5.0` to `[project.dependencies]` for cross-platform process management

### Entry Point

Add to `pyproject.toml`:
```toml
[project.scripts]
hive = "hivenode.__main__:main"
8os = "hivenode.cli:main"  # NEW - do not remove existing "hive" entry
```

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Sections 2.1–2.3)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (existing settings — port 8420, modes)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\__main__.py` (existing entry point)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` (existing scripts entry: `hive = "hivenode.__main__:main"`)

---

## Files to Create

### 1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`

Main CLI module with click commands.

**Structure:**
```python
import click
import subprocess
import platform
import signal
import secrets
from pathlib import Path
import yaml
import psutil
import sys

@click.group()
def main():
    """8os - ShiftCenter local environment manager."""
    pass

@main.command()
def up():
    """Start local hivenode."""
    # Check if already running
    # Create config if it doesn't exist
    # Start uvicorn as background process
    # Write PID file
    # Output success message
    pass

@main.command()
def down():
    """Stop local hivenode."""
    # Read PID file
    # Kill process gracefully
    # Remove PID file
    # Output success message
    pass

@main.command()
def status():
    """Show hivenode status."""
    # Read PID file
    # Check if process alive
    # Output status
    pass

def _get_pid_file() -> Path:
    """Get path to PID file."""
    return Path.home() / ".shiftcenter" / "hivenode.pid"

def _get_config_file() -> Path:
    """Get path to config file."""
    return Path.home() / ".shiftcenter" / "config.yml"

def _is_running(pid: int) -> bool:
    """Check if process is running."""
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

def _create_config_if_needed():
    """Create default config file if it doesn't exist."""
    config_path = _get_config_file()
    if config_path.exists():
        return

    # Generate node_id
    node_id = f"node-{secrets.token_hex(4)}"

    # Platform-specific home volume
    system = platform.system()
    if system == "Windows":
        home_volume = f"C:\\Users\\{Path.home().name}\\ShiftCenter"
    elif system == "Darwin":
        home_volume = f"/Users/{Path.home().name}/ShiftCenter"
    else:  # Linux
        home_volume = f"/home/{Path.home().name}/ShiftCenter"

    config = {
        "node_id": node_id,
        "mode": "local",
        "port": 8420,
        "cloud_url": "https://api.shiftcenter.com",
        "volumes": {
            "home": home_volume
        },
        "sync": {
            "enabled": True,
            "interval_seconds": 300,
            "on_write": True
        }
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

if __name__ == "__main__":
    main()
```

**Key implementation notes:**
- Use `psutil` for cross-platform process management (check if running, terminate)
- Use `subprocess.Popen` with platform-specific flags for background process
- Handle edge cases: process dead but PID file exists, process running but PID file missing
- Config generation uses `secrets.token_hex(4)` for 8 random hex chars
- YAML uses `yaml.dump()` with `default_flow_style=False` for readable output

---

## Files to Modify

### 1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml`

**Add to `[project.dependencies]`:**
```toml
"click>=8.0",
"psutil>=5.0",
```

**Add to `[project.scripts]`:**
```toml
8os = "hivenode.cli:main"
```

**IMPORTANT:** Do NOT remove the existing `hive = "hivenode.__main__:main"` entry. The new `8os` entry is ADDITIONAL.

---

## Tests

Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cli.py` with ~12 tests.

### Test Requirements

Use `click.testing.CliRunner` for all CLI tests. Mock `subprocess.Popen` and `psutil.Process` to avoid actually starting/stopping processes.

**Test cases:**

1. **`test_up_creates_pid_file`**: Mock Popen, verify PID file created with correct PID
2. **`test_up_creates_config_if_missing`**: Verify config.yml created on first run with correct schema
3. **`test_up_does_not_overwrite_config`**: Verify existing config.yml not touched
4. **`test_up_when_already_running`**: Mock running process, verify error message
5. **`test_down_removes_pid_file`**: Mock process, verify PID file removed after kill
6. **`test_down_when_not_running`**: Verify correct error message
7. **`test_down_kills_process`**: Mock process, verify `terminate()` called
8. **`test_status_running`**: Mock running process, verify output shows "running"
9. **`test_status_not_running`**: Mock no PID file, verify output shows "not running"
10. **`test_status_dead_process`**: PID file exists but process dead, verify correct message
11. **`test_config_generation_windows`**: Mock Windows platform, verify path format
12. **`test_config_generation_unix`**: Mock Unix platform, verify path format

**Test structure:**
```python
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from hivenode.cli import main, _create_config_if_needed
import yaml

@pytest.fixture
def cli_runner():
    """Create CLI runner."""
    return CliRunner()

@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """Mock home directory."""
    monkeypatch.setattr(Path, 'home', lambda: tmp_path)
    return tmp_path

def test_up_creates_pid_file(cli_runner, mock_home):
    """Test that 8os up creates PID file."""
    with patch('hivenode.cli.subprocess.Popen') as mock_popen:
        mock_process = Mock()
        mock_process.pid = 12345
        mock_popen.return_value = mock_process

        with patch('hivenode.cli._is_running', return_value=False):
            result = cli_runner.invoke(main, ['up'])

        assert result.exit_code == 0
        pid_file = mock_home / ".shiftcenter" / "hivenode.pid"
        assert pid_file.exists()
        assert pid_file.read_text() == "12345"

# ... more tests
```

---

## Implementation Order (TDD)

1. **Write tests first** in `tests/hivenode/test_cli.py` (all 12 tests)
2. Run tests (all should fail)
3. Implement `hivenode/cli.py` (all functionality)
4. Modify `pyproject.toml` (add dependencies + script entry)
5. Run tests (all should pass)
6. Manual verification: `pip install -e .` then run `8os up`, `8os status`, `8os down`

---

## Constraints

- No file over 500 lines (cli.py should be ~200 lines max)
- TDD — tests first, implementation second
- No stubs — every function fully implemented
- All paths must be absolute in this task file
- Cross-platform compatibility (Windows + Unix/Mac)
- Graceful error handling for all edge cases

---

## Expected Test Count

**Target:** 12 tests in `tests/hivenode/test_cli.py`

---

## Definition of Done

- [ ] `hivenode/cli.py` created with all three commands (`up`, `down`, `status`)
- [ ] Config generation working with correct schema
- [ ] Cross-platform process management working (Windows + Unix)
- [ ] PID file creation/deletion working
- [ ] `pyproject.toml` updated with `click`, `psutil` dependencies
- [ ] `pyproject.toml` updated with `8os` script entry (keeping `hive` entry)
- [ ] 12 tests in `tests/hivenode/test_cli.py` — all passing
- [ ] Manual verification: `8os up`, `8os status`, `8os down` all work
- [ ] No hardcoded paths (all use `Path.home()`)
- [ ] No stubs, no TODOs, no incomplete functions

---

**Q33N signature:** TASK-026-READY-FOR-DISPATCH
