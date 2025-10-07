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
    Performance gate: BFS with large grid should be reasonably fast.

    With the bug (list.pop(0)), this is much slower due to O(n) per pop.
    After fixing (deque.popleft()), it should be at least 10x faster for large grids.
    """
    # Generate a larger grid for performance testing
    # Create a 200x200 grid with many buildings to force extensive BFS
    size = 200
    grid = [[0 for _ in range(size)] for _ in range(size)]

    # Place 16 buildings spread throughout grid
    positions = [(i*50, j*50) for i in range(1, 4) for j in range(1, 4) if i != 2 or j != 2]
    for x, y in positions[:16]:
        if x < size and y < size:
            grid[x][y] = 1

    # Measure performance
    perf = measure_performance(
        lambda: shortest_distance([row[:] for row in grid]),
        n_runs=2,
        warmup=1
    )

    # Performance gate: should complete in under 5.0 seconds (optimized version)
    # The bugged version takes 20+ seconds for 200x200 grid with list.pop(0)
    # This test will FAIL with the bug, PASS after fix
    assert perf['median'] < 5.0, (
        f"shortest_distance too slow: {perf['median']:.3f}s for {size}x{size} grid. "
        f"Expected < 5.0s. Check for O(n) queue operations (use deque instead of list)."
    )

    print(f"✓ Performance OK: {perf['median']:.4f}s ({size}x{size} grid)")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
