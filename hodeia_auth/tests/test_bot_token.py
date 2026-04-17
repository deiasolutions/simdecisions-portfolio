"""
test_bot_token
==============

Tests for bot token CRUD system.

Dependencies:
- import hashlib
- import pytest
- from datetime import datetime, UTC, timedelta
- from sqlalchemy import select
- from hodeia_auth.models import User, BotToken
- from hodeia_auth.services.bot_token import BotTokenService

Classes:
- TestBotTokenGeneration: Test token generation format and hashing.
- TestBotTokenCreation: Test bot token creation.
- TestBotTokenVerification: Test bot token verification.
- TestBotTokenRevocation: Test bot token revocation.
- TestBotTokenInfo: Test getting bot token info.

Functions:
- user(db_session): Create a test user.
- second_user(db_session): Create a second test user.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
