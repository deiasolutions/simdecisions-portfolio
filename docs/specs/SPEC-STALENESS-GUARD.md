# SPEC: Staleness Guard — Preventing Stale Specs from Overwriting Newer Work

**Author:** Q88N (Dave) × Q33NR (Opus 4.6)
**Date:** 2026-03-18
**Status:** DRAFT — needs Q88N review
**Related:** SPEC-PIPELINE-001 (Section 4: Directory State Machine, Section 5.3: Completion Validation)

---

## 1. Problem

A spec written on Day 1 describes modifications to `build_monitor.py`. On Day 2, a different spec modifies that same file and completes. On Day 3, the Day 1 spec is dispatched. The bee reads the spec (which references the Day 1 version of the file), writes code based on that stale context, and overwrites Day 2's changes.

**This happened on 2026-03-17.** Changes to the build monitor Active list that had been working for hours were silently reverted by a later bee working from an older spec.

File locking (the existing `/build/claim` system) does NOT prevent this — it only prevents two bees writing the same file *simultaneously*. A stale spec running *after* a newer one completes will correctly acquire the lock, then incorrectly overwrite the file.

---

## 2. Root Cause

Specs are written at a point in time but may be dispatched hours or days later. Nothing in the current system checks whether the codebase has changed since the spec was authored.

---

## 3. Proposed Solution: File Ledger + Pre-Dispatch Staleness Check

### 3.1 File Ledger

A persistent index tracking which spec last modified each file.

**Storage:** `.deia/hive/file-ledger.json` (also cached in hivenode at `/build/file-ledger`)

```json
{
  "hivenode/routes/build_monitor.py": {
    "last_modified_by": "SPEC-TASK-BL203-split-heartbeat",
    "spec_date": "2026-03-17T22:48:00",
    "commit": "ad06402"
  },
  "browser/src/App.tsx": {
    "last_modified_by": "SPEC-TASK-BUG031-code-explorer-click-error",
    "spec_date": "2026-03-17T23:33:00",
    "commit": "ad06402"
  }
}
```

**Who updates it:**
- The queue runner, immediately after auto-commit (BL-213). When a bee completes and its changes are committed, the queue runner updates the ledger with the files modified, the spec ID, and the commit hash.

**Fallback rebuild:** If the ledger is lost or corrupted, rebuild from git history by parsing commit messages (which BL-213 formats as `[BEE-MODEL] SPEC-ID: objective`).

### 3.2 Pre-Dispatch Staleness Check

Before dispatching a spec, the queue runner:

1. Parse the spec's `## Files to Read First` and `## File Claims` sections to identify files the bee will touch
2. For each file, check the ledger: was this file modified by a spec *newer* than the one about to be dispatched?
3. If yes → **STALE**. Do not dispatch.

**Staleness detection:**
```python
spec_date = parse_spec_date(spec.path.name)  # from filename: 2026-03-17-SPEC-...
for file_path in spec.files_to_modify:
    ledger_entry = file_ledger.get(file_path)
    if ledger_entry and ledger_entry["spec_date"] > spec_date:
        # This file was modified by a newer spec
        return STALE, ledger_entry["last_modified_by"]
```

### 3.3 Staleness Routing

| Situation | Action |
|-----------|--------|
| Spec is stale (files changed by newer spec) | Move to `_needs_review/` with staleness report |
| Spec is fresh (no conflicts) | Dispatch normally |
| Ledger unavailable | Dispatch with warning (best-effort) |

When a spec is flagged stale, append a `## Staleness Report` section:

```markdown
## Staleness Report
- Flagged: 2026-03-18T07:30:00
- Reason: Files modified by newer spec(s)
- Conflicts:
  - `hivenode/routes/build_monitor.py` — last modified by SPEC-TASK-BL203 (2026-03-17T22:48)
  - `browser/src/App.tsx` — last modified by SPEC-TASK-BUG031 (2026-03-17T23:33)
- Action needed: Human must decide — regenerate spec, merge manually, or discard
```

### 3.4 Git Blame as Backup Check

When the file ledger doesn't have an entry (legacy files, ledger gap), fall back to:

```bash
git log --oneline -1 -- <file>
```

Parse the commit message for `[BEE-MODEL] SPEC-ID:` format. Compare the spec date from the commit against the current spec's date.

---

## 4. Relationship to SPEC-PIPELINE-001

PIPELINE-001 already defines infrastructure that supports this:

| PIPELINE-001 Feature | How It Helps Staleness Guard |
|---|---|
| **Section 4.6: Manifest** | Records when a spec started executing — timestamp for provenance |
| **Section 4.7: Failure Log** | Staleness detection is a type of pre-dispatch failure |
| **Section 5.3: Completion Validation** | LLM reviews diff against acceptance criteria — could catch stale overwrites post-hoc |
| **Section 6: PipelineStore** | `move_spec()` emits events — staleness routing is a transition from `queue` to `_needs_review/` |
| **Section 3.1: Event Ledger** | Every transition emits an event — staleness checks become auditable |
| **`_active/` directory** | Specs in flight are visible — prevents duplicate dispatch |

**What PIPELINE-001 does NOT cover:**
- Pre-dispatch staleness check (it validates fidelity, not freshness)
- File-level provenance tracking (it tracks spec-level state, not file-level)
- Automatic stale routing (its `_needs_review/` is for failures, not staleness)

**This spec extends PIPELINE-001** by adding file-level provenance as a new pre-dispatch gate, slotting in between the existing priority/dependency check and the actual dispatch.

---

## 5. Implementation Phases

### Phase A: File Ledger (depends on BL-213 auto-commit)
- Create `.deia/hive/file-ledger.json`
- Queue runner updates ledger after each auto-commit
- Hivenode serves ledger via `GET /build/file-ledger`
- Rebuild-from-git-history function

### Phase B: Pre-Dispatch Staleness Check
- Parse spec files for target file lists
- Cross-reference against ledger before dispatch
- Route stale specs to `_needs_review/` with staleness report

### Phase C: Integration with PIPELINE-001
- Wire staleness check into PipelineStore's pickup logic (Section 4.3)
- Emit `spec_staleness_detected` events to Event Ledger
- Add staleness as a triage category in LLM Failure Diagnosis (Section 5.2)

---

## 6. Open Questions

1. **Spec file list extraction:** Not all specs list files they'll modify. Should we require a `## Files to Modify` section in every spec template? Or infer from scope detection?
2. **Staleness threshold:** Should we allow a grace period? (e.g., files modified within 1 hour of spec creation are OK because they were likely part of the same planning session)
3. **Auto-regeneration:** Instead of routing to `_needs_review/`, should the system auto-regenerate the spec against the current codebase? (Higher cost, but fully autonomous)
4. **Claim instructions in dispatch template:** The 30-item overnight batch was missing file claim headers. Should `dispatch.py` or `--inject-boot` automatically append claim instructions to every spec?
