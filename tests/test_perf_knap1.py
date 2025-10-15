"""
Performance test for knapsack (Task: perf_knap1)

Bug: Recursive approach without memoization causing exponential time
Expected fix: Use DP array for O(n*W) memoization
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.dp.knapsack import Item, get_maximum_value
from perf_tasks.perf_knap1.baseline_snippet import get_maximum_value_baseline, Item as ItemBaseline
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify get_maximum_value produces correct results"""
    items = [Item(60, 5), Item(50, 3), Item(70, 4), Item(30, 2)]
    assert get_maximum_value(items, 5) == 80

    items2 = [Item(10, 1), Item(20, 2), Item(30, 3)]
    assert get_maximum_value(items2, 5) == 50


def test_performance():
    """
    Performance gate: knapsack should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be much slower (1000x+).
    After fixing, current should match baseline speed (within 1.5x).
    """
    # Create 22 items
    items = [Item(i*10 + 5, i % 5 + 1) for i in range(22)]
    capacity = 50

    # Measure current implementation
    def run_current():
        get_maximum_value(items, capacity)

    current_perf = measure_performance(run_current, n_runs=2, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        get_maximum_value_baseline(items, capacity)

    baseline_perf = measure_performance(run_baseline, n_runs=2, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 1000x+ → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"knapsack is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for missing memoization/DP array."
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
