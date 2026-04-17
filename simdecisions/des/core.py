"""
core
====

DES Core Engine — ADR-008

Discrete Event Simulation engine with priority queue, simulation clock,
configurable stop conditions, and event-driven main loop.

All components are pure Python dataclasses/classes — NOT ORM models.
This is pure computation, no database dependencies.

Components:
    ScheduledEvent  — a single event on the queue
    EventQueue      — priority queue sorted by (sim_time, priority, sequence_id)
    SimulationClock — tracks simulation time and wall clock
    SimConfig       — run configuration (seed, limits, mode)
    EngineState     — complete simulation state
    process_event   — dispatch to event-type handlers
    run             — main event loop
    load_flow       — create initial state from a PHASE-IR Flow

Dependencies:
- from __future__ import annotations
- import heapq
- import time
- import uuid
- from dataclasses import dataclass, field
- from typing import Any, Callable, Optional
- from simdecisions.des.edges import evaluate_edges

Classes:
- ScheduledEvent: A single event scheduled on the event queue.
- EventQueue: Priority queue for simulation events.
- SimulationClock: Tracks simulation time and wall clock.
- SimConfig: Simulation run configuration.
- EngineState: Complete simulation state.

Functions:
- create_stop_condition(config: SimConfig): Create a stop predicate from *config* limits.
- _flow_as_dict(flow): Convert Flow object to dict if needed.
- _sample_duration(node: dict, state: EngineState): Sample duration from node's distribution config.
- handle_token_create(event: ScheduledEvent, state: EngineState): Create a new token at a source node.
- handle_token_arrive(event: ScheduledEvent, state: EngineState): Token arrives at a node — schedule ``node_start``.
- _emit_node_executed(event: ScheduledEvent, state: EngineState, node: Optional[dict], cost_usd: float = 0.0): Emit a ledger event for node execution (training data).
- handle_node_start(event: ScheduledEvent, state: EngineState): Start processing at a node.
- _compute_node_cost(node: dict, state: EngineState, duration: float): Compute the cost in USD for a node execution.
- handle_node_end(event: ScheduledEvent, state: EngineState): Node finished processing — route token to outgoing edges.
- handle_renege_timeout(event: ScheduledEvent, state: EngineState): Token reneges (abandons) from a resource queue after timeout.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
