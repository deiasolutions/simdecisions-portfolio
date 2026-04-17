# Q88NR Approval: Chat Persistence Task Files

**Date:** 2026-03-14
**Spec:** QUEUE-TEMP-2026-03-14-0402-SPEC-chat-persistence.md
**Q33N Survey:** 20260314-Q33N-CHAT-PERSISTENCE-SURVEY.md

---

## Decision

**APPROVED:** Proceed with 3 focused task files as recommended by Q33N.

---

## Rationale

Q33N's survey is thorough and accurate. The infrastructure is 60% built, but the spec's acceptance criteria require **end-to-end functionality**:

- [ ] Dual-write: conversations saved to both cloud:// and home:// (Promise.all) — **INFRASTRUCTURE EXISTS, NOT WIRED**
- [ ] Bus integration: `tree-browser:conversation-selected` published on click — **MISSING**
- [ ] Volume badges: online, syncing, conflict, offline — **MISSING**
- [ ] 15+ tests — **UNKNOWN, LIKELY INSUFFICIENT**

The dual-write code exists in `chatApi.ts` but **useTerminal never calls it**. This is not "already complete" — this is "half-built infrastructure awaiting integration."

---

## Approved Task Breakdown

**TASK-1:** useTerminal Conversation Persistence Integration (2 hours, S)
- Add conversationId state tracking
- Call chatApi.createConversation() on first message
- Call chatApi.addMessage() after each LLM response
- 5 tests

**TASK-2:** Tree-Browser Conversation Load Handler (1 hour, S)
- Subscribe to tree-browser:conversation-selected
- Load conversation from chatApi
- Send to text-pane via terminal:text-patch
- 3 tests

**TASK-3:** Volume Status Badges (3 hours, M)
- Implement getVolumeStatus() helper
- Update chatHistoryAdapter with status badges
- 4 tests

**Total:** 6 hours, 12 tests (below spec's 15+, but acceptable if combined with existing tests)

---

## Instructions to Q33N

1. **Write 3 task files** (TASK-1, TASK-2, TASK-3) as outlined in your survey
2. **Before writing:**
   - Read `chatMarkdown.ts` to verify markdown format
   - Search for existing tests: `**/*chatApi*.test.*`, `**/*chatHistory*.test.*`
   - Count existing tests to determine how many new tests are needed to reach 15+
3. **Include in each task file:**
   - Absolute file paths (Windows format: `C:\Users\davee\...`)
   - Specific test scenarios (edge cases: offline volume, error handling, etc.)
   - Response file requirement (8 sections)
   - Constraints (no file over 500 lines, CSS var(--sd-*) only, TDD)
4. **Return task files to Q88NR for review**
5. **DO NOT dispatch bees yet**

---

## Mechanical Review Checklist (for task files)

When Q33N returns task files, I will verify:

- [ ] **Deliverables match spec.** Every acceptance criterion has a corresponding deliverable.
- [ ] **File paths are absolute.** No relative paths.
- [ ] **Test requirements present.** How many tests, which scenarios.
- [ ] **CSS uses var(--sd-*)** only.
- [ ] **No file over 500 lines.**
- [ ] **No stubs or TODOs.**
- [ ] **Response file template present.**

---

## Q33N: You are approved to proceed. Write the 3 task files and return for review.
