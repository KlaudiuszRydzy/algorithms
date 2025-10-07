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

    # Test 2: No buildings
    grid2 = [[0, 0, 0]]
    assert shortest_distance(grid2) == -1

    # Test 3: Single building
    grid3 = [[1]]
    assert shortest_distance(grid3) == -1

    # Test 4: Buildings but no meeting point
    grid4 = [[1, 2, 1]]
    assert shortest_distance(grid4) == -1


def test_performance():
    """
    Performance gate: BFS with large grid should be reasonably fast.

    With the bug (list.pop(0)), this is much slower due to O(n) per pop.
    After fixing (deque.popleft()), it should be at least 10x faster for large grids.
    """
    # Generate a larger grid for performance testing
    # Create a 50x50 grid with a few buildings
    size = 50
    grid = [[0 for _ in range(size)] for _ in range(size)]

    # Place buildings at corners
    grid[0][0] = 1
    grid[0][size-1] = 1
    grid[size-1][0] = 1
    grid[size-1][size-1] = 1

    # Measure performance
    perf = measure_performance(
        lambda: shortest_distance([row[:] for row in grid]),
        n_runs=5,
        warmup=1
    )

    # Performance gate: should complete in under 0.5 seconds (optimized version)
    # The bugged version takes 2-5+ seconds for 50x50 grid
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 0.5, (
        f"shortest_distance too slow: {perf['median']:.3f}s for {size}x{size} grid. "
        f"Expected < 0.5s. Check for O(n) queue operations (use deque instead of list)."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s ({size}x{size} grid)")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
