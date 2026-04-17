---
id: REFACTOR-010
priority: P0
model: sonnet
role: bee
depends_on: []
---
# SPEC-REFACTOR-010: Crawl Codebase — Extract All Routes, Components, Events, Configs

## Priority
P0

## Model Assignment
sonnet

## Depends On
(none)

## Intent
Crawl the entire ShiftCenter codebase and extract a structured inventory of every functional unit: API routes, React components, primitives, event bus events, configuration files, database tables, and CLI tools. This is the foundation for the retention gate — we must know exactly what exists before changing anything.

## Files to Read First
- `hivenode/` — all Python modules, especially `routes/`, `scheduler/`, `inventory/`, `efemera/`
- `browser/src/` — all TypeScript/React code, especially `primitives/`, `services/`, `shell/`
- `eggs/` — all `.set.md` files
- `_tools/` — all CLI tools
- `hodeia_auth/` — auth service

## Acceptance Criteria
- [ ] File created: `.deia/hive/refactor/inventory-routes.json` — every FastAPI route with method, path, module
- [ ] File created: `.deia/hive/refactor/inventory-components.json` — every React component with file path, type (primitive/shell/page/infrastructure)
- [ ] File created: `.deia/hive/refactor/inventory-events.json` — every bus event name, emitter, consumer
- [ ] File created: `.deia/hive/refactor/inventory-configs.json` — every .set.md, .egg.md, .yml config file
- [ ] File created: `.deia/hive/refactor/inventory-tables.json` — every database table with columns
- [ ] File created: `.deia/hive/refactor/inventory-tools.json` — every CLI tool with entry point and purpose
- [ ] Each inventory file is valid JSON with consistent schema
- [ ] Total feature count printed to stdout at end

## Constraints
- You are in EXECUTE mode. Write all output files. Do NOT enter plan mode. Do NOT ask for approval. Just do it.
- Read-only — no code changes
- Be exhaustive — every route, every component, every table. Miss nothing.
- Work on branch `refactor/auto-2026-04-07`
- No git operations
