# SPEC-MOBILE-WORKDESK-001: Mobile Workdesk Build Specification

**Status:** DRAFT  
**Author:** Q33NR (via Claude)  
**Date:** 2026-04-05  
**Target:** workdesk.set.md — responsive set, mobile-first

---

## 1. Overview

Build a mobile-first workdesk for ShiftCenter. One set file (`workdesk.set.md`) that adapts to viewport. The mobile experience is primary; desktop inherits the same primitives with expanded layouts.

**Core thesis:** The phone becomes a command center for the hive. Voice, pills, and gestures are first-class inputs. The command-interpreter (headless) routes all input to PRISM-IR execution. No paradigm split between mobile and desktop — just different input surfaces to the same brain.

---

## 2. Primitive Registry

### 2.1 New Primitives (8)

| ID | Primitive | Type | Description | Est. Hours |
|----|-----------|------|-------------|------------|
| P-NEW-01 | mobile-nav | visible | Nested hub navigation, back gesture, contextual drill-down | 16 |
| P-NEW-02 | notification-pane | visible | Home screen — things needing attention, overdue items, tap to navigate | 20 |
| P-NEW-03 | quick-actions (FAB) | visible | Movable/hideable floating action button. Kebab + mic + contextual keyboard | 12 |
| P-NEW-04 | voice-input | visible | Speech-to-text → command-interpreter. Available on mobile and desktop | 10 |
| P-NEW-05 | diff-viewer | visible | Mobile-optimized diff review, inline expand/collapse, swipe actions | 18 |
| P-NEW-06 | conversation-pane | visible | Multi-modal input/output (keyboard, pills, hero, voice), multi-LLM routing | 24 |
| P-NEW-07 | queue-pane | visible | Hivenode queue visibility — queued, running, blocked, completed | 16 |
| P-NEW-08 | command-interpreter | headless | Central brain. Parses intent, fuzzy matches context, emits PRISM-IR commands | 20 |

**Subtotal new primitives:** 136 hours

### 2.2 Existing Primitives — Mobile CSS (11)

| ID | Primitive | Current State | Mobile Work | Est. Hours |
|----|-----------|---------------|-------------|------------|
| P-MOB-01 | text-pane | Desktop-only | Responsive breakpoints, touch selection, mobile toolbar | 8 |
| P-MOB-02 | terminal | Desktop-only | Pill suggestions (TF-IDF), scrollable list, keyboard toggle | 12 |
| P-MOB-03 | tree-browser | Desktop-only | Touch-friendly rows, swipe actions, collapse/expand gestures | 8 |
| P-MOB-04 | efemera-connector | Desktop-only | Mobile channel list, compact member view | 6 |
| P-MOB-05 | settings | Desktop-only | Full-screen mobile layout, touch-friendly controls | 4 |
| P-MOB-06 | dashboard | Desktop-only | Compact currency display, collapsible sections | 6 |
| P-MOB-07 | progress-pane | Has MobileStageView | Minor polish, integrate with mobile-nav | 4 |
| P-MOB-08 | top-bar | Desktop-only | Mobile-optimized, hamburger integration | 4 |
| P-MOB-09 | menu-bar | Desktop-only | Convert to slide-out drawer on mobile | 6 |
| P-MOB-10 | status-bar | Desktop-only | Compact single-line mobile variant | 3 |
| P-MOB-11 | command-palette | Desktop-only | Full-screen mobile overlay, touch-friendly | 6 |

**Subtotal mobile CSS:** 67 hours

### 2.3 Terminal Enhancement

| ID | Feature | Description | Est. Hours |
|----|---------|-------------|------------|
| T-ENH-01 | Suggestive typing | TF-IDF index on command history, paths, names. No LLM. | 8 |
| T-ENH-02 | Pill rendering | Pills above keyboard, scrollable when overflow | 4 |
| T-ENH-03 | Context weighting | Rank suggestions by visible pane context | 4 |

**Subtotal terminal enhancement:** 16 hours

### 2.4 Integration & Testing

| ID | Task | Description | Est. Hours |
|----|------|-------------|------------|
| INT-01 | Shell responsive wiring | Viewport detection → layout switching in Shell.tsx | 8 |
| INT-02 | Set file authoring | workdesk.set.md with all primitives declared | 4 |
| INT-03 | RTD bus integration | All new primitives publish RTDs correctly | 6 |
| INT-04 | Command vocabulary | Define PRISM-IR command mappings for command-interpreter | 8 |
| INT-05 | End-to-end mobile test | Manual test on real device (iOS/Android) | 8 |
| INT-06 | Voice → command flow | voice-input → command-interpreter → PRISM-IR → hivenode | 6 |

**Subtotal integration:** 40 hours

---

## 3. Dependency Graph

```
                    ┌─────────────────────────────────────────┐
                    │         command-interpreter             │
                    │            (P-NEW-08)                   │
                    │         [MUST BUILD FIRST]              │
                    └─────────────────┬───────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
   ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
   │  voice-input │           │ quick-actions│           │ conversation │
   │  (P-NEW-04)  │           │  (P-NEW-03)  │           │    -pane     │
   └──────┬───────┘           └──────┬───────┘           │  (P-NEW-06)  │
          │                          │                   └──────┬───────┘
          │                          │                          │
          └──────────────────────────┼──────────────────────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │    mobile-nav       │
                          │     (P-NEW-01)      │
                          └─────────┬───────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ notification │         │  queue-pane  │         │  diff-viewer │
   │    -pane     │         │  (P-NEW-07)  │         │  (P-NEW-05)  │
   │  (P-NEW-02)  │         └──────────────┘         └──────────────┘
   └──────────────┘


   PARALLEL TRACK (no deps on new primitives):
   ┌─────────────────────────────────────────────────────────────────┐
   │  Mobile CSS for existing primitives (P-MOB-01 through P-MOB-11) │
   │  Terminal enhancements (T-ENH-01 through T-ENH-03)              │
   └─────────────────────────────────────────────────────────────────┘
```

### Dependency Rules

1. **command-interpreter** has no dependencies — build first
2. **voice-input**, **quick-actions**, **conversation-pane** depend on command-interpreter
3. **mobile-nav** depends on voice-input, quick-actions (FAB integrates with nav)
4. **notification-pane**, **queue-pane**, **diff-viewer** depend on mobile-nav (navigation targets)
5. **Mobile CSS track** runs in parallel — no dependencies on new primitives
6. **Terminal enhancements** run in parallel — no dependencies on new primitives
7. **Integration tasks** run after their dependencies complete

---

## 4. Task Breakdown

### Phase 1: Foundation (command-interpreter)

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-001 | command-interpreter: core parser + fuzzy matching | — | 8 | P-MOB-* |
| TASK-MW-002 | command-interpreter: PRISM-IR command emission | MW-001 | 6 | P-MOB-* |
| TASK-MW-003 | command-interpreter: confirmation logic + ambiguity picker | MW-002 | 6 | P-MOB-* |

### Phase 2: Input Surfaces (parallel after Phase 1)

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-004 | voice-input: Web Speech API wrapper | MW-003 | 5 | MW-005, MW-006 |
| TASK-MW-005 | voice-input: command-interpreter integration | MW-004 | 5 | MW-006 |
| TASK-MW-006 | quick-actions: FAB component + move/hide/restore | MW-003 | 6 | MW-004, MW-005 |
| TASK-MW-007 | quick-actions: mic + keyboard toggle buttons | MW-006 | 6 | MW-008 |
| TASK-MW-008 | conversation-pane: multi-input rendering (pills, hero, text) | MW-003 | 10 | MW-009 |
| TASK-MW-009 | conversation-pane: multi-LLM routing via Efemera | MW-008 | 8 | MW-010 |
| TASK-MW-010 | conversation-pane: output surfaces (text, voice, pills) | MW-009 | 6 | — |

