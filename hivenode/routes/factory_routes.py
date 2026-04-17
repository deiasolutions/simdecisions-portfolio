"""
factory_routes
==============

Factory Routes — Mobile factory operations API.

MCP-with-fallback pattern:
- Prefer MCP tools when available (fast, real-time)
- Fallback to file operations when MCP is down
- File-based flow remains canonical

Endpoints:
- GET  /factory/responses         — List response files
- GET  /factory/responses/{id}/content — Get response content
- POST /factory/archive           — Archive task + response
- POST /factory/spec-submit       — Submit new spec
- GET  /factory/git-summary       — Git activity summary
- GET  /factory/health            — Service health check

Dependencies:
- import json
- import logging
- import re
- import subprocess
- import sys
- from datetime import datetime
- from pathlib import Path
- from fastapi import APIRouter, HTTPException, Query
- from pydantic import BaseModel
- from ..mcp.client import mcp_client

Classes:
- ArchiveRequest: Parse metadata from response file content.
- ReassignTaskRequest: Read queue state from disk. Returns default state if file doesn't exist.

Functions:
- parse_response_metadata(content: str): Parse metadata from response file content.
- extract_task_id_from_filename(filename: str): Extract task ID from response filename.
- extract_bee_id_from_filename(filename: str): Extract bee ID from response filename if present.
- generate_spec_id(spec_type: str): Generate spec ID: SPEC-{TYPE}-{YYYYMMDD}-{HHMM}
- render_spec_template(request: SpecSubmitRequest, spec_id: str): Render spec markdown from request.
- _read_queue_state(): Read queue state from disk. Returns default state if file doesn't exist.
- _write_queue_state(state: str): Write queue state to disk.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
