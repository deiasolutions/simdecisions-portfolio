"""
store
=====

Efemera messaging store — SQLAlchemy Core (PG + SQLite dual backend).

Rewritten from raw sqlite3. Follows the same pattern as inventory/store.py:
global _engine singleton, init_engine()/get_engine()/reset_engine(), Table defs.

Field renames from legacy:
  channels.created_by → owner_id
  messages.author_id  → sender_id
  messages.author_name → display_name
  members.username    → display_name

Dependencies:
- import uuid
- from datetime import datetime, UTC
- from typing import List, Dict, Any, Optional
- from sqlalchemy import (
- from sqlalchemy.pool import StaticPool

Functions:
- init_engine(url: str, force: bool = False): Initialize the relay store engine. Called once at startup.
- get_engine(): Get the current engine. Raises if not initialized.
- reset_engine(): For tests only — reset global engine.
- _seed_if_empty(): Seed system channels if the channels table is empty.
- _now(): List all channels.
- get_channel(channel_id: str): Get a single channel by ID.
- create_channel(name: str,
    channel_type: str,
    owner_id: str,
    pinned: bool = False,
    description: str = "",
    read_only: bool = False,
    channel_id: Optional[str] = None,): Create a new channel.
- list_messages(channel_id: str, since: Optional[str] = None, limit: int = 50): List messages for a channel, optionally since a timestamp.
- create_message(channel_id: str,
    sender_id: str,
    display_name: str,
    content: str,
    author_type: str = "human",
    message_type: str = "text",
    reply_to_id: Optional[str] = None,
    moderation_status: str = "approved",
    moderation_reason: Optional[str] = None,
    metadata_json: Optional[str] = None,): Create a new message in a channel.
- get_message(message_id: str): Get a single message by ID.
- edit_message(message_id: str, new_content: str, editor_id: str): Create a new version of a message. Returns the new version row.
- get_message_history(message_id: str): Get all versions of a message (the edit chain).
- get_replies(message_id: str, limit: int = 50): Get replies to a message (latest version only).
- update_message_status(message_id: str, status: str, reason: Optional[str] = None): Update moderation status of a message.
- list_members(channel_id: str): List members of a channel with presence status.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
