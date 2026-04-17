# ShiftCenter Task Registry

**Status:** LIVING DOCUMENT
**Last Updated:** 2026-03-10

This is the planning source of truth. Every task is registered here before a task file is written. Never write a task file for something not in this registry.

---

## Active Tasks

| ID | Title | Status | Assigned | Wave |
|----|-------|--------|----------|------|
| TASK-001 | Port Event Ledger (schema, writer, reader, aggregation, export) | QUEUED | TBD | 0 |

## Completed Tasks

(none yet — this is a fresh repo)

## Planned (not yet queued)

| ID | Title | Depends On | Priority |
|----|-------|------------|----------|
| TASK-002 | ra96it.com auth MVP (register, login, MFA, JWT) | TASK-001 (ledger for auth audit) | P0 |
| TASK-003 | Named Volume System (local:// + cloud:// minimum) | TASK-001, TASK-002 | P0 |
| TASK-004 | LLM Router + sensitivity gate + BYOK | TASK-001 | P0 |
| TASK-005 | relay_bus (browser-side pub/sub) | TASK-001 | P1 |
| TASK-006 | gate_enforcer (5-disposition policy engine) | TASK-001, TASK-005 | P1 |
| TASK-007 | split_pane + applet_shell (port from old repo) | TASK-005 | P1 |
| TASK-008 | egg_loader (port + verify) | TASK-007 | P1 |
| TASK-009 | text-pane primitive (P-01) | TASK-007, TASK-008 | P2 |
| TASK-010 | terminal primitive (P-04) | TASK-007, TASK-008 | P2 |
| TASK-011 | tree-browser primitive (P-07) | TASK-007, TASK-008 | P2 |
| TASK-012 | dashboard primitive (P-15) | TASK-007, TASK-008 | P2 |
| TASK-013 | AI Chat App EGG config | TASK-009, TASK-010, TASK-011, TASK-012, TASK-004 | P2 |