### Phase 3: Navigation

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-011 | mobile-nav: nested hub structure | MW-005, MW-007 | 8 | — |
| TASK-MW-012 | mobile-nav: back gesture + drill-down | MW-011 | 4 | MW-013 |
| TASK-MW-013 | mobile-nav: FAB integration | MW-012 | 4 | MW-012 |

### Phase 4: Destination Panes (parallel after Phase 3)

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-014 | notification-pane: data model + home screen | MW-013 | 10 | MW-017, MW-020 |
| TASK-MW-015 | notification-pane: badge counts + swipe-to-dismiss | MW-014 | 6 | MW-018, MW-021 |
| TASK-MW-016 | notification-pane: tap-to-navigate | MW-015 | 4 | MW-019, MW-022 |
| TASK-MW-017 | queue-pane: hivenode data fetch | MW-013 | 8 | MW-014, MW-020 |
| TASK-MW-018 | queue-pane: state display (queued/running/blocked/done) | MW-017 | 4 | MW-015, MW-021 |
| TASK-MW-019 | queue-pane: tap actions (view, reorder, cancel, approve) | MW-018 | 4 | MW-016, MW-022 |
| TASK-MW-020 | diff-viewer: diff parsing + mobile layout | MW-013 | 10 | MW-014, MW-017 |
| TASK-MW-021 | diff-viewer: inline expand/collapse | MW-020 | 4 | MW-015, MW-018 |
| TASK-MW-022 | diff-viewer: swipe actions (approve/reject) | MW-021 | 4 | MW-016, MW-019 |

### Phase 5: Mobile CSS (parallel track — can start immediately)

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-023 | text-pane mobile CSS | — | 8 | MW-001 through MW-028 |
| TASK-MW-024 | terminal mobile CSS + pill rendering | — | 12 | MW-001 through MW-028 |
| TASK-MW-025 | tree-browser mobile CSS | — | 8 | MW-001 through MW-028 |
| TASK-MW-026 | efemera-connector mobile CSS | — | 6 | MW-001 through MW-028 |
| TASK-MW-027 | settings mobile CSS | — | 4 | MW-001 through MW-028 |
| TASK-MW-028 | dashboard mobile CSS | — | 6 | MW-001 through MW-028 |
| TASK-MW-029 | progress-pane polish | — | 4 | MW-001 through MW-028 |
| TASK-MW-030 | top-bar mobile CSS | — | 4 | MW-001 through MW-028 |
| TASK-MW-031 | menu-bar → mobile drawer | — | 6 | MW-001 through MW-028 |
| TASK-MW-032 | status-bar mobile CSS | — | 3 | MW-001 through MW-028 |
| TASK-MW-033 | command-palette mobile overlay | — | 6 | MW-001 through MW-028 |

### Phase 6: Terminal Enhancements (parallel track)

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-034 | TF-IDF suggestion index | — | 8 | MW-001 through MW-033 |
| TASK-MW-035 | Pill UI + scrollable list | MW-034 | 4 | MW-001 through MW-033 |
| TASK-MW-036 | Context weighting logic | MW-035 | 4 | MW-001 through MW-033 |

### Phase 7: Integration

| Task ID | Description | Deps | Est. Hours | Parallelizable With |
|---------|-------------|------|------------|---------------------|
| TASK-MW-037 | Shell.tsx responsive wiring | MW-013, MW-033 | 8 | — |
| TASK-MW-038 | workdesk.set.md authoring | MW-037 | 4 | MW-039 |
| TASK-MW-039 | RTD bus integration for new primitives | MW-022 | 6 | MW-038 |
| TASK-MW-040 | PRISM-IR command vocabulary definition | MW-003 | 8 | MW-037 |
| TASK-MW-041 | Voice → command → PRISM-IR flow test | MW-040 | 6 | — |
| TASK-MW-042 | End-to-end mobile device test | MW-041, MW-038, MW-039 | 8 | — |

---

## 5. Concurrency Map

### Maximum Parallelism Points

**At project start (t=0):**
- Phase 1 (MW-001) + Phase 5 (MW-023 through MW-033) + Phase 6 (MW-034)
- Up to **12 concurrent tasks** if all mobile CSS and terminal work starts immediately

**After Phase 1 completes:**
- Phase 2 tasks (MW-004 through MW-010) — up to 3 parallel streams
- Phase 5/6 continue in parallel

**After Phase 3 completes:**
- Phase 4 tasks (MW-014 through MW-022) — up to 3 parallel streams (notification, queue, diff)

### Critical Path

```
MW-001 → MW-002 → MW-003 → MW-004 → MW-005 → MW-011 → MW-012 → MW-013 → MW-014 → MW-015 → MW-016 → MW-037 → MW-038 → MW-042
```

**Critical path duration:** ~95 hours (with zero parallelism)  
**With max parallelism:** ~50-60 hours wall time (estimate)

---

## 6. Estimates Summary

| Category | Hours |
|----------|-------|
| New primitives | 136 |
| Mobile CSS | 67 |
| Terminal enhancements | 16 |
| Integration | 40 |
| **Total** | **259** |

At 8h/day sustained:
- **Sequential:** ~32 days
- **2 concurrent bees:** ~18-20 days
- **3 concurrent bees:** ~12-15 days

---

## 7. Scheduler Stub (OR-Tools)

The following Python script uses Google OR-Tools to compute an optimal dispatch schedule given constraints.

### File: `scheduler_mobile_workdesk.py`

