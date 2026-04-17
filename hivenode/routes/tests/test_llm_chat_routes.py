"""
test_llm_chat_routes
====================

Tests for LLM chat streaming routes.

Tests the POST /api/llm/chat/stream endpoint that provides
Server-Sent Events (SSE) streaming for LLM responses.

Dependencies:
- import asyncio
- import json
- from unittest.mock import patch
- import pytest
- from fastapi import FastAPI
- from fastapi.testclient import TestClient
- from hivenode.routes.llm_chat_routes import router

Functions:
- client(): Test client fixture.
- test_stream_command_routing(client): Test that 'command' type routes to command-interpreter.
- test_stream_question_routing(client): Test that 'question' type routes to Claude API.
- test_stream_code_routing(client): Test that 'code' type routes to code-specialized model.
- test_stream_invalid_type(client): Test error handling for invalid message type.
- test_stream_empty_message(client): Test error handling for empty message.
- test_stream_network_error(client): Test error handling for network/API errors.
- test_stream_sse_format(client): Test that SSE format is correct (data: prefix, double newlines).
- test_stream_with_history(client): Test streaming with conversation history.
- test_stream_timeout(client): Test timeout handling for long-running streams.
- test_command_confidence_levels(client): Test different confidence levels trigger appropriate responses.
- test_stream_multiple_clients(client): Test that multiple concurrent clients work correctly.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
