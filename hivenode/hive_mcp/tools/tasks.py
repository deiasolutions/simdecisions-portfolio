"""
tasks
=====

Task management tools for Hive MCP.

Dependencies:
- import os
- import re
- import yaml
- import shutil
- from pathlib import Path
- from typing import List, Dict, Optional, Any
- from datetime import datetime, timezone

Functions:
- _find_repo_root(): Find repository root by looking for .deia directory.
- _validate_task_path(task_file: str): Validate task file path (reject path traversal, absolute paths, and _archive).
- _parse_frontmatter(content: str): Parse YAML frontmatter from task file content.
- task_list(assigned_bee: Optional[str] = None,
    wave: Optional[str] = None,
    status: Optional[str] = None): List task files in .deia/hive/tasks/ with optional filters.
- task_read(task_file: str): Read a specific task file from .deia/hive/tasks/.
- _validate_task_naming(filename: str): Validate task file naming convention.
- task_write(filename: str, content: str): Write a task file to .deia/hive/tasks/.
- _response_exists(task_file: str): Check if a response file exists for the given task.
- task_archive(task_file: str): Archive a completed task to _archive/.
- claim_task(spec_id: str, bee_id: str, state_manager: Any): Claim a task from the queue to prevent double-dispatch.
- release_task(spec_id: str, reason: str, state_manager: Any): Release a claimed task and move spec to final destination.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