```python
#!/usr/bin/env python3
"""
Mobile Workdesk Build Scheduler

Uses Google OR-Tools CP-SAT solver to minimize makespan
under min/max concurrent bee constraints.

Usage:
    python scheduler_mobile_workdesk.py --min-bees 1 --max-bees 3

Output:
    Dispatch schedule showing which tasks to start at each time slot,
    respecting dependencies and concurrency limits.
"""

from ortools.sat.python import cp_model
from dataclasses import dataclass
from typing import Optional
import argparse
import json


@dataclass
class Task:
    id: str
    description: str
    duration_hours: int
    dependencies: list[str]
    parallelizable_with: list[str]  # informational


# Task registry from SPEC-MOBILE-WORKDESK-001
TASKS = [
    # Phase 1: Foundation
    Task("MW-001", "command-interpreter: core parser + fuzzy matching", 8, []),
    Task("MW-002", "command-interpreter: PRISM-IR emission", 6, ["MW-001"]),
    Task("MW-003", "command-interpreter: confirmation + ambiguity", 6, ["MW-002"]),
    
    # Phase 2: Input Surfaces
    Task("MW-004", "voice-input: Web Speech API wrapper", 5, ["MW-003"]),
    Task("MW-005", "voice-input: command-interpreter integration", 5, ["MW-004"]),
    Task("MW-006", "quick-actions: FAB component", 6, ["MW-003"]),
    Task("MW-007", "quick-actions: mic + keyboard buttons", 6, ["MW-006"]),
    Task("MW-008", "conversation-pane: multi-input rendering", 10, ["MW-003"]),
    Task("MW-009", "conversation-pane: multi-LLM routing", 8, ["MW-008"]),
    Task("MW-010", "conversation-pane: output surfaces", 6, ["MW-009"]),
    
    # Phase 3: Navigation
    Task("MW-011", "mobile-nav: nested hub structure", 8, ["MW-005", "MW-007"]),
    Task("MW-012", "mobile-nav: back gesture + drill-down", 4, ["MW-011"]),
    Task("MW-013", "mobile-nav: FAB integration", 4, ["MW-012"]),
    
    # Phase 4: Destination Panes
    Task("MW-014", "notification-pane: data model + home", 10, ["MW-013"]),
    Task("MW-015", "notification-pane: badges + swipe", 6, ["MW-014"]),
    Task("MW-016", "notification-pane: tap-to-navigate", 4, ["MW-015"]),
    Task("MW-017", "queue-pane: hivenode fetch", 8, ["MW-013"]),
    Task("MW-018", "queue-pane: state display", 4, ["MW-017"]),
    Task("MW-019", "queue-pane: tap actions", 4, ["MW-018"]),
    Task("MW-020", "diff-viewer: parsing + layout", 10, ["MW-013"]),
    Task("MW-021", "diff-viewer: expand/collapse", 4, ["MW-020"]),
    Task("MW-022", "diff-viewer: swipe actions", 4, ["MW-021"]),
    
    # Phase 5: Mobile CSS (no deps on new primitives)
    Task("MW-023", "text-pane mobile CSS", 8, []),
    Task("MW-024", "terminal mobile CSS + pills", 12, []),
    Task("MW-025", "tree-browser mobile CSS", 8, []),
    Task("MW-026", "efemera-connector mobile CSS", 6, []),
    Task("MW-027", "settings mobile CSS", 4, []),
    Task("MW-028", "dashboard mobile CSS", 6, []),
    Task("MW-029", "progress-pane polish", 4, []),
    Task("MW-030", "top-bar mobile CSS", 4, []),
    Task("MW-031", "menu-bar → drawer", 6, []),
    Task("MW-032", "status-bar mobile CSS", 3, []),
    Task("MW-033", "command-palette overlay", 6, []),
    
    # Phase 6: Terminal Enhancements
    Task("MW-034", "TF-IDF suggestion index", 8, []),
    Task("MW-035", "Pill UI + scrollable", 4, ["MW-034"]),
    Task("MW-036", "Context weighting", 4, ["MW-035"]),
    
    # Phase 7: Integration
    Task("MW-037", "Shell.tsx responsive wiring", 8, ["MW-013", "MW-033"]),
    Task("MW-038", "workdesk.set.md authoring", 4, ["MW-037"]),
    Task("MW-039", "RTD bus integration", 6, ["MW-022"]),
    Task("MW-040", "PRISM-IR command vocabulary", 8, ["MW-003"]),
    Task("MW-041", "Voice → command flow test", 6, ["MW-040"]),
    Task("MW-042", "End-to-end mobile test", 8, ["MW-041", "MW-038", "MW-039"]),
]


def build_task_index(tasks: list[Task]) -> dict[str, int]:
    """Map task ID to list index."""
    return {t.id: i for i, t in enumerate(tasks)}


def solve_schedule(tasks: list[Task], min_bees: int, max_bees: int, time_unit_hours: int = 1):
    """
    Solve for optimal schedule using CP-SAT.
    
    Args:
        tasks: List of Task objects
        min_bees: Minimum concurrent tasks (keep bees busy)
        max_bees: Maximum concurrent tasks (resource limit)
        time_unit_hours: Granularity of time slots (default 1 hour)
    
    Returns:
        dict with schedule, makespan, and utilization stats
    """
    model = cp_model.CpModel()
    task_idx = build_task_index(tasks)
    num_tasks = len(tasks)
    
    # Upper bound on makespan: sum of all durations (fully sequential)
    horizon = sum(t.duration_hours for t in tasks)
    
    # Decision variables: start time for each task
    starts = []
    ends = []
    intervals = []
    
    for t in tasks:
        start = model.NewIntVar(0, horizon, f"start_{t.id}")
        end = model.NewIntVar(0, horizon, f"end_{t.id}")
        interval = model.NewIntervalVar(start, t.duration_hours, end, f"interval_{t.id}")
        starts.append(start)
        ends.append(end)
        intervals.append(interval)
    
    # Dependency constraints: task can't start until all deps finish
    for i, t in enumerate(tasks):
        for dep_id in t.dependencies:
            if dep_id in task_idx:
                dep_i = task_idx[dep_id]
                model.Add(starts[i] >= ends[dep_i])
    
    # Concurrency constraint: at most max_bees tasks running at any time
    # Using cumulative constraint with unit demand
    demands = [1] * num_tasks
    model.AddCumulative(intervals, demands, max_bees)
    
    # Makespan: the latest end time
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, ends)
    
    # Objective: minimize makespan
    model.Minimize(makespan)
    
    # Optional: soft constraint to keep at least min_bees busy
    # (This is tricky with CP-SAT; we'll report utilization instead)
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule = []
        for i, t in enumerate(tasks):
            schedule.append({
                "task_id": t.id,
                "description": t.description,
                "start_hour": solver.Value(starts[i]),
                "end_hour": solver.Value(ends[i]),
                "duration_hours": t.duration_hours,
            })
        
        # Sort by start time
        schedule.sort(key=lambda x: (x["start_hour"], x["task_id"]))
        
        # Compute utilization
        total_work = sum(t.duration_hours for t in tasks)
        makespan_val = solver.Value(makespan)
        max_possible_work = makespan_val * max_bees
        utilization = total_work / max_possible_work if max_possible_work > 0 else 0
        
        return {
            "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
            "makespan_hours": makespan_val,
            "total_work_hours": total_work,
            "max_concurrent_bees": max_bees,
            "utilization": round(utilization, 3),
            "schedule": schedule,
        }
    else:
        return {
            "status": "INFEASIBLE" if status == cp_model.INFEASIBLE else "UNKNOWN",
            "schedule": [],
        }


def print_gantt(result: dict):
    """Print ASCII Gantt chart."""
    if result["status"] not in ("OPTIMAL", "FEASIBLE"):
        print(f"No solution found: {result['status']}")
        return
    
    print(f"\n{'='*80}")
    print(f"MOBILE WORKDESK BUILD SCHEDULE")
    print(f"{'='*80}")
    print(f"Makespan: {result['makespan_hours']} hours")
    print(f"Total work: {result['total_work_hours']} hours")
    print(f"Max concurrent: {result['max_concurrent_bees']} bees")
    print(f"Utilization: {result['utilization']*100:.1f}%")
    print(f"{'='*80}\n")
    
    # Group by start hour for dispatch view
    by_start = {}
    for item in result["schedule"]:
        start = item["start_hour"]
        if start not in by_start:
            by_start[start] = []
        by_start[start].append(item)
    
    print("DISPATCH ORDER (grouped by start time):\n")
    for start_hour in sorted(by_start.keys()):
        tasks_at_start = by_start[start_hour]
        print(f"Hour {start_hour:3d}: ", end="")
        task_strs = [f"{t['task_id']} ({t['duration_hours']}h)" for t in tasks_at_start]
        print(", ".join(task_strs))
    
    print(f"\n{'='*80}")
    print("TASK DETAIL:\n")
    
    for item in result["schedule"]:
        bar_width = item["duration_hours"]
        bar_start = item["start_hour"]
        print(f"{item['task_id']:8s} | {'.'*bar_start}{'█'*bar_width} | {item['description'][:50]}")


def main():
    parser = argparse.ArgumentParser(description="Mobile Workdesk Build Scheduler")
    parser.add_argument("--min-bees", type=int, default=1, help="Minimum concurrent bees")
    parser.add_argument("--max-bees", type=int, default=3, help="Maximum concurrent bees")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Gantt")
    args = parser.parse_args()
    
    result = solve_schedule(TASKS, args.min_bees, args.max_bees)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_gantt(result)


if __name__ == "__main__":
    main()
```

### Usage

```bash
# Install OR-Tools if not present
pip install ortools --break-system-packages

# Run with defaults (1-3 concurrent bees)
python scheduler_mobile_workdesk.py

# Run with constraints
python scheduler_mobile_workdesk.py --min-bees 2 --max-bees 4

# Output as JSON for programmatic consumption
python scheduler_mobile_workdesk.py --max-bees 3 --json > schedule.json
```

---

## 8. Command Vocabulary (command-interpreter)

### Voice/Text Commands → PRISM-IR

