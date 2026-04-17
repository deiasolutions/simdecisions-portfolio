"""
main
====

hodeia_auth FastAPI application - Authentication service MVP.

Dependencies:
- from contextlib import asynccontextmanager
- from fastapi import FastAPI, Request
- from fastapi.middleware.cors import CORSMiddleware
- from slowapi import Limiter, _rate_limit_exceeded_handler
- from slowapi.util import get_remote_address
- from slowapi.errors import RateLimitExceeded
- from hodeia_auth.db import create_tables
- from hodeia_auth.config import settings
- from hodeia_auth.routes import register, login, mfa, token, oauth, jwks, dev_login, profile, mfa_setup, recovery_email, password_reset, email_verify, sessions, bot_token
- from hivenode.relay.routes import router as relay_router

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
