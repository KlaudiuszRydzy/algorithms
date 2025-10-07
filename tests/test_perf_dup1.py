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
    Performance gate: remove_duplicates should scale linearly O(n).

    With the bug (list membership), this is O(n^2).
    After fixing (set membership), it should be O(n), at least 50x faster for n=10000.
    """
    # Generate test data with many duplicates
    n = 10000
    test_data = list(range(n // 2)) * 2  # Each number appears twice

    # Measure performance
    perf = measure_performance(
        lambda: remove_duplicates(test_data.copy()),
        n_runs=5,
        warmup=1
    )

    # Performance gate: should complete in under 0.05 seconds (optimized version)
    # The bugged version takes 2-5 seconds for n=10000
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.05, (
        f"remove_duplicates too slow: {perf['median']:.3f}s for n={n}. "
        f"Expected < 0.05s. Check for O(n) operations in loop (use set instead of list)."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s (n={n})")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