| Spoken / Typed | Matches | PRISM-IR Command |
|----------------|---------|------------------|
| "cancel [task]" | Fuzzy match task name in queue | `task.cancel(task_id)` |
| "pause [task]" | Fuzzy match running task | `task.pause(task_id)` |
| "resume [task]" | Fuzzy match paused task | `task.resume(task_id)` |
| "prioritize [task]" | Fuzzy match queued task | `task.set_priority(task_id, "high")` |
| "deprioritize [task]" | Fuzzy match queued task | `task.set_priority(task_id, "low")` |
| "approve [task]" | Fuzzy match blocked task | `task.approve(task_id)` |
| "reject [task]" | Fuzzy match blocked task | `task.reject(task_id)` |
| "assign [task] to [bee]" | Fuzzy match both | `task.assign(task_id, bee_id)` |
| "show [task]" | Fuzzy match any task | Navigate to task detail |
| "what's running" | — | Navigate to queue-pane, filter=running |
| "what's blocked" | — | Navigate to queue-pane, filter=blocked |
| "what's queued" | — | Navigate to queue-pane, filter=queued |
| "go home" | — | Navigate to notification-pane |
| "open [pane]" | Fuzzy match pane name | Navigate to pane |
| "change [field] to [value]" | Context-aware field match | Field-specific PRISM-IR |

### Confirmation Rules

| Action Type | Confirmation Required |
|-------------|----------------------|
| Destructive (cancel, reject) | Always |
| State change (pause, resume, prioritize) | Only if ambiguous |
| Navigation | Never |
| Field change | If value seems unusual |

### Ambiguity Handling

If fuzzy match returns >1 candidate with similar scores:
1. Emit picker request to UI
2. User taps choice
3. Continue with selected item

---

## 9. Task Structure: Spec → Test → Build → Verify

Every primitive follows this sequence:

```
SPEC task → TEST task → BUILD task(s) → VERIFY task
     ↓           ↓            ↓              ↓
  .spec.md    .test.ts    implementation   acceptance
```

### Task Type Definitions

| Type | Deliverable | Acceptance |
|------|-------------|------------|
| SPEC | `SPEC-[PRIMITIVE]-001.md` | Reviewed, no open questions |
| TEST | Test file(s) with failing tests | Tests run, all fail (TDD red) |
| BUILD | Implementation code | Tests pass (TDD green) |
| VERIFY | Response file with acceptance checklist | All criteria met |

### TDD Enforcement

**Tests are written BEFORE implementation.** The TEST task produces:
- Unit tests for all public interfaces
- Integration tests for bus/RTD interactions
- Edge case coverage (empty state, error states, offline)

Tests MUST fail when first written (nothing to test yet). BUILD task makes them pass.

---

## 10. Revised Task Breakdown (with Spec + Test phases)

### Phase 0: Spec Writing (can parallelize heavily)

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-S01 | SPEC: command-interpreter | — | 3 | SPEC |
| TASK-MW-S02 | SPEC: voice-input | — | 2 | SPEC |
| TASK-MW-S03 | SPEC: quick-actions (FAB) | — | 2 | SPEC |
| TASK-MW-S04 | SPEC: conversation-pane | — | 3 | SPEC |
| TASK-MW-S05 | SPEC: mobile-nav | — | 3 | SPEC |
| TASK-MW-S06 | SPEC: notification-pane | — | 2 | SPEC |
| TASK-MW-S07 | SPEC: queue-pane | — | 2 | SPEC |
| TASK-MW-S08 | SPEC: diff-viewer | — | 2 | SPEC |

**Subtotal specs:** 19 hours (all parallelizable at t=0)

### Phase 0.5: Test Writing (after each spec)

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-T01 | TEST: command-interpreter | S01 | 4 | TEST |
| TASK-MW-T02 | TEST: voice-input | S02 | 2 | TEST |
| TASK-MW-T03 | TEST: quick-actions | S03 | 2 | TEST |
| TASK-MW-T04 | TEST: conversation-pane | S04 | 4 | TEST |
| TASK-MW-T05 | TEST: mobile-nav | S05 | 3 | TEST |
| TASK-MW-T06 | TEST: notification-pane | S06 | 3 | TEST |
| TASK-MW-T07 | TEST: queue-pane | S07 | 3 | TEST |
| TASK-MW-T08 | TEST: diff-viewer | S08 | 3 | TEST |

**Subtotal tests:** 24 hours

### Phase 1: Foundation (command-interpreter) — BUILD

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-001 | BUILD: command-interpreter core parser + fuzzy matching | T01 | 8 | BUILD |
| TASK-MW-002 | BUILD: command-interpreter PRISM-IR emission | MW-001 | 6 | BUILD |
| TASK-MW-003 | BUILD: command-interpreter confirmation + ambiguity | MW-002 | 6 | BUILD |
| TASK-MW-V01 | VERIFY: command-interpreter | MW-003 | 2 | VERIFY |

### Phase 2: Input Surfaces — BUILD

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-004 | BUILD: voice-input Web Speech API wrapper | T02, MW-V01 | 5 | BUILD |
| TASK-MW-005 | BUILD: voice-input command-interpreter integration | MW-004 | 5 | BUILD |
| TASK-MW-V02 | VERIFY: voice-input | MW-005 | 2 | VERIFY |
| TASK-MW-006 | BUILD: quick-actions FAB component | T03, MW-V01 | 6 | BUILD |
| TASK-MW-007 | BUILD: quick-actions mic + keyboard buttons | MW-006 | 6 | BUILD |
| TASK-MW-V03 | VERIFY: quick-actions | MW-007 | 2 | VERIFY |
| TASK-MW-008 | BUILD: conversation-pane multi-input rendering | T04, MW-V01 | 10 | BUILD |
| TASK-MW-009 | BUILD: conversation-pane multi-LLM routing | MW-008 | 8 | BUILD |
| TASK-MW-010 | BUILD: conversation-pane output surfaces | MW-009 | 6 | BUILD |
| TASK-MW-V04 | VERIFY: conversation-pane | MW-010 | 2 | VERIFY |

### Phase 3: Navigation — BUILD

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-011 | BUILD: mobile-nav nested hub structure | T05, MW-V02, MW-V03 | 8 | BUILD |
| TASK-MW-012 | BUILD: mobile-nav back gesture + drill-down | MW-011 | 4 | BUILD |
| TASK-MW-013 | BUILD: mobile-nav FAB integration | MW-012 | 4 | BUILD |
| TASK-MW-V05 | VERIFY: mobile-nav | MW-013 | 2 | VERIFY |

### Phase 4: Destination Panes — BUILD

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-014 | BUILD: notification-pane data model + home | T06, MW-V05 | 10 | BUILD |
| TASK-MW-015 | BUILD: notification-pane badges + swipe | MW-014 | 6 | BUILD |
| TASK-MW-016 | BUILD: notification-pane tap-to-navigate | MW-015 | 4 | BUILD |
| TASK-MW-V06 | VERIFY: notification-pane | MW-016 | 2 | VERIFY |
| TASK-MW-017 | BUILD: queue-pane hivenode fetch | T07, MW-V05 | 8 | BUILD |
| TASK-MW-018 | BUILD: queue-pane state display | MW-017 | 4 | BUILD |
| TASK-MW-019 | BUILD: queue-pane tap actions | MW-018 | 4 | BUILD |
| TASK-MW-V07 | VERIFY: queue-pane | MW-019 | 2 | VERIFY |
| TASK-MW-020 | BUILD: diff-viewer parsing + layout | T08, MW-V05 | 10 | BUILD |
| TASK-MW-021 | BUILD: diff-viewer expand/collapse | MW-020 | 4 | BUILD |
| TASK-MW-022 | BUILD: diff-viewer swipe actions | MW-021 | 4 | BUILD |
| TASK-MW-V08 | VERIFY: diff-viewer | MW-022 | 2 | VERIFY |

