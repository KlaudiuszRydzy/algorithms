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
from perf_tasks.perf_fib1.baseline_snippet import fib_list_baseline
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
    Performance gate: fib_list should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be much slower (1000x+).
    After fixing, current should match baseline speed (within 1.5x).
    """
    n = 30

    # Measure current implementation
    def run_current():
        fib_list(n)

    current_perf = measure_performance(run_current, n_runs=5, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        fib_list_baseline(n)

    baseline_perf = measure_performance(run_baseline, n_runs=5, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 1000x+ → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"fib_list is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for missing memoization."
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
