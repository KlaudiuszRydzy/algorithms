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
    Performance gate: edit_distance should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be much slower (1000x+).
    After fixing, current should match baseline speed (within 1.5x).
    """
    word_a = "kitten sitting here"  # Length 18
    word_b = "sitting  kittens!"  # Length 18

    # Measure current implementation
    def run_current():
        edit_distance(word_a, word_b)

    current_perf = measure_performance(run_current, n_runs=3, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        edit_distance_baseline(word_a, word_b)

    baseline_perf = measure_performance(run_baseline, n_runs=3, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 1000x+ → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"edit_distance is {slowdown_factor:.1f}x slower than baseline. "
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
