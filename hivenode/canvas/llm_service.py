"""
llm_service
===========

Canvas LLM Service - Natural language process building via Claude.

Translates user chat messages into PHASE-IR mutations using tool-calling.

Dependencies:
- import os
- from typing import Dict, List, Optional, Any
- from dataclasses import dataclass

Classes:
- LLMResponse: Response from LLM including tool calls and text.

Functions:
- _format_flow_for_prompt(flow_ir: Dict[str, Any]): Format flow IR for inclusion in system prompt.
- generate_confirmation_message(mutations: List[Dict[str, Any]]): Generate a confirmation message with [node_id] refs when LLM doesn't provide one.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
