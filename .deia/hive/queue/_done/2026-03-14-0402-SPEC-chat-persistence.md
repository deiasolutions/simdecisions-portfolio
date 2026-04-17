# SPEC: HIVENODE-E2E Wave 4 — Chat Persistence + Conversation Navigator

## Priority
P1

## Objective
Rewrite chat persistence to dual-write to cloud:// and home://. Build tree-browser conversation navigator. Full context in `docs/specs/SPEC-HIVENODE-E2E-001.md` Sections 7-8.

## Context
Conversations stored as markdown files at `cloud://chats/YYYY-MM-DD/conversation-<uuid>.md` and `home://chats/...`. Tree-browser shows conversations grouped by volume and date.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` — Sections 7-8
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` — current chat flow
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` — tree-browser adapter pattern

## Acceptance Criteria
- [ ] Dual-write: conversations saved to both cloud:// and home:// (Promise.all)
- [ ] Graceful degradation: if one volume fails, other succeeds
- [ ] Markdown format with frontmatter (id, title, created, updated, model, volume)
- [ ] Tree-browser conversation navigator shows chats grouped by date
- [ ] Bus integration: `tree-browser:conversation-selected` published on click
- [ ] Volume badges: online, syncing, conflict, offline
- [ ] Volume preference per conversation: cloud+home, work+cloud, home-only
- [ ] 15+ tests
- [ ] No file over 500 lines

## Model Assignment
sonnet

## Constraints
- Depends on cloud storage adapter and volume sync being functional
- Tree-browser reads metadata only, NOT full conversation content
- Markdown format must be human-readable and grep-searchable
