# SPEC: AUTH-A — LoginPage rebrand ra96it to hodeia

## Priority
P1

## Objective
Rebrand LoginPage.tsx from ra96it to hodeia: replace VITE_RA96IT_API env var with VITE_AUTH_API, update all UI text from ra96it to hodeia or neutral language, update tests.

## Context
LoginPage currently references VITE_RA96IT_API and displays ra96it branding throughout UI (logo text, subtitles, logged-in messages). OAuth flow is already domain-agnostic. This is purely branding: rename env var to generic, replace ra96it text with hodeia.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts

## Deliverables
- [ ] Replace VITE_RA96IT_API with VITE_AUTH_API in LoginPage.tsx
- [ ] Update all UI text: ra96it to hodeia (logo text, subtitles, logged-in messages)
- [ ] Keep GitHub branding and consent flow unchanged
- [ ] Update LoginPage tests to verify new env var name
- [ ] Add test cases verifying UI displays hodeia instead of ra96it

## Acceptance Criteria
- [ ] VITE_RA96IT_API replaced with VITE_AUTH_API
- [ ] All instances of ra96it in UI text replaced with hodeia or neutral language
- [ ] GitHub branding unchanged
- [ ] Tests pass: existing + new test cases for env var and UI text
- [ ] No references to VITE_RA96IT_API remain in LoginPage.tsx or its tests

## Model Assignment
haiku

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD
- Do NOT change OAuth flow logic — only env var name and UI text
- Do NOT change localStorage keys (separate task)
