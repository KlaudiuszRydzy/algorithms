"""
Performance test for knapsack (Task: perf_knap1)

Bug: Recursive approach without memoization causing exponential time
Expected fix: Use DP array for O(n*W) memoization
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.dp.knapsack import Item, get_maximum_value
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify get_maximum_value produces correct results"""
    items = [Item(60, 5), Item(50, 3), Item(70, 4), Item(30, 2)]
    assert get_maximum_value(items, 5) == 80

    items2 = [Item(10, 1), Item(20, 2), Item(30, 3)]
    assert get_maximum_value(items2, 5) == 50


def test_performance():
    """
    Performance gate: knapsack should scale O(n*W) not exponentially.
    """
    # Create 22 items
    items = [Item(i*10 + 5, i % 5 + 1) for i in range(22)]
    capacity = 50

    perf = measure_performance(
        lambda: get_maximum_value(items, capacity),
        n_runs=2,
        warmup=1
    )

    assert perf['median'] < 0.5, (
        f"get_maximum_value too slow: {perf['median']:.3f}s for n={len(items)}. "
        f"Expected < 0.5s. Check for missing memoization/DP array."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s (n={len(items)})")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
