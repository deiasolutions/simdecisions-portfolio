"""
test_process_tree_kill
======================

Tests for process tree cleanup on bee termination (BUG-013 / BL-202).

Verifies that terminate() kills child processes, not just the direct PID.

Dependencies:
- import subprocess
- import sys
- import time
- import os
- from pathlib import Path
- from hivenode.adapters.cli.claude_cli_subprocess import ClaudeCodeProcess

Classes:
- TestKillTreeStatic: Unit tests for _kill_tree static method.
- TestTerminateKillsTree: Integration test: ClaudeCodeProcess.terminate() kills child tree.

Functions:
- _get_child_pids(parent_pid: int): Get child PIDs of a process (platform-aware).
- _pid_alive(pid: int): Check if a PID is still running.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
