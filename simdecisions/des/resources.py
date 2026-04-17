"""
resources
=========

Resource Manager — ADR-008 / TASK-082

Resource allocation with queuing disciplines, preemption modes, and
multi-unit resources for the DES engine.

Components:
    QueueDiscipline  -- 6 queue ordering strategies
    PreemptionMode   -- 4 preemption behaviours
    QueuedRequest    -- a waiting request in a resource queue
    ResourceState    -- runtime state of a single resource
    ResourceManager  -- central manager for registration, acquire/release,
                        queuing, preemption, and snapshot/restore

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Optional
- from simdecisions.phase_ir.primitives import Resource

Classes:
- QueueDiscipline: Ordering strategy for the resource wait queue.
- PreemptionMode: What happens to the preempted holder.
- QueuedRequest: A request waiting in a resource queue.
- ResourceState: Runtime state of a single managed resource.
- ResourceManager: Central manager for simulation resources.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
