"""
confirmation_handler
====================

Confirmation and disambiguation handler for Mobile Workdesk command interpreter.

Implements the interactive flows for handling commands based on confidence:
- Auto-execute: confidence >= 0.9
- Confirm: 0.7 <= confidence < 0.9 (show "Did you mean X?" prompt)
- Disambiguate: confidence < 0.7 (show alternatives picker)

State machine:
    PENDING → (AUTO_EXECUTE | CONFIRM | DISAMBIGUATE) → RESOLVED

Dependencies:
- from dataclasses import dataclass
- from enum import Enum
- from typing import List, Optional
- from hivenode.shell.command_interpreter import ParseResult
- from hivenode.shell.prism_emitter import PRISMEmitter

Classes:
- ResolutionAction: Actions resulting from command resolution.
- Resolution: Result of resolving a command with user interaction.
- ConfirmationHandler: Handles confirmation and disambiguation flows for command execution.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
