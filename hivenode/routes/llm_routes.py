"""
llm_routes
==========

LLM proxy routes - POST /llm/chat endpoint.

Dependencies:
- import time
- import logging
- from typing import Optional, List
- from fastapi import APIRouter, Request, HTTPException, Header
- from pydantic import BaseModel, Field
- from slowapi import Limiter
- from slowapi.util import get_remote_address
- from hivenode.llm.proxy import resolve_key, enforce_model, call_anthropic_api, extract_text_content
- from hivenode.llm.cost import calculate_cost, emit_llm_event
- from hivenode.ledger.writer import LedgerWriter

Classes:
- ChatMessage: Chat message format.
- ChatRequest: Request body for POST /llm/chat.
- UsageInfo: Token usage information.
- ChatResponse: Successful response from POST /llm/chat.
- ErrorResponse: Error response.

Functions:
- init_ledger_writer(db_path: str): Initialize the global ledger writer.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
