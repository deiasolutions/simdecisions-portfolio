# TASK-028: /shell/exec Route + OS Translation

**Assigned to:** BEE (Sonnet)
**From:** Q33N
**Date:** 2026-03-12
**Spec:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Sections 3.2.1–3.2.3)
**Part of:** SPEC-HIVENODE-E2E-001 Wave 1

---

## Objective

Create the `/shell/exec` route that receives IR (intermediate representation) shell commands, translates them to the local OS (Windows/Unix), executes them, and returns the output. Includes OS translation engine, allowlist/denylist security, and Event Ledger integration.

---

## Requirements

### Route Specification

**Endpoint:** `POST /shell/exec`

**Request schema:**
```json
{
  "command": "mkdir",
  "args": ["foo/bar"],
  "working_dir": "home://projects/myapp",
  "os_hint": "auto"
}
```

**Response schema:**
```json
{
  "status": "success",
  "exit_code": 0,
  "stdout": "",
  "stderr": "",
  "os_used": "windows",
  "command_executed": "mkdir foo\\bar",
  "duration_ms": 12
}
```

**Error response:**
```json
{
  "status": "denied",
  "reason": "Command not in allowlist: rm",
  "exit_code": -1
}
```

### OS Translation

From spec Section 3.2.1 — translate IR commands to platform-specific commands:

| IR command | Windows | Unix/Mac |
|-----------|---------|----------|
| `mkdir foo/bar` | `mkdir foo\bar` | `mkdir -p foo/bar` |
| `ls -la` | `dir /a` | `ls -la` |
| `cp file1 file2` | `copy file1 file2` | `cp file1 file2` |
| `rm file` | `del file` | `rm file` |
| `cat file` | `type file` | `cat file` |
| `grep pattern file` | `findstr pattern file` | `grep pattern file` |
| `pwd` | `cd` | `pwd` |
| `mv file1 file2` | `move file1 file2` | `mv file1 file2` |
| `touch file` | `type nul > file` | `touch file` |

**Path separator normalization:**
- Windows: `/` → `\` in all path arguments
- Unix: `\` → `/` in all path arguments

**Detection:**
- Use `platform.system()` to detect OS: `"Windows"` / `"Darwin"` / `"Linux"`
- Cache OS detection result (don't call on every command)

### Allowlist / Denylist

From spec Section 3.2.2:

**Default allowlist** (commands accepted):
```python
DEFAULT_ALLOWLIST = [
    "mkdir", "ls", "dir", "cp", "copy", "mv", "move", "rm", "del",
    "cat", "type", "grep", "findstr", "pwd", "cd", "echo", "touch",
    "find", "git", "npm", "python", "pytest", "node", "pip"
]
```

**Default denylist** (commands always rejected):
```python
DEFAULT_DENYLIST = [
    "rm -rf /",
    "del /s /q C:\\",
    "format",
    "mkfs",
    ":(){:|:&};:"  # Fork bomb
]
```

**Validation logic:**
1. Check if full command string matches denylist pattern → DENY
2. Check if command name is in allowlist → ALLOW
3. Otherwise → DENY

### Security

From spec Section 3.2.3:

1. **Mode restriction**: Shell exec is LOCAL MODE ONLY by default
   - If `settings.mode == "cloud"`, reject with 403 error
   - Cloud mode can enable shell exec via config (future wave)

2. **Event Ledger logging**:
   - Every execution → log `SHELL_EXEC` event with: command, args, exit_code, duration, actor
   - Every denial → log `SHELL_DENIED` event with: command, reason, actor

3. **Timeout**: 30 seconds default
   - Use `subprocess.run(timeout=30)` to enforce
   - If timeout exceeded → return error response with status="timeout"

4. **Working directory resolution**:
   - `working_dir` is a volume URI (e.g., `home://projects/myapp`)
   - Use `PathResolver` to resolve to actual disk path
   - Execute command in that directory

### Architecture

Create the following modules:

