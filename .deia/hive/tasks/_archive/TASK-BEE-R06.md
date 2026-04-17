# TASK-BEE-R06: Channel System + Chat + Efemera

**Assigned to:** BEE (Sonnet)
**From:** Q33NR
**Date:** 2026-03-23
**Wave:** A (parallel with R01-R05, R07-R09)

---

## Objective

Audit the channel/chat/messaging system. Compare old efemera chat + channel infrastructure against what exists in shiftcenter now.

## Old Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\` — look for chat/, channels/, compose/, messaging/
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\` — look for chat/, message/

## New Repo Locations

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\` — chat mode rendering
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\` — channelsAdapter.ts, membersAdapter.ts
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\` — relayPoller.ts
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\` — store.py, routes.py
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md`

## Specific Questions

1. Does clicking a channel in Efemera EGG load messages?
2. Does channel selection update the text pane in Chat EGG?
3. Do system messages bleed across panes?
4. Is chat bubble rendering working correctly?
5. Does the old efemera-compose applet exist in any form?
6. Is there a channel creation flow? Channel management?
7. How does message persistence work? localStorage? SQLite? Nothing?
8. Compare old chat system features vs new — what's missing?

## Output Format

YAML frontmatter + sections. Write to: `.deia/hive/responses/2026-03-23-BEE-R06-RESPONSE-channels-chat.md`
Append to shared log.

## Shared Log

Append interesting findings to `.deia/hive/coordination/2026-03-23-RESEARCH-FINDINGS-LOG.md`.
Format: `### [HH:MM] BEE-R06 | [SEVERITY] | CATEGORY\n\nOne-liner.\n\n---`
SEVERITY: [CRIT], [WARN], [NOTE], [FYI]. CATEGORY: MISSING, BROKEN, REGRESSED, REDUNDANT-BUILD, ALREADY-FIXED, QUALITY, SECURITY.

## IMPORTANT
- READ-ONLY research. Do NOT modify code. Do NOT commit.
