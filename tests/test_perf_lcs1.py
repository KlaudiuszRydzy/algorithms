"""
Performance test for longest_common_subsequence (Task: perf_lcs1)

Bug: Recursive approach without memoization causing exponential time
Expected fix: Use DP table for O(m*n) memoization
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.dp.longest_common_subsequence import longest_common_subsequence
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify longest_common_subsequence produces correct results"""
    # Test 1: Example from docstring
    assert longest_common_subsequence('abcdgh', 'aedfhr') == 3

    # Test 2: Identical strings
    assert longest_common_subsequence('abc', 'abc') == 3

    # Test 3: No common subsequence
    assert longest_common_subsequence('abc', 'def') == 0

    # Test 4: One empty string
    assert longest_common_subsequence('', 'abc') == 0
    assert longest_common_subsequence('abc', '') == 0

    # Test 5: Partial match
    assert longest_common_subsequence('programming', 'gaming') == 6  # 'gramin'


def test_performance():
    """
    Performance gate: LCS should scale polynomially O(m*n) not exponentially.

    With the bug (no memoization), this is exponential.
    After fixing (DP table), should be O(m*n), at least 100x faster for len=25.
    """
    # Generate test strings
    s1 = 'a' * 12 + 'b' * 13  # Length 25
    s2 = 'b' * 13 + 'a' * 12  # Length 25

    # Measure performance
    perf = measure_performance(
        lambda: longest_common_subsequence(s1, s2),
        n_runs=5,
        warmup=1
    )

    # Performance gate: should complete in under 0.01 seconds (optimized DP version)
    # The bugged recursive version takes 10+ seconds for length 25
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.01, (
        f"longest_common_subsequence too slow: {perf['median']:.3f}s for len=25. "
        f"Expected < 0.01s. Check for missing memoization/DP table."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s (len=25)")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
