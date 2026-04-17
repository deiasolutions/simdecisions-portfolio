"""
canvas_chat
===========

Canvas Chat API - LLM-powered natural language process building.

FastAPI endpoint that accepts chat messages and returns IR mutations.

Dependencies:
- from typing import List, Optional, Dict, Any
- from pydantic import BaseModel, Field
- from fastapi import APIRouter, HTTPException, Request
- from jsonpatch import apply_patch
- from slowapi import Limiter
- from slowapi.util import get_remote_address
- from hivenode.canvas.llm_service import call_llm, generate_confirmation_message
- from hivenode.canvas.mutation_applier import apply_mutation

Classes:
- CanvasChatRequest: Request to chat with canvas (natural language → IR mutations).
- CanvasChatResponse: Response from canvas chat with mutations and confirmations.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
