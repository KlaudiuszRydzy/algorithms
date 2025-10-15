# Performance Bug Test Suite for SWE-Agent

## Overview

This repository branch (`perf-bugs-suite`) contains **8 performance bug tasks** based on the [keon/algorithms](https://github.com/keon/algorithms) Python library.

## Repository Structure

```
perf-bugs-suite branch:
├── algorithms/               # Algorithm implementations (with bugs injected)
├── tests/                    # Performance test harnesses with baseline comparison
├── perf_tasks/              # Task metadata and baseline snippets
│   ├── _templates/perf_harness.py  # Reusable timing utilities
│   ├── perf_*/baseline_snippet.py  # Correct implementations from master
│   └── perf_*/problem_*.md         # Problem statements (3 modes each)
├── instances.jsonl          # 24 SWE-Agent task instances (8 tasks × 3 modes)
└── PERF_SUITE_README.md     # This file

master branch:
└── algorithms/              # Original (correct) implementations
```

## Task Details

| Task ID | File | Bug Type | Complexity | Slowdown |
|---------|------|----------|------------|----------|
| `perf_ms1` | `algorithms/sort/merge_sort.py` | Redundant nested scan | O(n²) → O(n log n) | 50× |
| `perf_fib1` | `algorithms/dp/fib.py` | Missing memoization | O(2ⁿ) → O(n) | 190,000× |
| `perf_dup1` | `algorithms/arrays/remove_duplicates.py` | Wrong data structure | O(n²) → O(n) | 340× |
| `perf_bfs1` | `algorithms/bfs/shortest_distance_from_all_buildings.py` | Inefficient queue | O(n²) → O(n) | 1.3× |
| `perf_prime1` | `algorithms/maths/prime_check.py` | Redundant computation | O(n×√n) → O(√n) | 3-5× |
| `perf_lcs1` | `algorithms/dp/longest_common_subsequence.py` | Missing DP table | O(2ⁿ) → O(m×n) | 1000×+ |
| `perf_edit1` | `algorithms/dp/edit_distance.py` | Missing DP table | O(2ⁿ) → O(m×n) | 1000×+ |
| `perf_knap1` | `algorithms/dp/knapsack.py` | Missing memoization | O(2ⁿ) → O(n×W) | 13,000× |

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
# Python 3.11
python --version  # Should be 3.11.x

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
sweagent run-batch \
  --config config/default.yaml \
  --config ./hpc_podman_algorithms.yaml \
  --agent.model.per_instance_cost_limit=0 \
  --agent.model.max_input_tokens=60000
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

Tests use **relative comparison** between buggy code (perf-bugs-suite branch) and correct baseline (master branch):

```python
def test_performance():
    # Measure current (buggy) implementation
    def run_current():
        data_copy = test_data.copy()
        merge_sort(data_copy)
    current_perf = measure_performance(run_current, n_runs=3, warmup=1)

    # Measure baseline (correct) implementation from master
    def run_baseline():
        data_copy = test_data.copy()
        merge_sort_baseline(data_copy)
    baseline_perf = measure_performance(run_baseline, n_runs=3, warmup=1)

    # Calculate slowdown factor
    slowdown_factor = current_perf['median'] / baseline_perf['median']

    # Pass if within 1.5x of baseline (buggy code will fail with 10-1000x slowdown)
    assert slowdown_factor < 1.5, f"Code is {slowdown_factor:.1f}x slower than baseline"
```

## Validation

Run the validation script to confirm all tasks are properly configured:

```bash
python validate_suite.py
```

**Expected output on `perf-bugs-suite` branch:**
- ✓ All correctness tests PASS (bugs don't break functionality)
- ✓ All performance tests FAIL (bugs cause measurable slowdown)

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
  "image_name": "python:3.11",
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

---

Original algorithms from [keon/algorithms](https://github.com/keon/algorithms)

