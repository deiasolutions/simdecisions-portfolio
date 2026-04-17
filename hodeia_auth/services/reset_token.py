"""
reset_token
===========

Password reset token service for hodeia_auth.

Dependencies:
- import hashlib
- import secrets
- from datetime import datetime, UTC, timedelta

Classes:
- PasswordResetToken: In-memory store for password reset codes (simple implementation).

Functions:
- send_reset_code(email: str, code: str): Send password reset code via recovery email (uses Twilio Verify).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
