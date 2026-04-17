# SPEC: Research — Discord integration port from Efemera to ShiftCenter

## Objective

Investigate the Discord integration in the platform/efemera codebase and produce a written assessment of what it would take to port it to shiftcenter -- or confirm it's already been ported.

Questions to answer:
1. What does it do? (bot, webhooks, OAuth, relay, etc.)
2. Has any of it already been ported to shiftcenter?
3. If not ported, what files/modules would need to come over?
4. What dependencies does it have? (Discord API keys, bot tokens, external services)
5. How much work is it? (S/M/L estimate)

## Files to Read First

- hivenode/efemera/store.py
- hivenode/efemera/routes.py

## Files to Modify

- .deia/hive/responses/20260324-SPEC-DISCORD-INTEGRATION-RESEARCH-RESPONSE.md

## Deliverables

- [ ] Written response file ONLY -- no code changes
- [ ] Response file at .deia/hive/responses/20260324-SPEC-DISCORD-INTEGRATION-RESEARCH-RESPONSE.md

## Acceptance Criteria

- [ ] Identified all Discord-related files in platform/efemera
- [ ] Checked shiftcenter for any existing Discord code
- [ ] Documented what the integration does (features, endpoints, bot commands)
- [ ] Documented dependencies (packages, env vars, external APIs)
- [ ] Provided effort estimate for porting (S/M/L with reasoning)
- [ ] Response file written to .deia/hive/responses/ with all 8 sections

## Smoke Test

- [ ] Response file written to .deia/hive/responses/20260324-SPEC-DISCORD-INTEGRATION-RESEARCH-RESPONSE.md

## Constraints

- Research only -- no code changes
- Write response file to .deia/hive/responses/
- Include all 8 response sections per BOOT.md template
- IMPORTANT: This is a RESEARCH task. Do NOT write any code. Do NOT modify any files except the response file.

## Context

Source files to investigate are in the platform repo (not in this repo):
- `platform/efemera/src/efemera/` -- look for discord/, integrations/, or similar directories
- Check for any Discord-related packages in platform requirements/dependencies

## Model Assignment

haiku

## Priority

P2