### Phase 5: Mobile CSS (parallel track)

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-023 | BUILD: text-pane mobile CSS | — | 8 | BUILD |
| TASK-MW-024 | BUILD: terminal mobile CSS + pills | — | 12 | BUILD |
| TASK-MW-025 | BUILD: tree-browser mobile CSS | — | 8 | BUILD |
| TASK-MW-026 | BUILD: efemera-connector mobile CSS | — | 6 | BUILD |
| TASK-MW-027 | BUILD: settings mobile CSS | — | 4 | BUILD |
| TASK-MW-028 | BUILD: dashboard mobile CSS | — | 6 | BUILD |
| TASK-MW-029 | BUILD: progress-pane polish | — | 4 | BUILD |
| TASK-MW-030 | BUILD: top-bar mobile CSS | — | 4 | BUILD |
| TASK-MW-031 | BUILD: menu-bar → drawer | — | 6 | BUILD |
| TASK-MW-032 | BUILD: status-bar mobile CSS | — | 3 | BUILD |
| TASK-MW-033 | BUILD: command-palette overlay | — | 6 | BUILD |

### Phase 6: Terminal Enhancements (parallel track)

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-034 | BUILD: TF-IDF suggestion index | — | 8 | BUILD |
| TASK-MW-035 | BUILD: Pill UI + scrollable | MW-034 | 4 | BUILD |
| TASK-MW-036 | BUILD: Context weighting | MW-035 | 4 | BUILD |

### Phase 7: Integration

| Task ID | Description | Deps | Est. Hours | Type |
|---------|-------------|------|------------|------|
| TASK-MW-037 | BUILD: Shell.tsx responsive wiring | MW-V05, MW-033 | 8 | BUILD |
| TASK-MW-038 | BUILD: workdesk.set.md authoring | MW-037 | 4 | BUILD |
| TASK-MW-039 | BUILD: RTD bus integration | MW-V08 | 6 | BUILD |
| TASK-MW-040 | BUILD: PRISM-IR command vocabulary | MW-V01 | 8 | BUILD |
| TASK-MW-041 | TEST: Voice → command flow E2E | MW-040 | 6 | TEST |
| TASK-MW-042 | VERIFY: E2E mobile test | MW-041, MW-038, MW-039 | 8 | VERIFY |

---

## 11. Revised Estimates Summary

| Category | Hours |
|----------|-------|
| Spec writing | 19 |
| Test writing | 24 |
| New primitives (build) | 136 |
| New primitives (verify) | 16 |
| Mobile CSS | 67 |
| Terminal enhancements | 16 |
| Integration | 40 |
| **Total** | **318** |

---

## 12. Dynamic Rescheduling

### Concept

The scheduler doesn't run once — it runs **continuously** as tasks complete. When a task finishes (or fails, or stalls), the scheduler:

1. Updates task status in the registry
2. Re-runs OR-Tools with remaining tasks
3. Emits new dispatch recommendations
4. Respects min/max bee constraints

### Implementation

#### File: `scheduler_state.json`

Persistent state file tracking:

```json
{
  "project": "mobile-workdesk",
  "started_at": "2026-04-05T10:00:00Z",
  "constraints": {
    "min_bees": 2,
    "max_bees": 4
  },
  "tasks": {
    "MW-S01": {"status": "DONE", "actual_hours": 2.5, "completed_at": "..."},
    "MW-S02": {"status": "DONE", "actual_hours": 2.0, "completed_at": "..."},
    "MW-T01": {"status": "IN_PROGRESS", "started_at": "...", "bee": "BEE-001"},
    "MW-001": {"status": "BLOCKED", "blocked_by": ["MW-T01"]}
  },
  "telemetry": {
    "total_actual_hours": 4.5,
    "total_estimated_hours": 5.0,
    "velocity": 1.11
  }
}
```

#### Velocity Tracking

As tasks complete, we compute rolling velocity:

```
velocity = actual_hours / estimated_hours
```

If velocity < 1.0, we're running fast. If velocity > 1.0, we're behind.

The scheduler adjusts remaining estimates:

```
adjusted_estimate = original_estimate * velocity
```

This gives realistic projections as the build progresses.

#### Rescheduling Triggers

| Event | Action |
|-------|--------|
| Task completes | Mark DONE, unlock dependents, reschedule |
| Task fails | Mark FAILED, assess impact, reschedule |
| Task stalls (no progress 2h) | Alert, optionally reassign, reschedule |
| Bee goes offline | Redistribute work, reschedule |
| Constraint change | Reschedule with new min/max |

#### Scheduler Daemon (future)

For now: manual Python invocation after each task batch.

Soon: `hivenode/scheduler/daemon.py` watches task completions, auto-reschedules.

---

## 13. Telemetry Requirements

### CRITICAL: Every LLM Call Must Capture

Every prompt/response pair — whether from bee dispatch, conversation-pane, or any other LLM interaction — **MUST** emit telemetry to the Event Ledger.

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Task being worked (e.g., "MW-001") |
| `bee_id` | string | Bee/agent making the call |
| `model` | string | Exact model string (e.g., "claude-sonnet-4-20250514") |
| `provider` | string | "anthropic" / "google" / "openai" |
| `tokens_in` | int | Input tokens (prompt) |
| `tokens_out` | int | Output tokens (completion) |
| `cache_read` | int | Tokens read from cache |
| `cache_write` | int | Tokens written to cache |
| `latency_ms` | int | Wall time for request |
| `cost_usd` | float | Computed cost from rate table |
| `carbon_g` | float | Computed carbon from rate table |
| `timestamp` | ISO8601 | When the call completed |
| `success` | bool | Did the call succeed? |
| `error` | string? | Error message if failed |

#### Telemetry Emission Points

1. **Bee dispatch** — Every task file sent to a bee
2. **Bee response** — Every response file received
3. **Conversation-pane** — Every user ↔ LLM exchange
4. **Voice transcription** — If using cloud STT
5. **Command interpretation** — If LLM-assisted (future)

#### Event Ledger Schema Extension

```sql
CREATE TABLE llm_telemetry (
  id SERIAL PRIMARY KEY,
  task_id TEXT,
  bee_id TEXT NOT NULL,
  model TEXT NOT NULL,
  provider TEXT NOT NULL,
  tokens_in INT NOT NULL,
  tokens_out INT NOT NULL,
  cache_read INT DEFAULT 0,
  cache_write INT DEFAULT 0,
  latency_ms INT NOT NULL,
  cost_usd DECIMAL(10,6) NOT NULL,
  carbon_g DECIMAL(10,4) NOT NULL,
  success BOOLEAN NOT NULL,
  error TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_llm_telemetry_task ON llm_telemetry(task_id);
CREATE INDEX idx_llm_telemetry_model ON llm_telemetry(model);
CREATE INDEX idx_llm_telemetry_created ON llm_telemetry(created_at);
```

#### Rate Table Location

`hivenode/rate_loader/model_rates.yml` — must include all token types:

```yaml
models:
  claude-opus-4-20250514:
    input_per_1k: 0.015
    output_per_1k: 0.075
    cache_read_per_1k: 0.00375
    cache_write_per_1k: 0.01875
    carbon_per_1k_tokens: 0.0023
    
  claude-sonnet-4-20250514:
    input_per_1k: 0.003
    output_per_1k: 0.015
    cache_read_per_1k: 0.0003
    cache_write_per_1k: 0.00375
    carbon_per_1k_tokens: 0.0015
    
  claude-haiku-3-5-20241022:
    input_per_1k: 0.0008
    output_per_1k: 0.004
    cache_read_per_1k: 0.00008
    cache_write_per_1k: 0.001
    carbon_per_1k_tokens: 0.0008
    
  gemini-2.0-flash:
    input_per_1k: 0.0001
    output_per_1k: 0.0004
    carbon_per_1k_tokens: 0.0005
    
  gpt-4o:
    input_per_1k: 0.005
    output_per_1k: 0.015
    carbon_per_1k_tokens: 0.0018
```

#### Telemetry Helper Function

