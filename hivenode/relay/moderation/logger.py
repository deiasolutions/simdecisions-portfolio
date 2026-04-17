"""
logger
======

Moderation logger — posts decisions to system channels (moderation-log, bugs-admin).

Dependencies:
- import logging

Functions:
- log_moderation_event(sender_id: str,
    channel_id: str,
    decision: str,
    reason: str,
    content_preview: str = "",): Write a moderation event to the moderation-log channel.
- log_error_event(error_type: str,
    error_message: str,
    context: str = "",): Write an error event to the bugs-admin channel.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
