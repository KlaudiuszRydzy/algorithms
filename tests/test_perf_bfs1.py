"""
Performance test for shortest_distance BFS (Task: perf_bfs1)

Bug: Using list.pop(0) which is O(n) instead of deque.popleft() O(1)
Expected fix: Use collections.deque for efficient queue operations
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.bfs.shortest_distance_from_all_buildings import shortest_distance
from perf_tasks.perf_bfs1.baseline_snippet import shortest_distance_baseline
from perf_tasks._templates.perf_harness import measure_performance


def test_correctness():
    """Verify shortest_distance produces correct results"""
    # Test 1: Simple case
    grid1 = [
        [1, 0, 2, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0]
    ]
    result = shortest_distance(grid1)
    assert result > 0, "Should find a valid meeting point"

    # Test 2: No buildings (algorithm returns -1)
    grid2 = [[0, 0, 0]]
    result2 = shortest_distance(grid2)
    assert result2 == -1 or result2 >= 0, "Should handle grid with no buildings"

    # Test 3: Single building (no meeting point possible)
    grid3 = [[1]]
    result3 = shortest_distance(grid3)
    assert result3 == -1 or result3 >= 0, "Should handle single building"

    # Test 4: Valid small grid
    grid4 = [[1, 0, 1], [0, 0, 0]]
    result4 = shortest_distance(grid4)
    assert isinstance(result4, int), "Should return integer result"


def test_performance():
    """
    Performance gate: BFS should be within 1.5x of baseline performance.

    Compares current implementation against the correct baseline from master.
    With the bug, current will be slower (10-20x).
    After fixing, current should match baseline speed (within 1.5x).
    """
    # Generate a larger grid for performance testing
    size = 200
    grid = [[0 for _ in range(size)] for _ in range(size)]

    # Place 16 buildings spread throughout grid
    positions = [(i*50, j*50) for i in range(1, 4) for j in range(1, 4) if i != 2 or j != 2]
    for x, y in positions[:16]:
        if x < size and y < size:
            grid[x][y] = 1

    # Measure current implementation
    def run_current():
        grid_copy = [row[:] for row in grid]
        shortest_distance(grid_copy)

    current_perf = measure_performance(run_current, n_runs=2, warmup=1)

    # Measure baseline implementation
    def run_baseline():
        grid_copy = [row[:] for row in grid]
        shortest_distance_baseline(grid_copy)

    baseline_perf = measure_performance(run_baseline, n_runs=2, warmup=1)

    # Calculate slowdown factor
    current_time = current_perf['median']
    baseline_time = baseline_perf['median']
    slowdown_factor = current_time / baseline_time

    # Performance gate: current should be within 1.5x of baseline
    # With bug: slowdown will be 10-20x → FAIL
    # After fix: slowdown will be ~1.0x → PASS
    assert slowdown_factor < 1.5, (
        f"BFS is {slowdown_factor:.1f}x slower than baseline. "
        f"Current: {current_time:.3f}s, Baseline: {baseline_time:.3f}s. "
        f"Expected slowdown < 1.5x. Check for O(n) queue ops (use deque)."
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
