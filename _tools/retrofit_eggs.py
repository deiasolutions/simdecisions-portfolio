"""
retrofit_eggs
=============

Retrofit all EGG files to ADR-SC-CHROME-001 v3 format.
Remove old hide* flags, devOverride, masterTitleBar, workspaceBar, shellTabBar.
Replace with new ui block format (chromeMode, commandPalette, akk only).

Dependencies:
- import json
- import re
- from pathlib import Path

Functions:
- extract_block(content: str, block_name: str): Extract a fenced block and its position.
- retrofit_ui_block(content: str): Replace ui block with new format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
