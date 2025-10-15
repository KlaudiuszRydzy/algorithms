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
from perf_tasks.perf_lcs1.baseline_snippet import longest_common_subsequence_baseline
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
    Performance gate: LCS should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be much slower (1000x+).
    After fixing, current should match baseline speed (within 1.5x).
    """
    str_a = "abcdefghijklmnopqrstuvwxy"  # 25 chars
    str_b = "bcdefghijklmnopqrstuvwxyz"  # 25 chars

    # Measure current implementation
    def run_current():
        longest_common_subsequence(str_a, str_b)

    current_perf = measure_performance(run_current, n_runs=3, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        longest_common_subsequence_baseline(str_a, str_b)

    baseline_perf = measure_performance(run_baseline, n_runs=3, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 1000x+ → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"LCS is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for missing memoization/DP table."
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
