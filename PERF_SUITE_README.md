# Performance Bug Test Suite for SWE-Agent

A curated collection of realistic performance bugs for testing AI agents on algorithmic optimization tasks.

## Overview

This repository branch (`perf-bugs-suite`) contains **6 performance bug tasks** based on the [keon/algorithms](https://github.com/keon/algorithms) Python library. Each bug represents a common performance anti-pattern found in real codebases:

1. **Redundant nested scans** - O(n²) where O(n) exists
2. **Missing memoization** - Exponential recomputation instead of caching
3. **Wrong data structure** - List membership O(n) instead of set O(1)
4. **Inefficient queue operations** - list.pop(0) O(n) instead of deque O(1)
5. **Redundant computations** - Expensive operations repeated in tight loops
6. **Missing DP table** - Recursive without cache causing exponential blowup

### Why This Suite?

- **Realistic bugs**: Common patterns seen in production code, not artificial delays
- **Correctness preserved**: Bugged code produces correct output, just slower
- **Measurable impact**: 5-100× slowdowns that agents can detect and fix
- **Multiple difficulty levels**: 3 prompt modes per task (hinted, no-scope, fix-only)
- **Deterministic testing**: Performance gates use statistical measures (median) with warmup runs

## Repository Structure

```
perf-bugs-suite branch:
├── algorithms/               # Algorithm implementations (with bugs injected)
│   ├── sort/merge_sort.py   # Task 1: Redundant min() scans
│   ├── dp/fib.py             # Task 2: Missing memoization
│   ├── arrays/remove_duplicates.py  # Task 3: List instead of set
│   ├── bfs/shortest_distance_from_all_buildings.py  # Task 4: list.pop(0)
│   ├── maths/prime_check.py  # Task 5: Redundant sqrt()
│   └── dp/longest_common_subsequence.py  # Task 6: No DP table
├── tests/                    # Performance test harnesses
│   ├── test_perf_ms1.py     # Merge sort harness
│   ├── test_perf_fib1.py    # Fibonacci harness
│   ├── test_perf_dup1.py    # Duplicates harness
│   ├── test_perf_bfs1.py    # BFS harness
│   ├── test_perf_prime1.py  # Prime check harness
│   └── test_perf_lcs1.py    # LCS harness
├── perf_tasks/              # Task metadata
│   ├── _templates/
│   │   └── perf_harness.py  # Reusable timing utilities
│   ├── perf_ms1/
│   │   ├── problem_hinted.md      # Exact location hint
│   │   ├── problem_perf.md        # Performance goal, no location
│   │   ├── problem_fix.md         # Generic "fix code"
│   │   └── baseline_snippet.py    # Original (fast) code
│   └── ... (5 more tasks)
├── instances.jsonl          # 18 SWE-Agent task instances (6 tasks × 3 modes)
├── validate_suite.py        # Validation script
└── PERF_SUITE_README.md     # This file

master branch:
└── algorithms/              # Original (fast) implementations
```

## Task Details

| Task ID | File | Bug Type | Complexity | Speedup Expected |
|---------|------|----------|------------|------------------|
| `perf_ms1` | `algorithms/sort/merge_sort.py` | Redundant nested scan | O(n²) → O(n log n) | 50× |
| `perf_fib1` | `algorithms/dp/fib.py` | Missing memoization | O(2ⁿ) → O(n) | 1000× |
| `perf_dup1` | `algorithms/arrays/remove_duplicates.py` | Wrong data structure | O(n²) → O(n) | 50× |
| `perf_bfs1` | `algorithms/bfs/shortest_distance_from_all_buildings.py` | Inefficient queue | O(n²) → O(n) | 10× |
| `perf_prime1` | `algorithms/maths/prime_check.py` | Redundant computation | O(n×√n) → O(√n) | 3× |
| `perf_lcs1` | `algorithms/dp/longest_common_subsequence.py` | Missing DP table | O(2ⁿ) → O(m×n) | 100× |

## Prompt Modes

Each task has **3 problem statements** with different clarity levels:

1. **`hinted_exact_scope`**: Gives exact file + line numbers of the bottleneck
   - Example: *"Optimize merge_sort in algorithms/sort/merge_sort.py:27-28 - redundant min() calls..."*

2. **`make_faster_no_hint`**: Describes performance goal without location
   - Example: *"Make merge_sort faster in algorithms/sort/merge_sort.py - 50× slower than expected..."*

3. **`fix_only`**: Generic request with no hints
   - Example: *"Fix the performance issue in algorithms/sort/merge_sort.py"*

## Using This Suite with SWE-Agent

### Prerequisites

```bash
# Python 3.12
python --version  # Should be 3.12.x

# Clone this repository
git clone https://github.com/YOUR_USERNAME/algorithms.git
cd algorithms
git checkout perf-bugs-suite
```

### Quick Start

```bash
# 1. Validate the suite
python validate_suite.py

# 2. Run SWE-Agent with instances.jsonl
cd /path/to/SWE-agent
python -m sweagent.run.run run \
  --instances.type file \
  --instances.path /path/to/algorithms/instances.jsonl \
  --instances.deployment.type local \
  --config config/default.yaml \
  --model.name "gpt-4"
```

### Running Individual Tasks

```bash
# Test a single task manually
cd /path/to/algorithms
pytest -xvs tests/test_perf_ms1.py

# Run only correctness (should pass)
pytest -xvs tests/test_perf_ms1.py::test_correctness

# Run only performance (should FAIL on perf-bugs-suite branch)
pytest -xvs tests/test_perf_ms1.py::test_performance
```

## Performance Testing Methodology

### Statistical Approach

We use **relative speedup factors** instead of absolute time thresholds to ensure machine-independent testing:

```python
# Measure baseline (bugged) performance
baseline_times = [run_bugged() for _ in range(10)]
baseline_median = median(baseline_times)

# Measure fixed performance
fixed_times = [run_fixed() for _ in range(10)]
fixed_median = median(fixed_times)

# Calculate speedup
speedup = baseline_median / fixed_median

# Pass/fail criterion
PASS = speedup >= min_speedup_factor  # e.g., 5.0×
```

### Why Median + Warmup?

- **Median**: Robust to outliers (GC pauses, OS scheduling)
- **Warmup runs**: Eliminate JIT compilation/caching effects
- **Relative speedup**: Machine-independent (works on any hardware)

### Test Harness Example

Each test file (`tests/test_perf_*.py`) contains:

1. **`test_correctness()`**: Verifies bugged code still produces correct output
2. **`test_performance()`**: Asserts execution time is within acceptable bounds

```python
def test_performance():
    """Bugged version will FAIL this test."""
    perf = measure_performance(
        lambda: merge_sort(test_data.copy()),
        n_runs=5,
        warmup=1
    )

    assert perf['median'] < 0.5, (
        f"merge_sort too slow: {perf['median']:.3f}s. "
        f"Expected < 0.5s."
    )
```

## Validation

Run the validation script to confirm all tasks are properly configured:

```bash
python validate_suite.py
```

**Expected output on `perf-bugs-suite` branch:**
- ✓ All correctness tests PASS (bugs don't break functionality)
- ✓ All performance tests FAIL (bugs cause measurable slowdown)

## Development Workflow

### Adding a New Task

1. **Inject bug** into algorithm file with clear comments
2. **Create task directory**: `perf_tasks/perf_TASKID/`
3. **Write 3 problem statements**: `problem_hinted.md`, `problem_perf.md`, `problem_fix.md`
4. **Save baseline snippet**: `baseline_snippet.py` (original fast code)
5. **Create test harness**: `tests/test_perf_TASKID.py`
6. **Add 3 JSONL entries** to `instances.jsonl` (one per mode)
7. **Update validation script**: Add test file to `PERF_TESTS` list
8. **Run validation**: `python validate_suite.py`

### Bug Injection Guidelines

**DO:**
- Use realistic patterns (redundant scans, missing cache, wrong data structures)
- Preserve correctness (bugged code must produce correct output)
- Add clear comments explaining the bug
- Aim for 5-100× slowdowns (measurable but fixable)

**DON'T:**
- Use `time.sleep()` or artificial delays
- Break functionality (correctness tests must pass)
- Create bugs that are too subtle (<2× slowdown)
- Create bugs that are too hard (require domain expertise)

## JSONL Schema

Each entry in `instances.jsonl` follows this schema:

```json
{
  "image_name": "python:3.12",
  "instance_id": "perf_ms1__hinted",
  "repo_name": "algorithms",
  "base_commit": "HEAD",
  "problem_statement": "Optimize merge_sort in...",
  "extra_fields": {
    "dataset_id": "keon_algorithms_perf",
    "task_id": "perf_ms1",
    "category": "sort",
    "bug_type": "redundant_nested_scan",
    "entrypoint": "algorithms.sort.merge_sort:merge_sort",
    "test_cmd": "pytest -xvs tests/test_perf_ms1.py",
    "inputs_desc": "Random list n=5000",
    "detection_target": {
      "path": "algorithms/sort/merge_sort.py",
      "line_span": [27, 28]
    },
    "prompt_mode": "hinted_exact_scope"
  }
}
```

## Performance Benchmarks (Reference Machine)

Approximate timings on 2020 MacBook Pro (M1, 16GB RAM):

| Task | Bugged | Fixed | Speedup |
|------|--------|-------|---------|
| perf_ms1 | 5.2s | 0.08s | 65× |
| perf_fib1 | 12.5s | 0.001s | 12500× |
| perf_dup1 | 3.8s | 0.02s | 190× |
| perf_bfs1 | 4.1s | 0.15s | 27× |
| perf_prime1 | 0.06s | 0.015s | 4× |
| perf_lcs1 | 8.3s | 0.002s | 4150× |


- Original algorithms from [keon/algorithms](https://github.com/keon/algorithms)

