# DES Engine Port Comparison: Platform → ShiftCenter

**Date:** 2026-03-14
**Source repo:** `platform/efemera/src/efemera/` (des/ + phase_ir/)
**Target repo:** `shiftcenter/engine/` (des/ + phase_ir/)

## Line Count Summary

| Component | Platform (old) | ShiftCenter (new) | Delta |
|-----------|---------------:|------------------:|------:|
| DES engine (`des/`) | 7,842 | 7,710 | -132 |
| PHASE-IR (`phase_ir/`) | 6,463 | 1,365 | -5,098 |
| **Total source** | **14,305** | **9,075** | **-5,230** |
| Tests | — | 11,827 | +11,827 |

## DES Core — Nearly Identical Port

The DES simulation engine is a faithful 1:1 port. All 17 modules match line-for-line:

| File | Platform | ShiftCenter | Notes |
|------|----------|-------------|-------|
| core.py | 673 | 673 | Identical |
| engine.py | 481 | 481 | Identical |
| tokens.py | 578 | 578 | Identical |
| resources.py | 600 | 600 | Identical |
| distributions.py | 749 | 749 | Identical |
| edges.py | 420 | 420 | Identical |
| checkpoints.py | 430 | 430 | Identical |
| statistics.py | 481 | 481 | Identical |
| generators.py | 276 | 276 | Identical |
| pools.py | 432 | 432 | Identical |
| dispatch.py | 445 | 445 | Identical |
| loader_v2.py | 202 | 202 | Identical |
| replication.py | 585 | 585 | Identical |
| sweep.py | 542 | 542 | Identical |
| replay.py | 289 | 289 | Identical |
| trace_writer.py | 350 | 350 | Identical |
| `__init__.py` | 8 | 31 | ShiftCenter adds exports |

**Difference:** Platform had `engine_routes.py` (265 lines) — moved to `hivenode/routes/sim.py` in ShiftCenter. ShiftCenter added `ledger_adapter.py` (146 lines) for three-currency ledger integration.

## PHASE-IR — NOT Ported (except DES dependencies)

PHASE-IR was **not ported** to ShiftCenter. The only files that came over are the expression engine and primitives — the bare minimum the DES engine imports for guard evaluation. The actual PHASE-IR system (PIE runtime, validation, BPMN compiler, node types, etc.) remains in the platform repo only.

**Ported: 1,365 / 6,463 lines (21%) — only what DES depends on.**

The following platform modules were **not ported**:

| Platform-only file | Lines | Purpose |
|---|---:|---|
| bpmn_compiler.py | 536 | BPMN XML → PHASE-IR compiler |
| cli.py | 578 | Standalone CLI entry point |
| formalism.py | 399 | Formal verification / proof rules |
| mermaid.py | 423 | Mermaid diagram export |
| node_types.py | 705 | Extended node type registry |
| pie.py | 546 | Process Instance Engine (runtime) |
| schema.py | 243 | JSON schema definitions |
| schema_routes.py | 187 | Schema validation API |
| trace.py | 420 | Trace storage engine |
| trace_routes.py | 128 | Trace retrieval API |
| validate_schema.py | 140 | Schema validation logic |
| validation.py | 614 | Flow validation rules |
| validation_routes.py | 96 | Validation API routes |
| models.py | 82 | DB models (SQLAlchemy) |
| expressions.py | 61 | Legacy shim (replaced by expressions/) |
| `__main__.py` | 4 | CLI entry point |
| **Total not ported** | **5,162** | |

### What came over (DES dependencies only)

These are not a "PHASE-IR port" — they're just the files the DES engine imports:

| File | Lines | Why DES needs it |
|------|------:|---------|
| primitives.py | 146 | Flow/Node/Edge dataclasses used by DES loader |
| expressions/evaluator.py | 350 | Guard evaluation on edges |
| expressions/lexer.py | 250 | Tokenizer for guard expressions |
| expressions/parser.py | 355 | AST parser for guard expressions |
| expressions/types.py | 163 | AST node types |
| expressions/`__init__.py` | 72 | Re-exports |

## What ShiftCenter Added

| File | Lines | Purpose |
|------|------:|---------|
| engine/des/ledger_adapter.py | 146 | Maps DES events → ShiftCenter 3-currency ledger |
| hivenode/routes/sim.py | ~480 | 16 FastAPI endpoints (from platform's engine_routes.py, expanded) |
| hivenode/schemas_sim.py | ~200 | Pydantic request/response schemas |
| tests/engine/ (20 files) | 11,827 | Comprehensive test suite |

## Port Decision Rationale

The DES core was ported in full because it's the simulation runtime — pure computation, no dependencies. The PHASE-IR tooling (BPMN compiler, Mermaid export, validation, CLI) was left behind because:

1. ShiftCenter loads flows via API, not CLI
2. BPMN import is a future feature (not needed for alpha)
3. Validation and schema checking can be added incrementally
4. Mermaid/diagram export will be handled by the frontend canvas

## Status

- **DES core:** Complete, tested (20 test files, 11,827 test lines)
- **PHASE-IR:** NOT ported. Only DES-dependency files (expressions, primitives) copied over. Full PHASE-IR system (PIE, validation, BPMN, node types, schema, CLI) remains in platform repo only.
- **Hivenode integration:** Scaffolded, blocked on TASK-071
- **If PHASE-IR port is needed:** Source is at `platform/efemera/src/efemera/phase_ir/` (5,162 lines to port)
