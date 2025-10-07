"""
Process matrix rows with independent computations.

PERFORMANCE BUG: Rows are processed sequentially in a single thread.
Should use multiprocessing to process rows in parallel.

Example use case: Applying transformations to image rows, computing
statistics per sample in a dataset, batch feature extraction.
"""
import numpy as np
from typing import Callable


def process_matrix_rows(matrix: np.ndarray, func: Callable = None) -> np.ndarray:
    """
    Apply a function to each row of a matrix independently.

    PERFORMANCE BUG: Processes rows sequentially instead of in parallel.
    Each row operation is independent and could be processed concurrently
    using multiprocessing.Pool to achieve ~N× speedup on N cores.

    Args:
        matrix: Input matrix (2D numpy array)
        func: Function to apply to each row. If None, uses default computation.

    Returns:
        Numpy array with processed results for each row
    """
    if func is None:
        func = _default_row_computation

    results = []

    # PERFORMANCE BUG: Sequential processing with for loop
    # Should use: with multiprocessing.Pool() as pool:
    #                results = pool.map(func, matrix)
    for row in matrix:
        result = func(row)
        results.append(result)

    return np.array(results)


def _default_row_computation(row: np.ndarray) -> float:
    """
    Default computation applied to each row.

    Simulates a moderately expensive operation combining multiple statistics.
    """
    # Compute multiple statistics to make it CPU-bound
    mean = np.mean(row)
    std = np.std(row)
    sorted_row = np.sort(row)
    median = np.median(sorted_row)
    q75 = np.percentile(sorted_row, 75)
    q25 = np.percentile(sorted_row, 25)

    # Combine into a single metric
    return mean + std + (q75 - q25) + median
