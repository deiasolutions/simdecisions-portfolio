# SPEC: MCP Queue — Documentation

## Priority
P2

## Depends On
MCP-QUEUE-05

## Objective
Update process docs, deployment guides, and create spec document to capture the MCP queue notification architecture.

## Context
Tasks 01-05 implemented and tested the MCP notification system. This task documents architecture, operational procedures, and deployment steps.

Design doc: `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
Task file: `.deia/hive/tasks/2026-04-06-TASK-MCP-QUEUE-06-documentation.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` — design doc
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/processes/PROCESS-LIBRARY-V2.md` — existing process format
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-06-TASK-MCP-QUEUE-06-documentation.md` — full task spec with templates

## Acceptance Criteria
- [ ] P-SCHEDULER.md process doc (scheduler daemon + MCP event flow)
- [ ] P-DISPATCHER.md process doc (dispatcher daemon + MCP counters)
- [ ] SPEC-MCP-QUEUE-NOTIFICATIONS.md canonical spec archived
- [ ] Deployment guide updates (Railway + local dev)
- [ ] Troubleshooting sections for common MCP issues
- [ ] All CLI examples tested and working
- [ ] No file over 500 lines

## Smoke Test
- [ ] All docs readable, links valid
- [ ] CLI examples from docs copy-paste into terminal

## Model Assignment
haiku

## Constraints
- Follow existing docs style
- Include ASCII diagrams for event flows
- All examples copy-pasteable
- No stubs — all docs complete
- Response file: `.deia/hive/responses/20260406-TASK-MCP-QUEUE-06-RESPONSE.md`
