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
    Performance gate: prime_check should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be slower (3-5x).
    After fixing, current should match baseline speed (within 1.5x).
    """
    # Test with many large prime-like numbers to amplify the bug
    large_numbers = []
    for i in range(500):
        large_numbers.append(999900 + i)

    # Measure current implementation
    def run_current():
        for num in large_numbers:
            prime_check(num)

    current_perf = measure_performance(run_current, n_runs=3, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        for num in large_numbers:
            prime_check_baseline(num)

    baseline_perf = measure_performance(run_baseline, n_runs=3, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 3-5x → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"prime_check is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for redundant computations in loop."
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