```python
# hivenode/telemetry/llm_logger.py

from datetime import datetime
from .rate_loader import get_rates

def log_llm_call(
    task_id: str | None,
    bee_id: str,
    model: str,
    provider: str,
    tokens_in: int,
    tokens_out: int,
    cache_read: int,
    cache_write: int,
    latency_ms: int,
    success: bool,
    error: str | None = None,
) -> dict:
    """Log an LLM call with computed cost and carbon."""
    rates = get_rates(model)
    
    cost_usd = (
        (tokens_in / 1000) * rates["input_per_1k"] +
        (tokens_out / 1000) * rates["output_per_1k"] +
        (cache_read / 1000) * rates["cache_read_per_1k"] +
        (cache_write / 1000) * rates["cache_write_per_1k"]
    )
    
    carbon_g = (
        (tokens_in + tokens_out + cache_read + cache_write) / 1000
    ) * rates["carbon_per_1k_tokens"]
    
    record = {
        "task_id": task_id,
        "bee_id": bee_id,
        "model": model,
        "provider": provider,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cache_read": cache_read,
        "cache_write": cache_write,
        "latency_ms": latency_ms,
        "cost_usd": round(cost_usd, 6),
        "carbon_g": round(carbon_g, 4),
        "success": success,
        "error": error,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    
    emit_to_ledger("llm_telemetry", record)
    return record
```

#### Response File Telemetry Section

Every bee response file includes:

```markdown
## Telemetry

| Metric | Value |
|--------|-------|
| Model | claude-sonnet-4-20250514 |
| Provider | anthropic |
| Tokens In | 4,521 |
| Tokens Out | 1,847 |
| Cache Read | 2,100 |
| Cache Write | 0 |
| Latency | 3,421 ms |
| Cost (USD) | $0.041235 |
| Carbon (g CO2e) | 0.0127 |

## Clock / Coin / Carbon

| Currency | Value |
|----------|-------|
| CLOCK | 3,421 ms |
| COIN | $0.041235 |
| CARBON | 0.0127 g |
```

---

## 14. Set File Skeleton

### File: `workdesk.set.md`

```yaml
---
name: workdesk
version: 0.1.0
description: Mobile-first hive command center
viewport: responsive
---

# Headless primitives
- type: command-interpreter
  headless: true
  config:
    vocabulary: /config/command-vocabulary.yml
    prism_endpoint: ${HIVENODE_URL}/api/prism

# Visible primitives
- type: mobile-nav
  id: nav
  home: notification-pane
  
- type: notification-pane
  id: notifications
  
- type: queue-pane
  id: queue
  config:
    hivenode: ${HIVENODE_URL}
    
- type: diff-viewer
  id: diff
  
- type: conversation-pane
  id: conversation
  config:
    providers:
      - anthropic
      - google
      - openai
    efemera_channel: ${EFEMERA_CHANNEL}

- type: voice-input
  id: voice
  config:
    target: command-interpreter

- type: quick-actions
  id: fab
  config:
    buttons:
      - id: mic
        icon: microphone
        action: voice.toggle
      - id: keyboard
        icon: keyboard
        action: terminal.keyboard
        show_when: terminal.focused
      - id: kebab
        icon: more-vertical
        actions:
          - move
          - hide
    movable: true
    hideable: true

# Existing primitives (mobile CSS applied)
- type: terminal
  id: terminal
  config:
    suggestions:
      engine: tfidf
      sources:
        - command_history
        - file_paths
        - entity_names

- type: text-pane
  id: editor

- type: tree-browser
  id: files
  config:
    volume: home://

- type: efemera-connector
  id: efemera

- type: settings
  id: settings

- type: dashboard
  id: dashboard

- type: progress-pane
  id: progress

- type: top-bar
  id: topbar

- type: menu-bar
  id: menu

- type: status-bar
  id: status

- type: command-palette
  id: palette
```

---

## 15. Task Flow: Staging → Backlog → Queue

```
STAGING                      ← inbox, new tasks land here
    │
    │ scheduler evaluates, orders, moves to backlog
    ▼
BACKLOG                      ← ordered list, scheduler can reprioritize anytime
    │
    │ dispatcher moves when schedule says go
    ▼
QUEUE                        ← waiting for bee slot + deps
    │
    │ queue-runner assigns when bee available AND deps met
    ▼
RUNNING                      ← executing
    │
    │ completes, emits telemetry
    ▼
DONE
```

**Folder structure:**

```
.deia/hive/
├── staging/          # Unprocessed inbox — scheduler evaluates these
├── backlog/          # Ordered by scheduler, waiting for dispatch window
├── queue/            # Ready for execution, waiting for bee + deps
├── running/          # Currently executing (queue-runner tracks)
└── _done/            # Completed with response files
```

**Ownership:**

| Component | Reads | Writes | Does |
|-----------|-------|--------|------|
| Scheduler | staging/, _done/ (velocity) | backlog/ (ordering) | Evaluates staging, orders into backlog, reprioritizes |
| Dispatcher | backlog/, schedule | queue/ | Moves tasks when schedule time arrives |
| Queue-runner | queue/, _done/ (deps) | running/, _done/ | Assigns to bee when slot free + deps met |

**Key rule:** Queue-runner is the final gate. It won't execute a task until deps are in `_done/`, regardless of what scheduler/dispatcher say. This handles cases where dispatcher moves a task to queue before its dependencies complete.

**Existing queue-runner (7,500 lines) handles:** queue/ → running/ → _done/, deps checking, heartbeats, watchdog, retry, fix cycles. We're adding the upstream staging/ → backlog/ → queue/ pipeline.

---

## 16. Scheduler v2 (with Rescheduling + Telemetry)

### File: `scheduler_mobile_workdesk.py`

