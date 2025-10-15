"""
Performance test for remove_duplicates (Task: perf_dup1)

Bug: List membership check (O(n)) in loop causing O(n^2) complexity
Expected fix: Use set for O(1) membership checks, achieving O(n)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.arrays.remove_duplicates import remove_duplicates
from perf_tasks.perf_dup1.baseline_snippet import remove_duplicates_baseline
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify remove_duplicates produces correct results"""
    # Test 1: Empty array
    assert remove_duplicates([]) == []

    # Test 2: No duplicates
    assert remove_duplicates([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    # Test 3: All duplicates
    assert remove_duplicates([1, 1, 1, 1]) == [1]

    # Test 4: Mixed types
    result = remove_duplicates([1, 1, 2, 2, 3, 4, 4, "hey", "hey", "hello"])
    assert result == [1, 2, 3, 4, "hey", "hello"]

    # Test 5: Order preserved
    assert remove_duplicates([3, 1, 2, 1, 3, 2]) == [3, 1, 2]


def test_performance():
    """
    Performance gate: remove_duplicates should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be much slower (50-100x).
    After fixing, current should match baseline speed (within 1.5x).
    """
    # Generate test data with many duplicates
    n = 10000
    test_data = list(range(n // 2)) * 2  # Each number appears twice

    # Measure current implementation
    def run_current():
        remove_duplicates(test_data.copy())

    current_perf = measure_performance(run_current, n_runs=5, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        remove_duplicates_baseline(test_data.copy())

    baseline_perf = measure_performance(run_baseline, n_runs=5, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 50-100x → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"remove_duplicates is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for O(n) list membership (use set)."
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