1. **`hivenode/shell/__init__.py`** — empty
2. **`hivenode/shell/executor.py`** — `ShellExecutor` class
3. **`hivenode/shell/allowlist.py`** — allowlist/denylist validation
4. **`hivenode/routes/shell.py`** — FastAPI route handler

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Sections 3.2.1–3.2.3)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (how routes are mounted)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\resolver.py` (volume path resolution — `home://` → disk path)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` (VolumeRegistry for volume lookups)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (dependency injection pattern)
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` (how to log events)
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings.mode for local/cloud check)
8. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` (existing Pydantic models — follow same pattern)

---

## Files to Create

### 1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\shell\__init__.py`

Empty file (marks package).

---

### 2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\shell\allowlist.py`

Allowlist/denylist validation.

```python
"""Shell command allowlist and denylist."""
from typing import List

DEFAULT_ALLOWLIST = [
    "mkdir", "ls", "dir", "cp", "copy", "mv", "move", "rm", "del",
    "cat", "type", "grep", "findstr", "pwd", "cd", "echo", "touch",
    "find", "git", "npm", "python", "pytest", "node", "pip"
]

DEFAULT_DENYLIST = [
    "rm -rf /",
    "del /s /q C:\\",
    "format",
    "mkfs",
    ":(){:|:&};:"  # Fork bomb
]

def is_allowed(command: str, args: List[str], allowlist: List[str] = None, denylist: List[str] = None) -> tuple[bool, str]:
    """
    Check if command is allowed.

    Args:
        command: Command name (e.g., "mkdir")
        args: Command arguments
        allowlist: List of allowed commands (default: DEFAULT_ALLOWLIST)
        denylist: List of denied command patterns (default: DEFAULT_DENYLIST)

    Returns:
        (allowed: bool, reason: str)
    """
    if allowlist is None:
        allowlist = DEFAULT_ALLOWLIST
    if denylist is None:
        denylist = DEFAULT_DENYLIST

    # Build full command string for denylist check
    full_command = f"{command} {' '.join(args)}"

    # Check denylist (exact match or pattern)
    for denied in denylist:
        if denied in full_command:
            return False, f"Command matches denylist pattern: {denied}"

    # Check allowlist
    if command not in allowlist:
        return False, f"Command not in allowlist: {command}"

    return True, ""
```

---

### 3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\shell\executor.py`

OS translation and command execution engine.