```python
#!/usr/bin/env python3
"""
Mobile Workdesk Build Scheduler v2

Features:
- OR-Tools CP-SAT constraint solver
- Dynamic rescheduling from state file
- Velocity tracking and estimate adjustment
- Telemetry aggregation

Usage:
    # Initial schedule
    python scheduler_mobile_workdesk.py --min-bees 2 --max-bees 4
    
    # Reschedule after task completion
    python scheduler_mobile_workdesk.py --state scheduler_state.json --reschedule
    
    # Mark task complete with actuals
    python scheduler_mobile_workdesk.py --complete MW-S01 --actual-hours 2.5
    
    # View current state
    python scheduler_mobile_workdesk.py --state scheduler_state.json --status
"""

from ortools.sat.python import cp_model
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import argparse
import json


@dataclass
class Task:
    id: str
    description: str
    duration_hours: int
    dependencies: list[str]
    task_type: str  # SPEC, TEST, BUILD, VERIFY
    status: str = "PENDING"
    actual_hours: Optional[float] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    assigned_bee: Optional[str] = None


# Full task registry
TASKS = [
    # Phase 0: Specs (all parallelizable)
    Task("MW-S01", "SPEC: command-interpreter", 3, [], "SPEC"),
    Task("MW-S02", "SPEC: voice-input", 2, [], "SPEC"),
    Task("MW-S03", "SPEC: quick-actions (FAB)", 2, [], "SPEC"),
    Task("MW-S04", "SPEC: conversation-pane", 3, [], "SPEC"),
    Task("MW-S05", "SPEC: mobile-nav", 3, [], "SPEC"),
    Task("MW-S06", "SPEC: notification-pane", 2, [], "SPEC"),
    Task("MW-S07", "SPEC: queue-pane", 2, [], "SPEC"),
    Task("MW-S08", "SPEC: diff-viewer", 2, [], "SPEC"),
    
    # Phase 0.5: Tests (after specs)
    Task("MW-T01", "TEST: command-interpreter", 4, ["MW-S01"], "TEST"),
    Task("MW-T02", "TEST: voice-input", 2, ["MW-S02"], "TEST"),
    Task("MW-T03", "TEST: quick-actions", 2, ["MW-S03"], "TEST"),
    Task("MW-T04", "TEST: conversation-pane", 4, ["MW-S04"], "TEST"),
    Task("MW-T05", "TEST: mobile-nav", 3, ["MW-S05"], "TEST"),
    Task("MW-T06", "TEST: notification-pane", 3, ["MW-S06"], "TEST"),
    Task("MW-T07", "TEST: queue-pane", 3, ["MW-S07"], "TEST"),
    Task("MW-T08", "TEST: diff-viewer", 3, ["MW-S08"], "TEST"),
    
    # Phase 1: command-interpreter BUILD
    Task("MW-001", "BUILD: command-interpreter core", 8, ["MW-T01"], "BUILD"),
    Task("MW-002", "BUILD: command-interpreter PRISM-IR", 6, ["MW-001"], "BUILD"),
    Task("MW-003", "BUILD: command-interpreter confirm", 6, ["MW-002"], "BUILD"),
    Task("MW-V01", "VERIFY: command-interpreter", 2, ["MW-003"], "VERIFY"),
    
    # Phase 2: Input surfaces BUILD
    Task("MW-004", "BUILD: voice-input wrapper", 5, ["MW-T02", "MW-V01"], "BUILD"),
    Task("MW-005", "BUILD: voice-input integration", 5, ["MW-004"], "BUILD"),
    Task("MW-V02", "VERIFY: voice-input", 2, ["MW-005"], "VERIFY"),
    Task("MW-006", "BUILD: quick-actions FAB", 6, ["MW-T03", "MW-V01"], "BUILD"),
    Task("MW-007", "BUILD: quick-actions buttons", 6, ["MW-006"], "BUILD"),
    Task("MW-V03", "VERIFY: quick-actions", 2, ["MW-007"], "VERIFY"),
    Task("MW-008", "BUILD: conversation multi-input", 10, ["MW-T04", "MW-V01"], "BUILD"),
    Task("MW-009", "BUILD: conversation LLM routing", 8, ["MW-008"], "BUILD"),
    Task("MW-010", "BUILD: conversation output", 6, ["MW-009"], "BUILD"),
    Task("MW-V04", "VERIFY: conversation-pane", 2, ["MW-010"], "VERIFY"),
    
    # Phase 3: Navigation BUILD
    Task("MW-011", "BUILD: mobile-nav hub", 8, ["MW-T05", "MW-V02", "MW-V03"], "BUILD"),
    Task("MW-012", "BUILD: mobile-nav gestures", 4, ["MW-011"], "BUILD"),
    Task("MW-013", "BUILD: mobile-nav FAB", 4, ["MW-012"], "BUILD"),
    Task("MW-V05", "VERIFY: mobile-nav", 2, ["MW-013"], "VERIFY"),
    
    # Phase 4: Destination panes BUILD
    Task("MW-014", "BUILD: notification data", 10, ["MW-T06", "MW-V05"], "BUILD"),
    Task("MW-015", "BUILD: notification badges", 6, ["MW-014"], "BUILD"),
    Task("MW-016", "BUILD: notification nav", 4, ["MW-015"], "BUILD"),
    Task("MW-V06", "VERIFY: notification-pane", 2, ["MW-016"], "VERIFY"),
    Task("MW-017", "BUILD: queue-pane fetch", 8, ["MW-T07", "MW-V05"], "BUILD"),
    Task("MW-018", "BUILD: queue-pane display", 4, ["MW-017"], "BUILD"),
    Task("MW-019", "BUILD: queue-pane actions", 4, ["MW-018"], "BUILD"),
    Task("MW-V07", "VERIFY: queue-pane", 2, ["MW-019"], "VERIFY"),
    Task("MW-020", "BUILD: diff-viewer parse", 10, ["MW-T08", "MW-V05"], "BUILD"),
    Task("MW-021", "BUILD: diff-viewer expand", 4, ["MW-020"], "BUILD"),
    Task("MW-022", "BUILD: diff-viewer swipe", 4, ["MW-021"], "BUILD"),
    Task("MW-V08", "VERIFY: diff-viewer", 2, ["MW-022"], "VERIFY"),
    
    # Phase 5: Mobile CSS (no deps — can start immediately)
    Task("MW-023", "BUILD: text-pane mobile", 8, [], "BUILD"),
    Task("MW-024", "BUILD: terminal mobile", 12, [], "BUILD"),
    Task("MW-025", "BUILD: tree-browser mobile", 8, [], "BUILD"),
    Task("MW-026", "BUILD: efemera mobile", 6, [], "BUILD"),
    Task("MW-027", "BUILD: settings mobile", 4, [], "BUILD"),
    Task("MW-028", "BUILD: dashboard mobile", 6, [], "BUILD"),
    Task("MW-029", "BUILD: progress-pane polish", 4, [], "BUILD"),
    Task("MW-030", "BUILD: top-bar mobile", 4, [], "BUILD"),
    Task("MW-031", "BUILD: menu-bar drawer", 6, [], "BUILD"),
    Task("MW-032", "BUILD: status-bar mobile", 3, [], "BUILD"),
    Task("MW-033", "BUILD: command-palette mobile", 6, [], "BUILD"),
    
    # Phase 6: Terminal enhancements
    Task("MW-034", "BUILD: TF-IDF index", 8, [], "BUILD"),
    Task("MW-035", "BUILD: Pill UI", 4, ["MW-034"], "BUILD"),
    Task("MW-036", "BUILD: Context weighting", 4, ["MW-035"], "BUILD"),
    
    # Phase 7: Integration
    Task("MW-037", "BUILD: Shell responsive", 8, ["MW-V05", "MW-033"], "BUILD"),
    Task("MW-038", "BUILD: workdesk.set.md", 4, ["MW-037"], "BUILD"),
    Task("MW-039", "BUILD: RTD integration", 6, ["MW-V08"], "BUILD"),
    Task("MW-040", "BUILD: PRISM-IR vocab", 8, ["MW-V01"], "BUILD"),
    Task("MW-041", "TEST: E2E voice flow", 6, ["MW-040"], "TEST"),
    Task("MW-042", "VERIFY: E2E mobile", 8, ["MW-041", "MW-038", "MW-039"], "VERIFY"),
]


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {
        "project": "mobile-workdesk",
        "started_at": datetime.utcnow().isoformat() + "Z",
        "constraints": {"min_bees": 2, "max_bees": 4},
        "tasks": {},
        "telemetry": {
            "total_actual_hours": 0,
            "total_estimated_hours": 0,
            "velocity": 1.0,
            "total_cost_usd": 0,
            "total_tokens_in": 0,
            "total_tokens_out": 0,
        },
    }


def save_state(state: dict, path: Path):
    path.write_text(json.dumps(state, indent=2))


def apply_state(tasks: list[Task], state: dict) -> list[Task]:
    for task in tasks:
        if task.id in state.get("tasks", {}):
            saved = state["tasks"][task.id]
            task.status = saved.get("status", "PENDING")
            task.actual_hours = saved.get("actual_hours")
            task.started_at = saved.get("started_at")
            task.completed_at = saved.get("completed_at")
            task.assigned_bee = saved.get("assigned_bee")
    return tasks


def compute_velocity(state: dict) -> float:
    actual = state["telemetry"]["total_actual_hours"]
    estimated = state["telemetry"]["total_estimated_hours"]
    if estimated == 0:
        return 1.0
    return actual / estimated


def get_remaining_tasks(tasks: list[Task]) -> list[Task]:
    return [t for t in tasks if t.status not in ("DONE", "FAILED")]


def solve_schedule(tasks: list[Task], min_bees: int, max_bees: int, velocity: float = 1.0) -> dict:
    model = cp_model.CpModel()
    task_idx = {t.id: i for i, t in enumerate(tasks)}
    
    adjusted_durations = [max(1, int(t.duration_hours * velocity)) for t in tasks]
    horizon = sum(adjusted_durations)
    
    starts, ends, intervals = [], [], []
    for i, t in enumerate(tasks):
        dur = adjusted_durations[i]
        start = model.NewIntVar(0, horizon, f"start_{t.id}")
        end = model.NewIntVar(0, horizon, f"end_{t.id}")
        interval = model.NewIntervalVar(start, dur, end, f"interval_{t.id}")
        starts.append(start)
        ends.append(end)
        intervals.append(interval)
    
    # Dependencies
    for i, t in enumerate(tasks):
        for dep_id in t.dependencies:
            if dep_id in task_idx:
                model.Add(starts[i] >= ends[task_idx[dep_id]])
    
    # Concurrency limit
    model.AddCumulative(intervals, [1]*len(tasks), max_bees)
    
    # Minimize makespan
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, ends)
    model.Minimize(makespan)
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        schedule = []
        for i, t in enumerate(tasks):
            schedule.append({
                "task_id": t.id,
                "description": t.description,
                "type": t.task_type,
                "status": t.status,
                "start_hour": solver.Value(starts[i]),
                "end_hour": solver.Value(ends[i]),
                "estimated_hours": t.duration_hours,
                "adjusted_hours": adjusted_durations[i],
            })
        schedule.sort(key=lambda x: (x["start_hour"], x["task_id"]))
        
        total_work = sum(adjusted_durations)
        makespan_val = solver.Value(makespan)
        utilization = total_work / (makespan_val * max_bees) if makespan_val > 0 else 0
        
        return {
            "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
            "makespan_hours": makespan_val,
            "total_work_hours": total_work,
            "velocity": velocity,
            "max_concurrent_bees": max_bees,
            "utilization": round(utilization, 3),
            "schedule": schedule,
        }
    return {"status": "INFEASIBLE", "schedule": []}


def mark_complete(state: dict, task_id: str, actual_hours: float, tasks: list[Task],
                  tokens_in: int = 0, tokens_out: int = 0, cost_usd: float = 0):
    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        raise ValueError(f"Unknown task: {task_id}")
    
    state["tasks"][task_id] = {
        "status": "DONE",
        "actual_hours": actual_hours,
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost_usd,
    }
    
    state["telemetry"]["total_actual_hours"] += actual_hours
    state["telemetry"]["total_estimated_hours"] += task.duration_hours
    state["telemetry"]["velocity"] = compute_velocity(state)
    state["telemetry"]["total_cost_usd"] += cost_usd
    state["telemetry"]["total_tokens_in"] += tokens_in
    state["telemetry"]["total_tokens_out"] += tokens_out
    
    return state


def print_schedule(result: dict, state: dict = None):
    if result["status"] not in ("OPTIMAL", "FEASIBLE"):
        print(f"No solution: {result['status']}")
        return
    
    print(f"\n{'='*80}")
    print(f"MOBILE WORKDESK BUILD SCHEDULE")
    print(f"{'='*80}")
    print(f"Makespan: {result['makespan_hours']} hours")
    print(f"Velocity: {result['velocity']:.2f}x")
    print(f"Max concurrent: {result['max_concurrent_bees']} bees")
    print(f"Utilization: {result['utilization']*100:.1f}%")
    
    if state:
        tel = state["telemetry"]
        print(f"\n--- Telemetry ---")
        print(f"Actual hours: {tel['total_actual_hours']:.1f}")
        print(f"Cost: ${tel['total_cost_usd']:.4f}")
        print(f"Tokens: {tel['total_tokens_in']:,} in / {tel['total_tokens_out']:,} out")
    
    print(f"{'='*80}\n")
    
    by_start = {}
    for item in result["schedule"]:
        by_start.setdefault(item["start_hour"], []).append(item)
    
    print("DISPATCH ORDER:\n")
    for hour in sorted(by_start.keys()):
        print(f"Hour {hour:3d}:")
        for item in by_start[hour]:
            icon = "✓" if item["status"] == "DONE" else "▶" if item["status"] == "IN_PROGRESS" else "○"
            print(f"  {icon} {item['task_id']:8s} [{item['type']:6s}] {item['adjusted_hours']:2d}h | {item['description'][:40]}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Mobile Workdesk Scheduler v2")
    parser.add_argument("--min-bees", type=int, default=2)
    parser.add_argument("--max-bees", type=int, default=4)
    parser.add_argument("--state", type=Path, default=Path("scheduler_state.json"))
    parser.add_argument("--reschedule", action="store_true")
    parser.add_argument("--status", action="store_true", help="Show current state")
    parser.add_argument("--complete", type=str, help="Task ID to mark complete")
    parser.add_argument("--actual-hours", type=float)
    parser.add_argument("--tokens-in", type=int, default=0)
    parser.add_argument("--tokens-out", type=int, default=0)
    parser.add_argument("--cost", type=float, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    tasks = [Task(**t.__dict__) for t in TASKS]
    state = load_state(args.state)
    
    if args.complete:
        if args.actual_hours is None:
            raise ValueError("--actual-hours required")
        state = mark_complete(state, args.complete, args.actual_hours, tasks,
                              args.tokens_in, args.tokens_out, args.cost)
        save_state(state, args.state)
        print(f"✓ {args.complete} complete ({args.actual_hours}h, ${args.cost:.4f})")
        print(f"  Velocity: {state['telemetry']['velocity']:.2f}x")
        return
    
    if args.status:
        tasks = apply_state(tasks, state)
        done = [t for t in tasks if t.status == "DONE"]
        remaining = [t for t in tasks if t.status not in ("DONE", "FAILED")]
        print(f"\n{'='*60}")
        print(f"PROJECT STATUS: mobile-workdesk")
        print(f"{'='*60}")
        print(f"Done: {len(done)} / {len(tasks)} tasks")
        print(f"Remaining: {len(remaining)} tasks")
        tel = state["telemetry"]
        print(f"Velocity: {tel['velocity']:.2f}x")
        print(f"Cost so far: ${tel['total_cost_usd']:.4f}")
        return
    
    tasks = apply_state(tasks, state)
    if args.reschedule:
        tasks = get_remaining_tasks(tasks)
        if not tasks:
            print("All tasks complete!")
            return
    
    velocity = state["telemetry"]["velocity"]
    result = solve_schedule(tasks, args.min_bees, args.max_bees, velocity)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_schedule(result, state if args.reschedule else None)


if __name__ == "__main__":
    main()
```

