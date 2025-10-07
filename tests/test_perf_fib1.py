"""
Performance test for fib_list (Task: perf_fib1)

Bug: Missing memoization in helper function causing O(2^n) recomputation
Expected fix: Cache/memoize fib values properly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.dp.fib import fib_list
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify fib_list produces correct Fibonacci numbers"""
    # Test small values
    assert fib_list(0) == 0
    assert fib_list(1) == 1
    assert fib_list(2) == 1
    assert fib_list(3) == 2
    assert fib_list(4) == 3
    assert fib_list(5) == 5
    assert fib_list(6) == 8
    assert fib_list(7) == 13
    assert fib_list(10) == 55
    assert fib_list(15) == 610


def test_performance():
    """
    Performance gate: fib_list should complete quickly for n=30.

    With the bug (missing memoization), this takes 10+ seconds.
    After fixing (proper DP), it should be < 0.01 seconds.
    """
    n = 30

    # Measure performance
    perf = measure_performance(
        lambda: fib_list(n),
        n_runs=5,
        warmup=1
    )

    # Performance gate: should complete in under 0.01 seconds (optimized version)
    # The bugged version takes 10+ seconds for n=30
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.01, (
        f"fib_list too slow: {perf['median']:.3f}s for n={n}. "
        f"Expected < 0.01s. Check for missing memoization/caching."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s (n={n})")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
