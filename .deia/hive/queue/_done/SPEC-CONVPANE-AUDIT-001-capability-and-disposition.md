# SPEC-CONVPANE-AUDIT-001: Conversation-Pane Capability & Disposition Audit

## Priority

P2

## Depends On

None

## Model Assignment

sonnet

## Objective

The prior audit in `SPEC-MOBILE-SUBMIT-001` concluded that `ConversationPane.tsx` is "display-only, never wired." That audit was correct about `ConversationPane.tsx` itself but **missed `useLLMRouter.ts` in the same folder**, which is a 413-line LLM routing hook (SSE streaming, exponential-backoff retry, command routing to `/api/prism/parse`, chat routing to `/api/llm/chat/stream`). The hook is live, fully implemented code but is never called by the adapter that exposes the pane as an app.

Before anything in `browser/src/primitives/conversation-pane/` is deleted, we need a capability-and-disposition audit of the whole folder, a comparison with the terminal primitive (which is the actual working chat path), and a clear per-component recommendation: **WIRE** (keep and connect properly), **SALVAGE** (keep but move to a better location), or **DEPRECATE** (safe to remove, document what deps go with it).

The deliverable is a report that lets Q88N decide the disposition, followed by ranked follow-on implementation specs.

## Files to Read First

browser/src/primitives/conversation-pane/ConversationPane.tsx
browser/src/primitives/conversation-pane/useLLMRouter.ts
browser/src/primitives/conversation-pane/ActionButton.tsx
browser/src/primitives/conversation-pane/CodeBlock.tsx
browser/src/primitives/conversation-pane/FileAttachment.tsx
browser/src/primitives/conversation-pane/ImageOutput.tsx
browser/src/primitives/conversation-pane/types.ts
browser/src/primitives/conversation-pane/index.ts
browser/src/apps/conversationPaneAdapter.tsx
browser/src/apps/index.ts
browser/src/primitives/terminal/TerminalApp.tsx
browser/src/primitives/terminal/useTerminal.ts
browser/src/primitives/terminal/terminalModes.ts
browser/src/primitives/terminal/types.ts
browser/src/primitives/terminal/useAttachment.ts
browser/src/primitives/text-pane/services/markdownRenderer.tsx
browser/src/sets/parseEggMd.ts
browser/sets/chat.set.md
browser/sets/chat2.set.md
hivenode/routes/llm_chat_routes.py
.deia/hive/responses/20260416-SPEC-MOBILE-SUBMIT-001-RESPONSE.md

## Acceptance Criteria

- [ ] Capability inventory table produced, one row per file in `browser/src/primitives/conversation-pane/` (name, LOC, purpose in one sentence, external importers count, test coverage).
- [ ] Side-by-side comparison of `useLLMRouter.ts` vs the terminal's chat routing (`useTerminal.ts` + `TerminalApp.tsx` + `terminalModes.ts`): which endpoints each calls, streaming implementation, retry logic, history/context handling, error surfacing.
- [ ] Verdict on `useLLMRouter.ts`: is it a meaningfully cleaner / more complete implementation than the terminal's routing, an equivalent duplicate, or missing features the terminal has? Cite specific line refs.
- [ ] Name-collision verification: for each of `ActionButton`, `CodeBlock`, `FileAttachment`, `ImageOutput`, determine whether the references found in `terminal/types.ts`, `terminal/useAttachment.ts`, `text-pane/services/markdownRenderer.tsx`, `sets/parseEggMd.ts` are actual imports from `conversation-pane/` or unrelated entities with the same name. Produce a reference map.
- [ ] Per-component disposition recommendation (WIRE / SALVAGE / DEPRECATE) with rationale:
  - [ ] ConversationPane.tsx
  - [ ] useLLMRouter.ts
  - [ ] ActionButton, CodeBlock, FileAttachment, ImageOutput (one row each)
  - [ ] types.ts, index.ts, conversationPaneAdapter.tsx, app registry entry at `browser/src/apps/index.ts:90`
- [ ] If WIRE is recommended for any component, concrete wiring plan: where it plugs in, which sets/apps consume it, what changes in the adapter or in `index.ts`.
- [ ] If SALVAGE is recommended for any component, target location (e.g., `browser/src/services/llmRouter.ts`) with import path changes listed.
- [ ] If DEPRECATE is recommended, list of files to remove plus any test/doc/CSS dependents that must go with them.
- [ ] Ranked follow-on implementation specs drafted (title + priority + model + one-line objective + acceptance-criteria sketch). These should be the specs Q88N dispatches **after** reading this report.
- [ ] Report includes a 3-sentence "What does Q88N decide?" framing at the top so the decision surface is obvious.

## Smoke Test

After reading the report, Q88N can answer in one sitting: (a) what does the conversation-pane folder actually do today, (b) what of it is worth keeping, (c) what's the next spec to dispatch. If any of those three answers requires more research, the report fails its smoke test.

## Constraints

- Read-only. No code changes. No file moves. No deletions.
- Do not modify `browser/src/apps/index.ts` or the adapter. Do not run `npm test`.
- Do not write the follow-on implementation specs themselves — just sketch them in the report so Q88N/Q33NR can formalize the chosen path.
- Cite file paths with line numbers when making claims (e.g., `useLLMRouter.ts:226` for the `/api/llm/chat/stream` call).
- If a claim in the prior MOBILE-SUBMIT-001 audit is contradicted by this audit, call it out explicitly with evidence.