---

## 17. Acceptance Criteria

### Build-Level

- [ ] All 8 new primitives built and passing tests
- [ ] All 11 existing primitives have mobile CSS
- [ ] Terminal has TF-IDF suggestions working
- [ ] workdesk.set.md inflates correctly
- [ ] Voice → command-interpreter → PRISM-IR flow works E2E
- [ ] Real device test passes (iOS or Android)

### Telemetry

- [ ] Every LLM call emits to llm_telemetry table
- [ ] All token types captured (in, out, cache_read, cache_write)
- [ ] Model string is exact (not aliased)
- [ ] Cost computed from rate table, not estimated
- [ ] Response files include telemetry section

### Scheduler

- [ ] OR-Tools solves initial schedule
- [ ] --complete updates state and velocity
- [ ] --reschedule produces adjusted schedule
- [ ] JSON output works for programmatic consumption

---

## 18. Files Delivered

| File | Purpose |
|------|---------|
| `SPEC-MOBILE-WORKDESK-001.md` | This spec |
| `scheduler_mobile_workdesk.py` | OR-Tools scheduler with rescheduling |
| `scheduler_state.json` | Persistent state (created on first run) |
| `workdesk.set.md` | Set file skeleton (to be completed in MW-038) |

---

## 19. Next Steps

1. **Review this spec** — Q33NR approval
2. **Run scheduler** — `python scheduler_mobile_workdesk.py --max-bees 3` to see initial dispatch order
3. **Dispatch Phase 0 specs** — All 8 SPEC tasks can start immediately in parallel
4. **Begin Phase 5 mobile CSS** — Can run in parallel with Phase 0

**Recommended starting bees:**
- Bee 1-3: SPEC tasks (MW-S01, MW-S02, MW-S03)
- Bee 4: Mobile CSS (MW-023 or MW-024)

---

*End of SPEC-MOBILE-WORKDESK-001*