"""
prism_emitter
=============

PRISM-IR emitter for Mobile Workdesk command interpreter.

Converts ParseResult objects from natural language parser into PRISM Intermediate
Representation (PRISM-IR) format for execution by the PRISM runtime.

PRISM-IR Schema:
{
    "action": str,           // Required: verb (open, close, search, etc.)
    "target": str,           // Required: object (terminal, file, pane, etc.)
    "parameters": dict,      // Optional: key-value command arguments
    "confidence": float,     // Required: 0.0-1.0 confidence score
    "mode": str,             // Required: "auto" | "confirm" | "disambiguate"
    "metadata": {            // Required: execution context and audit trail
        "original_command": str,
        "alternatives": list,
        "typo_corrected": bool,
        "confidence_score": float
    }
}

Execution Modes:
- "auto": confidence >= 0.9 — execute immediately without confirmation
- "confirm": 0.7 <= confidence < 0.9 — show confirmation prompt with command
- "disambiguate": confidence < 0.7 — show picker with alternatives

Dependencies:
- import json
- from hivenode.shell.command_interpreter import ParseResult

Classes:
- EmissionError: Exception raised when PRISM-IR emission fails.
- PRISMEmitter: Converts ParseResult to PRISM-IR format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
