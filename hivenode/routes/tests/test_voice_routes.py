"""
test_voice_routes
=================

Tests for voice input API routes.

Tests the integration between voice input frontend and command interpreter backend.
Covers:
- POST /api/voice/parse endpoint
- Request/response validation
- Command parsing integration
- PRISM-IR emission
- Error handling
- WebSocket streaming (optional)

Dependencies:
- import pytest
- from fastapi import FastAPI
- from fastapi.testclient import TestClient
- from unittest.mock import Mock, patch
- from hivenode.routes import voice_routes
- from hivenode.shell.command_interpreter import CommandInterpreter
- from hivenode.shell.prism_emitter import PRISMEmitter
- from hivenode.ledger.writer import LedgerWriter
- from hivenode.dependencies import get_ledger_writer, verify_jwt_or_local

Classes:
- TestVoiceParseEndpoint: Tests for POST /api/voice/parse endpoint.
- TestVoiceParseErrorHandling: Tests for error handling in voice parse endpoint.
- TestVoiceParseLogging: Tests for logging of voice commands.
- TestVoiceParseIntegration: Integration tests with real CommandInterpreter and PRISMEmitter.

Functions:
- mock_ledger(): Mock ledger writer for tests.
- mock_user(): Mock authenticated user for tests.
- client(): Test client for voice routes.
- mock_interpreter(): Mock CommandInterpreter for testing.
- mock_emitter(): Mock PRISMEmitter for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
