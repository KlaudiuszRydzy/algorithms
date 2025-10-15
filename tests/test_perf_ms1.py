"""
Performance test for merge_sort (Task: perf_ms1)

Bug: Redundant min() scans in merge loop causing O(n^2) complexity
Expected fix: Remove unnecessary min() calls
"""

import sys
import random
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.sort.merge_sort import merge_sort
from perf_tasks.perf_ms1.baseline_snippet import merge_sort_baseline
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify merge_sort produces correct results"""
    # Test 1: Empty array
    assert merge_sort([]) == []

    # Test 2: Single element
    assert merge_sort([1]) == [1]

    # Test 3: Already sorted
    assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    # Test 4: Reverse sorted
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    # Test 5: Random order
    assert merge_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    # Test 6: Duplicates
    assert merge_sort([5, 5, 5, 5]) == [5, 5, 5, 5]

    # Test 7: Negative numbers
    assert merge_sort([-3, -1, -4, -1, -5]) == [-5, -4, -3, -1, -1]


def test_performance():
    """
    Performance gate: merge_sort should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be much slower (50-100x).
    After fixing, current should match baseline speed (within 1.5x).
    """
    # Generate test data
    random.seed(42)
    n = 10000
    test_data = list(range(n))
    random.shuffle(test_data)

    # Measure current implementation
    def run_current():
        data_copy = test_data.copy()
        merge_sort(data_copy)

    current_perf = measure_performance(run_current, n_runs=3, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        data_copy = test_data.copy()
        merge_sort_baseline(data_copy)

    baseline_perf = measure_performance(run_baseline, n_runs=3, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 50-100x → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"merge_sort is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for O(n^2) operations in merge."
    )

    print(f"✓ Performance OK: {slowdown_factor:.2f}x baseline speed "
          f"(current: {current_time:.3f}s, baseline: {baseline_time:.3f}s)")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
