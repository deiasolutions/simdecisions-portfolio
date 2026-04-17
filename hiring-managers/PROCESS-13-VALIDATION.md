# PROCESS-13: Build Integrity Validation

PROCESS-13 is the build integrity system that validates AI-generated output before it ships.

**Current Status:** Paused — currently testing DDD (Design-Driven Development) approach alongside PROCESS-13 to evaluate workflow patterns.

**What is DDD?** Design-Driven Development front-loads design decisions before implementation begins. Instead of iterative correction loops, the spec is locked and validated upfront. We're comparing defect rates and velocity between the two approaches.

---

## The Problem

AI agents make mistakes:
- Hallucinate requirements
- Skip validation steps
- Ship incomplete work
- Drift from specs

Traditional code review catches this *after* code is written. PROCESS-13 catches it *before*.

---

## The Validation Pipeline

Gate 0 — Prompt to Spec: Extract requirements from user prompt, extract requirements from generated spec, compare for coverage check with no hallucinations and no orphans.

Phase 0 — Coverage: Every requirement in the assignment must appear in the spec. No out-of-scope additions without approval.

Phase 1 — Spec Fidelity: Encode spec to IR (intermediate representation), decode IR to reconstructed spec, compare with semantic similarity threshold of 0.85.

Phase 2 — Task Fidelity: Encode tasks to IR, decode IR to reconstructed tasks, compare with semantic similarity threshold of 0.85.

---

## Healing Loops

If validation fails:
1. Generate diagnostic (what's wrong, why)
2. Call LLM with healing prompt
3. Regenerate artifact
4. Re-validate
5. Max 3 retries, then escalate to human

---

## Implementation

| Component | Location |
|-----------|----------|
| Process spec | `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` |
| Validation logic | `hivenode/scheduler/integrity_check.py` (523 lines) |
| Capabilities | Orphan detection, stall detection, circular dependency detection |

---

## Why Paused?

We're currently testing DDD (Design-Driven Development) patterns to evaluate:
- Upfront design validation vs. iterative correction
- Spec quality when design is locked before implementation
- Comparison of defect rates between approaches

PROCESS-13 remains fully implemented and can be re-enabled immediately.
