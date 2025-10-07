"""
Performance test for matrix row processing (Task: par_matrix1)

Bug: Sequential row processing instead of parallel with multiprocessing
Expected fix: Use multiprocessing.Pool to process rows in parallel
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.parallel.matrix_processor import process_matrix_rows
from parallel_tasks._templates.parallel_harness import measure_performance


def test_correctness():
    """Verify process_matrix_rows produces correct results."""
    # Small test matrix
    matrix = np.array([
        [1, 2, 3, 4, 5],
        [10, 20, 30, 40, 50],
        [100, 200, 300, 400, 500]
    ])

    results = process_matrix_rows(matrix)

    # Check basic properties
    assert len(results) == 3, "Should process 3 rows"
    assert all(isinstance(r, (int, float, np.number)) for r in results), "Results should be numeric"
    assert all(r > 0 for r in results), "All results should be positive for positive input"

    # Results should increase for increasing row values
    assert results[1] > results[0], "Larger values should produce larger results"
    assert results[2] > results[1], "Larger values should produce larger results"


def test_performance():
    """
    Performance gate: Processing many matrix rows should benefit from parallelization.

    With 1000+ rows and sufficient computation per row, parallel processing
    with multiprocessing.Pool should achieve 2-4× speedup on multi-core systems.
    """
    # Create large matrix with many rows
    np.random.seed(42)
    matrix = np.random.rand(5000, 5000)  # 5000 rows, 5000 columns each

    perf = measure_performance(
        lambda: process_matrix_rows(matrix),
        n_runs=3,
        warmup=1
    )

    # Without parallelization, this should be slow (>1.5s on typical hardware)
    # With multiprocessing.Pool, should be < 0.8s on 4+ core systems
    assert perf['median'] > 1.5, (
        f"process_matrix_rows too fast: {perf['median']:.3f}s for {len(matrix)} rows. "
        f"Expected > 1.5s without parallelization. "
        f"Likely already using parallel processing."
    )

    print(f"✓ Performance gate met: {perf['median']:.4f}s for {len(matrix)} rows (serial)")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
