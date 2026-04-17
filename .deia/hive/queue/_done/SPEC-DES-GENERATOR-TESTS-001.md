# SPEC-DES-GENERATOR-TESTS-001

**Title:** Expand v2.0 generator test coverage  
**Priority:** P3  
**Status:** DRAFT  
**Date:** 2026-04-15  
**Author:** Q88N  
**Depends on:** None

---

## Problem

The DES engine has token generators for creating arrivals (v2.0 feature). From the audit (2026-04-14):
> "gap_006: v2.0 generator test coverage light"

Generators exist in `simdecisions/des/generators.py` but test coverage is thin:
- Entity attribute sampling not fully tested
- Scheduled arrivals (time windows) not tested
- Generator limits not tested
- Multiple generators interacting not tested
- Warmup period interaction not tested

---

## Solution

Write comprehensive test suite for generator functionality.

---

## Requirements

### R1: Basic arrival tests

```python
def test_exponential_arrivals():
    """Generator produces arrivals at exponential intervals."""
    flow = {
        "generators": [{
            "id": "arrivals",
            "entity": "customer",
            "arrival": {"distribution": "exponential", "rate": 100}
        }],
        # ... minimal flow
    }
    ctx = run_sim(flow, max_sim_time=100)
    
    # ~100 arrivals expected (rate=100/time unit, 100 time units)
    assert 80 < ctx['statistics'].tokens_created < 120

def test_poisson_arrivals():
    """Generator with Poisson process."""
    # Similar, verify arrival count distribution

def test_constant_arrivals():
    """Generator with fixed inter-arrival time."""
    flow = {
        "generators": [{
            "id": "arrivals",
            "entity": "order",
            "arrival": {"distribution": "constant", "value": 10}
        }],
    }
    ctx = run_sim(flow, max_sim_time=100)
    
    # Exactly 10 arrivals (at t=0,10,20,30,40,50,60,70,80,90)
    assert ctx['statistics'].tokens_created == 10
```

### R2: Entity attribute sampling

```python
def test_entity_attribute_distribution():
    """Generated entities have sampled attributes."""
    flow = {
        "generators": [{
            "id": "arrivals",
            "entity": "loan_application",
            "arrival": {"distribution": "exponential", "rate": 100},
            "attributes": {
                "amount": {"distribution": "uniform", "min": 1000, "max": 50000},
                "risk_score": {"distribution": "normal", "mean": 0.5, "std": 0.15}
            }
        }],
    }
    ctx = run_sim(flow, max_sim_time=10)
    
    # Check attribute distributions
    amounts = [t.entity['amount'] for t in ctx['tokens'].completed]
    assert all(1000 <= a <= 50000 for a in amounts)
    
    risks = [t.entity['risk_score'] for t in ctx['tokens'].completed]
    assert 0.4 < mean(risks) < 0.6  # Roughly centered on 0.5

def test_entity_enum_attribute():
    """Generated entities have sampled enum attributes."""
    flow = {
        "generators": [{
            "id": "arrivals",
            "entity": "ticket",
            "arrival": {"distribution": "exponential", "rate": 100},
            "attributes": {
                "priority": {
                    "distribution": "categorical",
                    "values": ["low", "medium", "high"],
                    "weights": [0.5, 0.3, 0.2]
                }
            }
        }],
    }
    ctx = run_sim(flow, max_sim_time=100)
    
    priorities = [t.entity['priority'] for t in ctx['tokens'].completed]
    low_count = priorities.count('low')
    # Roughly 50% should be 'low'
    assert 0.4 < low_count / len(priorities) < 0.6
```

### R3: Scheduled arrivals

```python
def test_schedule_time_window():
    """Generator only fires during scheduled window."""
    flow = {
        "generators": [{
            "id": "work_hours",
            "entity": "call",
            "arrival": {"distribution": "exponential", "rate": 100},
            "schedule": "09:00-17:00"  # 8 hours
        }],
    }
    # Simulate 24 hours
    ctx = run_sim(flow, max_sim_time=86400)
    
    # Arrivals only during 8-hour window
    for token in ctx['tokens'].all:
        arrival = token.created_at
        hour = (arrival % 86400) / 3600
        assert 9 <= hour < 17

def test_schedule_weekdays():
    """Generator respects weekday schedule."""
    flow = {
        "generators": [{
            "id": "business",
            "entity": "order",
            "arrival": {"distribution": "exponential", "rate": 10},
            "schedule": "weekdays"
        }],
    }
    # Simulate 1 week
    ctx = run_sim(flow, max_sim_time=604800)
    
    # No arrivals on Saturday (day 5) or Sunday (day 6)
    for token in ctx['tokens'].all:
        day = int(token.created_at / 86400) % 7
        assert day < 5  # Mon=0 through Fri=4
```

