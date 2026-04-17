"""
claude_cli_subprocess
=====================

claude_cli_subprocess.py

Core subprocess management for Claude Code CLI integration.
Handles process spawning, stream capture, task submission, and termination.

This module provides low-level process control for spawning and managing
'claude code' CLI processes. It captures output streams in background threads,
submits tasks via stdin, parses XML tool invocations, and enforces timeouts.

Dependencies:
- from typing import Optional, List, Dict, Any, Set
- from pathlib import Path
- from dataclasses import dataclass, field
- from enum import Enum
- import subprocess
- import threading
- import time
- import re
- import sys
- import os

Classes:
- ProcessState: Claude Code process states.
- ProcessResult: Result from Claude Code process execution.
- ClaudeCodeProcess: Claude Code CLI subprocess manager.

Functions:
- _build_pricing_dict(): Build a backward-compatible PRICING dict from rate_loader.
- extract_file_paths_from_tools(tool_uses: List[Dict[str, Any]]): Extract file paths from Write/Edit tool uses.
- extract_file_paths_from_text(text: str): Get all files shown in git status (modified, staged, untracked).
- verify_file_modifications(file_paths: Set[Path],
    start_time: float,
    work_dir: Path | None = None): Verify which files were actually modified by checking mtime against task start.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
