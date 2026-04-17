# SPEC: Subdomain -> EGG Routing

## Priority
P1

## Objective
Add hostname -> EGG mapping so different subdomains load different products from the same deploy.

## Context
Files to read first:
- `browser/src/App.tsx` or `browser/src/main.tsx`
- `browser/src/shell/useEggInit.ts`
- `eggs/` directory for available EGGs

## Acceptance Criteria
- [ ] Mapping in App.tsx or useEggInit.ts:
  - chat.efemera.live -> chat.egg.md
  - code.shiftcenter.com -> code.egg.md (when it exists, fallback to chat)
  - pm.shiftcenter.com -> pm.egg.md (when it exists, fallback to chat)
  - canvas.shiftcenter.com -> canvas.egg.md
  - dev.shiftcenter.com -> chat.egg.md (default)
  - localhost:5173 -> chat.egg.md (dev default)
- [ ] ?egg=name query param overrides hostname mapping
- [ ] Unknown hostname falls back to chat.egg.md
- [ ] 5+ tests

## Smoke Test
- [ ] dev.shiftcenter.com loads chat app
- [ ] dev.shiftcenter.com?egg=canvas loads canvas app
- [ ] localhost:5173?egg=monitor loads build monitor

## Depends On
- w3-02-dev-shiftcenter-dns

## Model Assignment
haiku