### R4: Generator limits

```python
def test_generator_max_count():
    """Generator stops after max count reached."""
    flow = {
        "generators": [{
            "id": "limited",
            "entity": "item",
            "arrival": {"distribution": "exponential", "rate": 1000},
            "limit": 50
        }],
    }
    ctx = run_sim(flow, max_sim_time=1000)
    
    assert ctx['statistics'].tokens_created == 50

def test_generator_until_time():
    """Generator stops at specified time."""
    flow = {
        "generators": [{
            "id": "timed",
            "entity": "item",
            "arrival": {"distribution": "exponential", "rate": 100},
            "until": 50
        }],
    }
    ctx = run_sim(flow, max_sim_time=100)
    
    # No arrivals after t=50
    for token in ctx['tokens'].all:
        assert token.created_at <= 50
```

### R5: Warmup interaction

```python
def test_warmup_excludes_generator_tokens():
    """Tokens created during warmup excluded from stats."""
    flow = {
        "generators": [{
            "id": "arrivals",
            "entity": "item",
            "arrival": {"distribution": "constant", "value": 10}
        }],
    }
    config = SimConfig(max_sim_time=100, warmup_time=30)
    ctx = run_sim(flow, config)
    
    # Arrivals at t=0,10,20 excluded (warmup)
    # Arrivals at t=30,40,50,60,70,80,90 counted (7 total)
    assert ctx['statistics'].tokens_created_after_warmup == 7
```

### R6: Multiple generators

```python
def test_multiple_generators():
    """Multiple generators produce independent streams."""
    flow = {
        "generators": [
            {
                "id": "type_a",
                "entity": "order_a",
                "arrival": {"distribution": "exponential", "rate": 50}
            },
            {
                "id": "type_b", 
                "entity": "order_b",
                "arrival": {"distribution": "exponential", "rate": 100}
            }
        ],
    }
    ctx = run_sim(flow, max_sim_time=100)
    
    type_a = [t for t in ctx['tokens'].all if t.entity['type'] == 'order_a']
    type_b = [t for t in ctx['tokens'].all if t.entity['type'] == 'order_b']
    
    # Roughly 2:1 ratio
    assert 1.5 < len(type_b) / len(type_a) < 2.5

def test_generators_different_schedules():
    """Generators with different schedules interleave correctly."""
    flow = {
        "generators": [
            {
                "id": "morning",
                "entity": "morning_call",
                "arrival": {"distribution": "exponential", "rate": 100},
                "schedule": "08:00-12:00"
            },
            {
                "id": "afternoon",
                "entity": "afternoon_call",
                "arrival": {"distribution": "exponential", "rate": 100},
                "schedule": "13:00-17:00"
            }
        ],
    }
    ctx = run_sim(flow, max_sim_time=86400)
    
    # Verify no overlap
    for token in ctx['tokens'].all:
        hour = (token.created_at % 86400) / 3600
        if token.entity['type'] == 'morning_call':
            assert 8 <= hour < 12
        else:
            assert 13 <= hour < 17
```

### R7: Reproducibility

```python
def test_generator_seed_reproducibility():
    """Same seed produces identical arrival sequence."""
    flow = {
        "generators": [{
            "id": "arrivals",
            "entity": "item",
            "arrival": {"distribution": "exponential", "rate": 100}
        }],
    }
    
    ctx1 = run_sim(flow, max_sim_time=100, seed=42)
    ctx2 = run_sim(flow, max_sim_time=100, seed=42)
    
    times1 = [t.created_at for t in ctx1['tokens'].all]
    times2 = [t.created_at for t in ctx2['tokens'].all]
    
    assert times1 == times2
```

---

## Implementation Location

| File | Change |
|------|--------|
| `tests/simdecisions/des/test_des_generators.py` | Expand with all test cases |

---

## Acceptance Criteria

- [ ] All R1-R7 test cases written and passing
- [ ] Test coverage for generators.py > 90%
- [ ] Edge cases covered (empty schedule, zero rate, negative values rejected)
- [ ] Tests run in < 5 seconds total (use small time windows)

---

## Estimated Effort

3-4 hours. Straightforward test writing.

---

## Notes

This is a testing spec, not a feature spec. The generator code exists; the tests validate it works as documented. If tests fail, file bugs for the generator implementation.
