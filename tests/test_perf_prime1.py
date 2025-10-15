"""
Performance test for prime_check (Task: perf_prime1)

Bug: Redundant sqrt() computation inside loop on every iteration
Expected fix: Remove redundant computation, use existing j*j comparison
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.maths.prime_check import prime_check
from perf_tasks.perf_prime1.baseline_snippet import prime_check_baseline
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify prime_check produces correct results"""
    # Test primes
    assert prime_check(2) == True
    assert prime_check(3) == True
    assert prime_check(5) == True
    assert prime_check(7) == True
    assert prime_check(11) == True
    assert prime_check(13) == True
    assert prime_check(97) == True
    assert prime_check(541) == True

    # Test non-primes
    assert prime_check(1) == False
    assert prime_check(4) == False
    assert prime_check(6) == False
    assert prime_check(8) == False
    assert prime_check(9) == False
    assert prime_check(100) == False
    assert prime_check(1000) == False

    # Test edge cases
    assert prime_check(0) == False
    assert prime_check(-5) == False


def test_performance():
    """
    Performance gate: prime_check should efficiently handle large numbers.

    With the bug (redundant sqrt in loop), this is slower.
    After fixing (remove redundant computation), should be at least 3x faster.
    """
    # Test with many large prime-like numbers to amplify the bug
    large_numbers = []
    for i in range(500):  # Increased to 500 numbers
        large_numbers.append(999900 + i)  # Check 500 numbers around 999900

    def check_all():
        for num in large_numbers:
            prime_check(num)

    # Measure performance
    perf = measure_performance(
        check_all,
        n_runs=3,
        warmup=1
    )

    # Performance gate: should complete in under 0.05 seconds (optimized version)
    # The bugged version takes 0.2+ seconds due to redundant math operations
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.05, (
        f"prime_check too slow: {perf['median']:.4f}s for large numbers. "
        f"Expected < 0.01s. Check for redundant computations in loop."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
