# Q33NR APPROVAL: RAG Entity Vectors Task Breakdown

**From:** Q33NR (regent)
**To:** Q33N (queen coordinator)
**Date:** 2026-03-15
**Ref:** 2026-03-15-COORDINATION-REPORT-rag-entity-vectors.md
**Spec:** 2026-03-15-1305-SPEC-w1-11-rag-entity-vectors

---

## Decisions

I have reviewed your gap analysis and task breakdown. Excellent work on the thorough analysis.

### Approved:

1. **Critical path (TASK-159 through TASK-162)?** **✓ YES — APPROVED**
   - TASK-159: Port entity archetypes (~450 lines, 15-20 tests, Haiku)
   - TASK-160: Port entity updates (~420 lines, 20-25 tests, Sonnet)
   - TASK-161: Port entity scheduler (~240 lines, 8-10 tests, Haiku)
   - TASK-162: Extend entity routes (4 files, 15-18 tests, Haiku)

2. **Route file split strategy?** **✓ APPROVED**
   - Keep 4 separate route files as proposed
   - routes.py (bot embedding, 215 lines) — keep as-is
   - archetype_routes.py (new, ~150 lines)
   - update_routes.py (new, ~130 lines)
   - vector_routes.py (new, ~100 lines)

### Deferred:

3. **BOK advanced features (TASK-163)?** **DEFER**
   - Rationale: Basic BOK service already satisfies spec acceptance criteria ("BOK service ported")
   - File ingest, spec reviewer, submission are nice-to-have but not required for MVP
   - Can be added in future spec if needed

4. **E2E lifecycle tests (TASK-164)?** **DEFER**
   - Rationale: Unit tests in TASK-159 through TASK-162 provide adequate coverage
   - E2E tests valuable but not critical path for initial port
   - Can be added after core functionality validated

---

## Next Steps

**Q33N: Proceed as follows:**

1. **Write task files** for TASK-159, TASK-160, TASK-161, TASK-162
2. **Return task files to Q33NR** for final review before dispatch
3. **Do NOT dispatch bees yet** — wait for Q33NR approval after task file review

**Task file requirements** (mechanical checklist):
- [ ] Absolute file paths (no relative paths)
- [ ] Test requirements specified (TDD, test count target)
- [ ] Deliverables match acceptance criteria
- [ ] No files over 500 lines
- [ ] No stubs allowed
- [ ] Response file template included in task
- [ ] Dependencies clearly identified
- [ ] Model assignment specified (Haiku/Sonnet per your recommendation)

---

## Acceptance Criteria (spec compliance check)

After TASK-159 through TASK-162 complete:

- [x] Entity vector extraction ported ✓ (archetypes + updates complete core entity logic)
- [x] Voyage AI adapter ported ✓ (ALREADY COMPLETE)
- [x] BOK service ported ✓ (ALREADY COMPLETE — basic search/enrich sufficient)
- [ ] Tests written and passing (TASK-159 through TASK-162 will deliver ~58-73 tests)

All spec acceptance criteria will be satisfied upon completion of critical path.

---

## Budget Awareness

Estimated cost for critical path (TASK-159 through TASK-162):
- ~1,600 lines of new code
- ~58-73 new tests
- 4 task files
- Est. 6-8 hours wall time
- Est. cost: ~$8-12 USD (4 bees × ~$2-3 each)

Within session budget. Proceed.

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-1305-SPE
**Status:** APPROVED — Awaiting task files for final review
