# BRIEFING: Write RAG Pipeline Task Files

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-14
**Priority:** HIGH

---

## Objective

Write 13 task files (TASK-110 through TASK-122) based on the approved decomposition document.

## Source Document

Read the approved decomposition at:
`.deia/hive/responses/20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

This decomposition is **APPROVED AS-IS**. No changes. Write one task file per task entry.

## Task File Location

All task files go to: `.deia/hive/tasks/`

Naming: `2026-03-14-TASK-{NUMBER}-{SHORT-NAME}.md`

Example: `2026-03-14-TASK-110-INDEXER-MODELS-SCANNER.md`

## Task File Format

Each task file MUST follow this structure:

```markdown
# TASK-{NUMBER}: {Title}

**Wave:** {N}
**Model:** {sonnet|haiku}
**Role:** bee
**Depends on:** {list of prerequisite TASK numbers, or "None"}

---

## Objective

{1-2 sentence description of what the bee must deliver}

## Source Spec

Port from: `docs/specs/SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `.deia/hive/responses/20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Create

{Exact file paths from decomposition}

## Files to Modify

{Exact file paths, or "None"}

## Deliverables

{Copy deliverables section from decomposition — every class, method, formula}

## Tests

{Test file paths and minimum test counts from decomposition}

## Acceptance Criteria

- [ ] All listed files created
- [ ] All tests pass (`python -m pytest {test_path} -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same algorithms, same formulas
- [ ] TDD: tests written first
```

## Task Numbers and Names

| Number | Short Name | Wave |
|--------|-----------|------|
| TASK-110 | INDEXER-MODELS-SCANNER | 1 |
| TASK-111 | ENHANCED-CHUNKERS | 1 |
| TASK-112 | TFIDF-EMBEDDER | 1 |
| TASK-113 | INDEXER-STORAGE | 2 |
| TASK-114 | INDEXER-SERVICE | 2 |
| TASK-115 | RELIABILITY-METRICS | 3 |
| TASK-116 | MARKDOWN-CLOUD-SYNC | 3 |
| TASK-117 | SYNC-DAEMON | 3 |
| TASK-118 | VOYAGE-BOT-EMBEDDINGS | 4 |
| TASK-119 | ENTITY-VECTORS | 4 |
| TASK-120 | ENTITY-ROUTES | 4 |
| TASK-121 | BOK-SYNTHESIZER | 5 |
| TASK-122 | RAG-INTEGRATION | 6 |

## Rules

1. Every deliverable from the decomposition MUST appear in the task file. Do not summarize or omit.
2. Include exact file paths (absolute paths).
3. Include model assignment per task.
4. Include dependency chain.
5. Do NOT dispatch any bees. Write task files ONLY.

## Completion

When done, list all 13 task files created with their paths.
