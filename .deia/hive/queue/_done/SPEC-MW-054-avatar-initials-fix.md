# SPEC-MW-054-avatar-initials-fix: Fix avatar initials showing wrong letters

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set top-bar, the user avatar bubble shows "LU" as initials but the menu bar correctly shows the user is signed in as "DEIA Solutions". The initials should be "DS" (from "DEIA Solutions"), not "LU". Investigate how the top-bar avatar component extracts initials from the user profile. The user data comes from `getUser()` in `primitives/auth/authStore.ts` which reads the JWT payload. Check whether the avatar is reading the wrong field (e.g. `username` or `email` instead of `display_name`), using a stale/cached value, or computing initials incorrectly. Fix it so the avatar initials match the display name.

## Files to Read First

- browser/src/primitives/top-bar/TopBar.tsx
- browser/src/primitives/auth/authStore.ts
- browser/src/primitives/menu-bar/MenuBarPrimitive.tsx

## Acceptance Criteria

- [ ] The avatar bubble on the top-bar shows initials derived from the user's `display_name` field
- [ ] For display_name "DEIA Solutions", the initials shown are "DS"
- [ ] The initials extraction handles edge cases: single word names (first two letters), empty names (fallback to "?"), names with more than two words (first letter of first and last word)
- [ ] The menu bar user status and the top-bar avatar show consistent user identity
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk` while signed in — verify avatar initials match display name
- [ ] Check that menu bar username matches the avatar initials source

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- Do not modify the auth store or JWT payload — only fix how initials are extracted from existing user data