```python
"""Shell command executor with OS translation."""
import platform
import subprocess
from typing import List, Tuple
from datetime import datetime

class ShellExecutor:
    """Execute shell commands with OS translation."""

    # Translation table: IR command → (Windows command, Unix command)
    TRANSLATION_TABLE = {
        "mkdir": ("mkdir", "mkdir -p"),
        "ls": ("dir /a", "ls -la"),
        "cp": ("copy", "cp"),
        "rm": ("del", "rm"),
        "cat": ("type", "cat"),
        "grep": ("findstr", "grep"),
        "pwd": ("cd", "pwd"),
        "mv": ("move", "mv"),
        "touch": ("type nul >", "touch"),
    }

    def __init__(self):
        """Initialize executor."""
        self.os_type = platform.system()  # "Windows", "Darwin", or "Linux"

    def translate(self, command: str, args: List[str]) -> Tuple[str, List[str]]:
        """
        Translate IR command to native OS command.

        Args:
            command: IR command name
            args: Command arguments

        Returns:
            (native_command, native_args)
        """
        # Get translation
        if command in self.TRANSLATION_TABLE:
            win_cmd, unix_cmd = self.TRANSLATION_TABLE[command]
            native_cmd = win_cmd if self.os_type == "Windows" else unix_cmd
        else:
            # No translation needed (e.g., git, npm, python)
            native_cmd = command

        # Normalize path separators in args
        native_args = [self._normalize_path(arg) for arg in args]

        # Handle special cases (e.g., "ls -la" → "dir /a" on Windows)
        if command == "ls" and self.os_type == "Windows":
            # "ls -la" → "dir /a"
            return "dir", ["/a"]
        elif command == "touch" and self.os_type == "Windows":
            # "touch file" → "type nul > file"
            return "cmd", ["/c", f"type nul > {native_args[0]}"]

        return native_cmd, native_args

    def _normalize_path(self, path: str) -> str:
        """Normalize path separators for OS."""
        if self.os_type == "Windows":
            return path.replace("/", "\\")
        else:
            return path.replace("\\", "/")

    def execute(self, command: str, args: List[str], working_dir: str, timeout: int = 30) -> dict:
        """
        Execute command and return result.

        Args:
            command: IR command name
            args: Command arguments
            working_dir: Working directory (absolute path)
            timeout: Timeout in seconds

        Returns:
            {
                "status": "success" | "error" | "timeout",
                "exit_code": int,
                "stdout": str,
                "stderr": str,
                "command_executed": str,
                "os_used": str,
                "duration_ms": int
            }
        """
        # Translate to native command
        native_cmd, native_args = self.translate(command, args)
        full_command = f"{native_cmd} {' '.join(native_args)}"

        # Execute
        start_time = datetime.now()
        try:
            result = subprocess.run(
                [native_cmd] + native_args,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            return {
                "status": "success",
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command_executed": full_command,
                "os_used": self.os_type.lower(),
                "duration_ms": duration_ms
            }

        except subprocess.TimeoutExpired:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            return {
                "status": "timeout",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout}s",
                "command_executed": full_command,
                "os_used": self.os_type.lower(),
                "duration_ms": duration_ms
            }

        except Exception as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            return {
                "status": "error",
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "command_executed": full_command,
                "os_used": self.os_type.lower(),
                "duration_ms": duration_ms
            }
```

**Key notes:**
- Translation table maps IR → (Windows, Unix)
- Path normalization handles `/` vs `\`
- Special cases: `ls -la`, `touch` on Windows
- `subprocess.run` with timeout enforcement
- Duration tracking for Event Ledger

---

### 4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\shell\schemas.py`

Pydantic request/response models.

```python
"""Pydantic schemas for shell execution."""
from typing import List
from pydantic import BaseModel, Field

class ShellExecRequest(BaseModel):
    """Shell execution request."""
    command: str = Field(..., description="IR command name (e.g., 'mkdir')")
    args: List[str] = Field(default_factory=list, description="Command arguments")
    working_dir: str = Field(..., description="Working directory (volume URI, e.g., 'home://projects')")
    os_hint: str = Field(default="auto", description="OS hint ('auto', 'windows', 'unix')")

class ShellExecResponse(BaseModel):
    """Shell execution response."""
    status: str = Field(..., description="'success', 'error', 'timeout', 'denied'")
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    os_used: str = ""
    command_executed: str = ""
    duration_ms: int = 0
    reason: str = ""  # Only for denied status
```

---

### 5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\shell.py`

FastAPI route handler.

