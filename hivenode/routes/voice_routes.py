"""
voice_routes
============

Voice input API routes for Mobile Workdesk.

Provides HTTP and WebSocket endpoints for voice command parsing and execution.
Integrates Web Speech API transcripts with command interpreter and PRISM-IR emitter.

Dependencies:
- import logging
- from typing import Any, Dict, Optional
- from datetime import datetime, timezone
- from fastapi import APIRouter, HTTPException, status, Depends
- from pydantic import BaseModel, Field, field_validator
- from hivenode.shell.command_interpreter import CommandInterpreter, ParseResult
- from hivenode.shell.prism_emitter import PRISMEmitter, EmissionError
- from hivenode.dependencies import get_ledger_writer, verify_jwt_or_local
- from hivenode.ledger.writer import LedgerWriter

Classes:
- VoiceParseRequest: Request schema for voice command parsing.
- VoiceParseResponse: Response schema for voice command parsing.

Functions:
- get_command_interpreter(): Get singleton CommandInterpreter instance.
- get_prism_emitter(): Get singleton PRISMEmitter instance.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
