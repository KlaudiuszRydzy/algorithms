"""
Process multiple CSV files and compute aggregated statistics.

PERFORMANCE BUG: Files are processed sequentially in a single thread.
Should use multiprocessing to process files in parallel.

Example use case: Computing daily statistics from hourly data files,
analyzing log files from multiple servers, aggregating sensor readings.
"""
import csv
from pathlib import Path
from typing import List, Dict


def process_csv_files(file_paths: List[str]) -> Dict[str, float]:
    """
    Process multiple CSV files and compute aggregate statistics.

    PERFORMANCE BUG: Processes files sequentially instead of in parallel.
    Each file is independent and could be processed concurrently using
    multiprocessing.Pool to achieve ~N× speedup on N cores.

    Args:
        file_paths: List of paths to CSV files to process

    Returns:
        Dictionary with aggregate statistics:
        - total_sum: Sum of all numeric values
        - total_count: Total number of records
        - mean: Average value across all files
        - file_count: Number of files processed
    """
    total_sum = 0
    total_count = 0

    # PERFORMANCE BUG: Sequential processing in a single loop
    # Should use: with multiprocessing.Pool() as pool:
    #                results = pool.map(process_single_file, file_paths)
    for file_path in file_paths:
        file_sum, file_count = _process_single_file(file_path)
        total_sum += file_sum
        total_count += file_count

    mean = total_sum / total_count if total_count > 0 else 0

    return {
        'total_sum': total_sum,
        'total_count': total_count,
        'mean': mean,
        'file_count': len(file_paths)
    }


def _process_single_file(file_path: str) -> tuple:
    """
    Process a single CSV file and return sum and count.

    This function is designed to be called by multiprocessing.Pool.
    """
    file_sum = 0
    file_count = 0

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Assume CSV has a 'value' column with numeric data
            value = float(row['value'])
            file_sum += value
            file_count += 1

    return file_sum, file_count
