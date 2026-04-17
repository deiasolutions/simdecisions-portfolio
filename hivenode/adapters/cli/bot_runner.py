"""
bot_runner
==========

Autonomous Bot Runner - Persistent bot task execution system

Monitors task queues, executes tasks via platform adapters, reports results.
Designed to run as persistent background process communicating with lead bot.

Dependencies:
- from typing import Dict, Any, Optional, Callable
- from pathlib import Path
- from datetime import datetime
- import time
- import asyncio
- import threading
- import logging
- from .claude_code_adapter import ClaudeCodeAdapter, parse_task_file, write_response_file
- from .claude_code_cli_adapter import ClaudeCodeCLIAdapter
- from .claude_sdk_adapter import ClaudeSDKAdapter

Classes:
- BotRunner: Autonomous bot runner for persistent task execution.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
