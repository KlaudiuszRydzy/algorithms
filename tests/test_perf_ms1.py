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
    Performance gate: merge_sort should complete in reasonable time.

    With the bug (redundant min() calls), this will be slow.
    After fixing, it should be at least 10x faster for n=5000.
    """
    # Generate test data
    random.seed(42)
    n = 5000
    test_data = list(range(n))
    random.shuffle(test_data)

    # Measure performance
    perf = measure_performance(
        lambda: merge_sort(test_data.copy()),
        n_runs=5,
        warmup=1
    )

    # Performance gate: should complete in under 0.5 seconds (optimized version)
    # The bugged version takes ~5-10 seconds
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.5, (
        f"merge_sort too slow: {perf['median']:.3f}s for n={n}. "
        f"Expected < 0.5s. Check for O(n^2) operations in merge."
    )

    print(f"✓ Performance OK: {perf['median']:.3f}s (n={n})")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
