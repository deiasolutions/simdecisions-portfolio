"""
store
=====

Terminal history store — SQLAlchemy Core (PG + SQLite dual backend).

Dependencies:
- import uuid
- from datetime import datetime, UTC
- from typing import List, Dict, Any, Optional
- from sqlalchemy import (
- from sqlalchemy.pool import StaticPool

Functions:
- init_engine(url: str, force: bool = False): Initialize the terminal store engine. Called once at startup.
- get_engine(): Get the current engine. Raises if not initialized.
- reset_engine(): For tests only — reset global engine.
- add_command(command: str, context: str = ""): Add a command to history.
- get_all_commands(limit: Optional[int] = None): Get all commands from history, ordered by most recent first.
- get_command_list(limit: Optional[int] = None): Get list of command strings from history.
- clear_history(): Clear all command history.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