```python
"""Shell execution routes."""
from fastapi import APIRouter, HTTPException, Depends, status
from hivenode.config import settings
from hivenode.dependencies import get_ledger_writer, get_volume_registry, verify_jwt_or_local
from hivenode.ledger.writer import LedgerWriter
from hivenode.storage.registry import VolumeRegistry
from hivenode.storage.resolver import PathResolver
from hivenode.shell.executor import ShellExecutor
from hivenode.shell.allowlist import is_allowed
from hivenode.shell.schemas import ShellExecRequest, ShellExecResponse

router = APIRouter()

@router.post("/exec", response_model=ShellExecResponse)
async def exec_command(
    req: ShellExecRequest,
    ledger: LedgerWriter = Depends(get_ledger_writer),
    registry: VolumeRegistry = Depends(get_volume_registry),
    user: dict = Depends(verify_jwt_or_local)
):
    """
    Execute a shell command with OS translation.

    Security:
    - LOCAL MODE ONLY by default
    - Allowlist/denylist validation
    - Event Ledger logging
    - 30-second timeout
    """
    # Check mode (local only)
    if settings.mode == "cloud":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Shell execution not allowed in cloud mode"
        )

    # Validate command against allowlist/denylist
    allowed, reason = is_allowed(req.command, req.args)
    if not allowed:
        # Log denial
        ledger.write_event(
            event_type="SHELL_DENIED",
            actor=f"user:{user['sub']}",
            payload_json={"command": req.command, "args": req.args, "reason": reason}
        )

        return ShellExecResponse(
            status="denied",
            exit_code=-1,
            reason=reason
        )

    # Resolve working directory (volume URI → disk path)
    resolver = PathResolver(registry)
    try:
        adapter, rel_path = resolver.resolve(req.working_dir)
        working_dir = adapter.resolve_path(rel_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid working directory: {str(e)}"
        )

    # Execute command
    executor = ShellExecutor()
    result = executor.execute(req.command, req.args, working_dir)

    # Log execution
    ledger.write_event(
        event_type="SHELL_EXEC",
        actor=f"user:{user['sub']}",
        payload_json={
            "command": req.command,
            "args": req.args,
            "exit_code": result["exit_code"],
            "duration_ms": result["duration_ms"],
            "working_dir": req.working_dir
        }
    )

    return ShellExecResponse(**result)
```

**Key notes:**
- Cloud mode check → 403
- Allowlist validation → logs `SHELL_DENIED`
- Volume URI resolution via `PathResolver`
- Execution via `ShellExecutor`
- Event Ledger logs `SHELL_EXEC`

---

## Files to Modify

### 1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`

Mount the shell router.

**Add import:**
```python
from hivenode.routes import health, auth, ledger_routes, storage_routes, node, llm_routes, shell
```

**Add to `create_router()` function:**
```python
router.include_router(shell.router, prefix='/shell', tags=['shell'])
```

---

### 2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml`

Add `hivenode.shell` to packages list.

**Modify `[tool.setuptools] packages`:**
```python
packages = ["ra96it", "ra96it.services", "ra96it.routes", "hivenode", "hivenode.routes", "hivenode.ledger", "hivenode.storage", "hivenode.storage.adapters", "hivenode.adapters", "hivenode.privacy", "hivenode.llm", "hivenode.governance", "hivenode.governance.gate_enforcer", "hivenode.shell", "engine"]
```

---

## Tests

Create comprehensive test suite in `tests/hivenode/shell/` and `tests/hivenode/test_shell_routes.py`.

### Test Files

1. **`tests/hivenode/shell/test_executor.py`** — Test OS translation and execution (~10 tests)
2. **`tests/hivenode/shell/test_allowlist.py`** — Test allowlist/denylist validation (~5 tests)
3. **`tests/hivenode/test_shell_routes.py`** — Test route handler (~8 tests)

### Test Requirements

**`test_executor.py` tests:**
1. `test_translate_mkdir_windows` — Verify path separator normalization
2. `test_translate_mkdir_unix` — Verify `-p` flag added
3. `test_translate_ls_windows` — Verify `dir /a` translation
4. `test_translate_ls_unix` — Verify passthrough
5. `test_translate_touch_windows` — Verify `type nul >` translation
6. `test_translate_touch_unix` — Verify passthrough
7. `test_execute_success` — Mock subprocess, verify result structure
8. `test_execute_timeout` — Mock timeout, verify error response
9. `test_execute_error` — Mock exception, verify error handling
10. `test_normalize_path_windows` — Verify `/` → `\`
11. `test_normalize_path_unix` — Verify `\` → `/`

**`test_allowlist.py` tests:**
1. `test_allowed_command` — `mkdir` should pass
2. `test_denied_command` — `mkfs` should fail
3. `test_not_in_allowlist` — `rm` with no allowlist entry should fail
4. `test_denylist_pattern_match` — `rm -rf /` should fail
5. `test_fork_bomb_denied` — Fork bomb pattern should fail

**`test_shell_routes.py` tests:**
1. `test_exec_success_local_mode` — Execute `mkdir` successfully
2. `test_exec_denied_command` — Verify denylist rejection
3. `test_exec_cloud_mode_forbidden` — Verify 403 in cloud mode
4. `test_exec_invalid_working_dir` — Verify 400 for bad volume URI
5. `test_exec_logs_shell_exec_event` — Verify Event Ledger logging
6. `test_exec_logs_shell_denied_event` — Verify denial logging
7. `test_exec_timeout` — Mock long-running command, verify timeout
8. `test_exec_volume_path_resolution` — Verify `home://` resolves correctly

