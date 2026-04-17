"""
mfa
===

MFA service using Twilio Verify API.

Dependencies:
- from typing import Literal
- from twilio.rest import Client
- from hodeia_auth.config import settings

Functions:
- get_twilio_client(): Get Twilio client instance.
- send_mfa_code(to: str,
    method: Literal["sms", "email"],): Send MFA code via Twilio Verify.
- verify_mfa_code(to: str,
    code: str,): Verify MFA code via Twilio Verify.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
