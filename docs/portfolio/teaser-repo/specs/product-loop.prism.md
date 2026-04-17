---
prism: product_development_loop
version: 1.0.0
---

```yaml
v: "1.0"
id: "product_development_loop"
name: "Product Development Loop - DEF → SIM → EXE"
intention: "Build validated products through simulation before execution"

constraints:
  validation: "3-phase validation before execution"
  quality: "Zero stubs, 100% requirement coverage"

failure_tolerance: "max 3 retries per phase"

entities:
  - type: requirement
    attrs:
      - { name: req_id, dtype: string }
      - { name: category, dtype: string }
      - { name: mandatory, dtype: boolean }
    lifecycle: [defined, validated, implemented, tested]

  - type: spec
    attrs:
      - { name: spec_id, dtype: string }
      - { name: fidelity_score, dtype: float }
    lifecycle: [drafted, gate_0_validated, phase_0_validated, phase_1_validated, approved]

  - type: task
    attrs:
      - { name: task_id, dtype: string }
      - { name: assigned_model, dtype: string }
    lifecycle: [created, dispatched, in_progress, completed]

  - type: code
    attrs:
      - { name: file_path, dtype: string }
      - { name: line_count, dtype: int }
    lifecycle: [stubbed, implemented, tested, shipped]

generators:
  - id: requirement_intake
    entity: requirement
    arrival:
      distribution: poisson
      rate: 10  # requirements per day
    limit: null

resources:
  - id: q33n_coordinator
    capacity: 1
    dispatch:
      mode: priority  # P0 > P1 > P2

  - id: worker_bees
    capacity: 5  # max 5 parallel bees
    dispatch:
      mode: fifo

nodes:
  - id: start
    t: start

  - id: gate_0_validation
    t: task
    resource: q33n_coordinator
    tm:
      d: constant
      val: 5  # seconds for Gate 0

  - id: phase_0_coverage
    t: task
    resource: q33n_coordinator
    tm:
      d: constant
      val: 5  # seconds for Phase 0

  - id: phase_1_spec_fidelity
    t: task
    resource: q33n_coordinator
    tm:
      d: constant
      val: 8  # seconds for Phase 1

  - id: phase_2_task_fidelity
    t: task
    resource: q33n_coordinator
    tm:
      d: constant
      val: 10  # seconds for Phase 2

  - id: dispatch_bees
    t: task
    resource: worker_bees
    tm:
      d: lognorm
      mean: 120  # 2 minutes per bee task
      std: 40    # CV ~0.33

  - id: test_validation
    t: task
    resource: worker_bees
    tm:
      d: constant
      val: 30  # seconds for test runs

  - id: end
    t: end

edges:
  - { s: start, t: gate_0_validation }
  - { s: gate_0_validation, t: phase_0_coverage, condition: "passed" }
  - { s: gate_0_validation, t: gate_0_validation, condition: "retry_count < 3" }
  - { s: phase_0_coverage, t: phase_1_spec_fidelity, condition: "coverage == 1.0" }
  - { s: phase_0_coverage, t: phase_0_coverage, condition: "retry_count < 3" }
  - { s: phase_1_spec_fidelity, t: phase_2_task_fidelity, condition: "fidelity >= 0.85" }
  - { s: phase_1_spec_fidelity, t: phase_1_spec_fidelity, condition: "retry_count < 3" }
  - { s: phase_2_task_fidelity, t: dispatch_bees, condition: "fidelity >= 0.85" }
  - { s: phase_2_task_fidelity, t: phase_2_task_fidelity, condition: "retry_count < 3" }
  - { s: dispatch_bees, t: test_validation }
  - { s: test_validation, t: end, condition: "all_tests_pass" }
  - { s: test_validation, t: dispatch_bees, condition: "retry_count < 2" }

metrics:
  - cycle_time  # DEF → EXE total time
  - validation_cost  # USD for Gate 0 + Phase 0/1/2
  - rework_rate  # % of builds requiring healing loops
  - escalation_rate  # % of builds requiring human intervention
  - autonomous_completion_rate  # % of builds passing all gates
```