**Test structure example:**
```python
import pytest
from unittest.mock import Mock, patch
from hivenode.shell.executor import ShellExecutor
from hivenode.shell.allowlist import is_allowed

def test_translate_mkdir_windows():
    """Test mkdir translation on Windows."""
    executor = ShellExecutor()
    with patch('platform.system', return_value='Windows'):
        executor.os_type = 'Windows'
        cmd, args = executor.translate('mkdir', ['foo/bar'])
        assert cmd == 'mkdir'
        assert args == ['foo\\bar']  # Path separator normalized

def test_allowed_command():
    """Test that allowed command passes."""
    allowed, reason = is_allowed('mkdir', ['foo'])
    assert allowed is True
    assert reason == ""

def test_denied_command():
    """Test that denied command fails."""
    allowed, reason = is_allowed('format', [])
    assert allowed is False
    assert "denylist" in reason.lower() or "allowlist" in reason.lower()
```

---

## Implementation Order (TDD)

1. **Write tests first:**
   - `tests/hivenode/shell/test_allowlist.py` (5 tests)
   - `tests/hivenode/shell/test_executor.py` (11 tests)
   - `tests/hivenode/test_shell_routes.py` (8 tests)

2. **Implement modules:**
   - `hivenode/shell/__init__.py` (empty)
   - `hivenode/shell/allowlist.py`
   - `hivenode/shell/executor.py`
   - `hivenode/shell/schemas.py`
   - `hivenode/routes/shell.py`

3. **Modify existing files:**
   - `hivenode/routes/__init__.py` (mount shell router)
   - `pyproject.toml` (add `hivenode.shell` to packages)

4. **Run all tests** — Verify 24 total tests pass (5 + 11 + 8)

---

## Constraints

- No file over 500 lines (executor.py should be ~150 lines, shell.py ~80 lines)
- TDD — tests first, implementation second
- No stubs — every function fully implemented
- All paths in task file must be absolute
- Cross-platform compatibility (Windows + Unix/Mac)
- Security-first approach (allowlist/denylist + Event Ledger)

---

## Expected Test Count

**Target:** 24 tests total
- `test_allowlist.py`: 5 tests
- `test_executor.py`: 11 tests
- `test_shell_routes.py`: 8 tests

---

## Definition of Done

- [ ] `hivenode/shell/__init__.py` created (empty)
- [ ] `hivenode/shell/allowlist.py` created with validation logic
- [ ] `hivenode/shell/executor.py` created with OS translation
- [ ] `hivenode/shell/schemas.py` created with Pydantic models
- [ ] `hivenode/routes/shell.py` created with route handler
- [ ] `hivenode/routes/__init__.py` updated (shell router mounted)
- [ ] `pyproject.toml` updated (`hivenode.shell` in packages)
- [ ] 24 tests created and passing
- [ ] Cloud mode rejection working (403 error)
- [ ] Allowlist/denylist validation working
- [ ] Event Ledger logging working (`SHELL_EXEC`, `SHELL_DENIED`)
- [ ] Volume URI resolution working
- [ ] Timeout enforcement working (30 seconds)
- [ ] No stubs, no TODOs, no incomplete functions

---

**Q33N signature:** TASK-028-READY-FOR-DISPATCH
