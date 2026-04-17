# SPEC: RAG indexer E2E verification

## Priority
P0.60

## Model Assignment
haiku

## Objective
Run full RAG indexer test suite to verify all rebuild tasks restored functionality. Fix any remaining import/assertion issues.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R12-rag-indexer-e2e-verify.md`

## Acceptance Criteria
- [ ] 130+ core RAG tests passing across 6 modules
- [ ] Scanner: 41, Storage: 22, Embedder: 27, Indexer service: 13, Sync: 10, Models: 17
- [ ] No import errors in RAG test suite
- [ ] Optional module failures documented
