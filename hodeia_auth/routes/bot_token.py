"""
bot_token
=========

Bot token API routes.

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException, status
- from sqlalchemy.orm import Session
- from pydantic import BaseModel
- from typing import Optional
- from datetime import datetime
- from hodeia_auth.dependencies import get_current_user
- from hodeia_auth.db import get_session
- from hodeia_auth.services.bot_token import BotTokenService
- from hodeia_auth.models import User

Classes:
- CreateBotTokenRequest: Request to create a bot token.
- BotTokenResponse: Bot token metadata (without the actual token).
- CreateBotTokenResponse: Response when creating a bot token (includes full token).
- BotTokenInfoResponse: Response for getting bot token info.
- RevokeBotTokenResponse: Response when revoking a bot token.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
