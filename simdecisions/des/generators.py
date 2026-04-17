"""
generators
==========

Generator and GeneratorManager for DES Engine — TASK-036.

Generators create tokens over time using statistical distributions for
inter-arrival times. Each generator can sample entity attributes from
distributions and respects active time windows.

Components:
    Generator        — generates arrivals using a distribution
    GeneratorManager — manages multiple generators for a simulation run
    GENERATOR_ARRIVAL_PRIORITY — event priority for generator arrivals

Dependencies:
- from __future__ import annotations
- from .distributions import create_distribution, RNGManager
- from .core import EventQueue

Classes:
- Generator: Generates arrivals using a distribution for inter-arrival times.
- GeneratorManager: Manages multiple generators for a simulation run.

Functions:
- _parse_time(val): Parse time value to float. Handles 'HH:MM' strings and plain numbers.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
