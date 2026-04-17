"""
llm_chat_routes
===============

LLM chat streaming routes.

Provides Server-Sent Events (SSE) endpoint for streaming LLM responses.
Routes messages to appropriate backends:
- command → local command-interpreter
- question → Claude API
- code → Claude API with code-specialized system prompt

Dependencies:
- import asyncio
- import json
- import logging
- import os
- from typing import AsyncGenerator, Literal, Optional
- import anthropic
- from fastapi import APIRouter
- from fastapi.responses import StreamingResponse
- from pydantic import BaseModel, Field
- from hivenode.shell.command_interpreter import CommandInterpreter

Classes:
- ChatMessage: Message in conversation history.
- ChatStreamRequest: Request body for streaming chat endpoint.

Functions:
- get_command_interpreter(): Get or create command interpreter instance.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
