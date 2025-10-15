"""
Performance test for edit_distance (Task: perf_edit1)

Bug: Recursive approach without memoization causing exponential time
Expected fix: Use DP table for O(m*n) memoization
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.dp.edit_distance import edit_distance
from perf_tasks.perf_edit1.baseline_snippet import edit_distance_baseline
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify edit_distance produces correct results"""
    # Test 1: Example from docstring
    assert edit_distance("FOOD", "MONEY") == 4

    # Test 2: Identical strings
    assert edit_distance("abc", "abc") == 0

    # Test 3: Empty strings
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "") == 3

    # Test 4: One character difference
    assert edit_distance("cat", "cut") == 1

    # Test 5: Complete replacement
    assert edit_distance("abc", "xyz") == 3


def test_performance():
    """
    Performance gate: edit_distance should scale O(m*n) not exponentially.

    With the bug (no memoization), this is exponential.
    After fixing (DP table), should be O(m*n), at least 100x faster for len=18.
    """
    # Test with strings of moderate length
    word_a = "kitten sitting here"  # Length 18
    word_b = "sitting  kittens!"  # Length 18

    # Measure performance
    perf = measure_performance(
        lambda: edit_distance(word_a, word_b),
        n_runs=3,
        warmup=1
    )

    # Performance gate: should complete in under 0.01 seconds (optimized DP version)
    # The bugged recursive version takes 5+ seconds for length 18
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.01, (
        f"edit_distance too slow: {perf['median']:.3f}s for len={len(word_a)}. "
        f"Expected < 0.01s. Check for missing memoization/DP table."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s (len={len(word_a)})")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
