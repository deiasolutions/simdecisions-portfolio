# BRIEFING: BUG-031 Re-Queue — Code Explorer Click Error

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Spec:** `.deia/hive/queue/2026-03-18-SPEC-REQUEUE-BUG031-code-explorer-click-error.md`
**Model:** sonnet
**Priority:** P0

---

## Situation

This is the **4th attempt** to fix BUG-031. The fix is known and documented. Previous bees claimed COMPLETE but the source code changes never landed in the actual file.

**Root cause (confirmed from 3 prior attempts):**
- `browser/src/apps/treeBrowserAdapter.tsx` sends `file:selected` bus events without:
  1. A `name` field (SDEditor expects `message.data.name`)
  2. A protocol prefix on the URI (backend `/storage/read` expects `home://path` format)

**Previous attempts:**
1. BUG-031 haiku — wrote correct fix, but changes didn't land
2. BUG-031-SONNET — same issue
3. BUG-039 fix-spec — failed due to file path error

---

## Your Mission

Write **ONE task file** for a bee to:

1. **Modify `browser/src/apps/treeBrowserAdapter.tsx`** to fix the `file:selected` event data
2. **Add tests** to verify the fix
3. **Run all affected test suites** to ensure no regressions

This is a **surgical fix**. The exact code change is documented in the spec. The bee must:
- Actually modify the source file (not just write tests)
- Add the `name` field to the event data
- Add the protocol prefix to the URI
- Verify the changes landed by reading the file back

---

## Critical Success Factors

### 1. Source Code Must Actually Change
The bee MUST:
- Use the Edit tool (not Write) to modify `treeBrowserAdapter.tsx`
- Read the file back after editing to confirm the changes landed
- Include the exact before/after diff in the response file

### 2. No Stubs, No Assumptions
- The bee must actually run the tests
- The bee must verify the file was modified
- The bee must check for regressions in related tests

### 3. Test Coverage Required
- Test that `file:selected` events include `name` field
- Test that URIs include protocol prefix (`home://`)
- Test that directory clicks don't trigger `file:selected`
- Test that SDEditor receives the correct event data

---

## Files the Bee Must Read First

1. `browser/src/apps/treeBrowserAdapter.tsx` — the file to modify
2. `browser/src/primitives/text-pane/SDEditor.tsx` — to understand what fields it expects
3. `hivenode/routes/storage_routes.py` — to confirm URI format expected

---

## Deliverables (from spec)

- [ ] treeBrowserAdapter.tsx modified with `name` field in file:selected events
- [ ] treeBrowserAdapter.tsx modified with protocol prefix on URI
- [ ] Directory clicks do NOT trigger file:selected
- [ ] Tests for file:selected event data (name, uri format)
- [ ] Tests for SDEditor receiving correct event data
- [ ] All smoke tests pass:
  - `cd browser && npx vitest run --reporter=verbose src/apps/__tests__/`
  - `cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/`
  - `cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/`

---

## Constraints (Rule Enforcement)

- **No file over 500 lines** (Rule 4)
- **CSS: var(--sd-*) only** (Rule 3) — not applicable here but enforce anyway
- **No stubs** (Rule 6)
- **TDD** (Rule 5) — tests first, then implementation
- **MUST modify source code** — not just tests

---

## Task File Requirements

Your task file MUST include:

1. **Objective** — one sentence: fix file:selected events in treeBrowserAdapter.tsx
2. **Context** — the 4 prior attempts, the known fix, the failure pattern
3. **Files to Read First** — treeBrowserAdapter.tsx, SDEditor.tsx, storage_routes.py
4. **Deliverables** — all items from spec, plus "verify changes landed by reading file back"
5. **Test Requirements** — specific test scenarios, TDD requirement
6. **Constraints** — all 10 hard rules apply
7. **Response Requirements** — all 8 sections mandatory

---

## What You Should NOT Do

- Do NOT write multiple task files. This is a single surgical fix.
- Do NOT assign this to haiku. The spec says sonnet. Use sonnet.
- Do NOT skip the "verify changes landed" deliverable. This is why we're on attempt #4.
- Do NOT approve the task until you've verified it's correct against the spec.

---

## After You Write the Task File

1. Save it to `.deia/hive/tasks/2026-03-18-TASK-BUG031-REQUEUE-fix-code-explorer-click.md`
2. Report back to Q33NR with a summary
3. Wait for Q33NR to review and approve
4. When approved, dispatch the bee with:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG031-REQUEUE-fix-code-explorer-click.md --model sonnet --role bee --inject-boot
   ```

---

## Questions?

If anything in the spec is unclear, flag it to Q33NR before writing the task file. Do NOT guess or improvise.

---

**End of Briefing**
