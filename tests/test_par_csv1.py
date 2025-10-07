"""
Performance test for CSV file processing (Task: par_csv1)

Bug: Sequential file processing instead of parallel with multiprocessing
Expected fix: Use multiprocessing.Pool to process files in parallel
"""

import sys
import csv
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.parallel.csv_processor import process_csv_files
from parallel_tasks._templates.parallel_harness import measure_performance


def generate_test_csvs(num_files: int, rows_per_file: int) -> tuple:
    """Generate CSV files for testing and return temp dir and file paths."""
    temp_dir = tempfile.mkdtemp()
    file_paths = []

    for i in range(num_files):
        file_path = Path(temp_dir) / f"data_{i:03d}.csv"
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'value'])
            writer.writeheader()
            for j in range(rows_per_file):
                writer.writerow({
                    'id': j,
                    'value': (i * rows_per_file + j) % 100  # Predictable values
                })
        file_paths.append(str(file_path))

    return temp_dir, file_paths


def test_correctness():
    """Verify process_csv_files produces correct results."""
    # Create 3 small test files
    temp_dir, file_paths = generate_test_csvs(num_files=3, rows_per_file=10)

    try:
        result = process_csv_files(file_paths)

        assert result['file_count'] == 3, "Should process 3 files"
        assert result['total_count'] == 30, "Should have 30 total records"
        assert result['total_sum'] > 0, "Sum should be positive"
        assert result['mean'] > 0, "Mean should be positive"

        # Verify mean calculation
        expected_mean = result['total_sum'] / result['total_count']
        assert abs(result['mean'] - expected_mean) < 0.01, "Mean should be correct"

    finally:
        shutil.rmtree(temp_dir)


def test_performance():
    """
    Performance gate: Processing multiple files should benefit from parallelization.

    With 8+ files and sufficient work per file, parallel processing with
    multiprocessing.Pool should achieve 2-4× speedup on multi-core systems.
    """
    # Create 12 files with enough data to benefit from parallelization
    temp_dir, file_paths = generate_test_csvs(num_files=12, rows_per_file=500000)

    try:
        perf = measure_performance(
            lambda: process_csv_files(file_paths),
            n_runs=3,
            warmup=1
        )

        # Without parallelization, this should be slow (>2s on typical hardware)
        # With multiprocessing.Pool, should be < 1s on 4+ core systems
        assert perf['median'] > 2.0, (
            f"process_csv_files too fast: {perf['median']:.3f}s for {len(file_paths)} files. "
            f"Expected > 2.0s without parallelization. "
            f"Likely already using parallel processing."
        )

        print(f"✓ Performance gate met: {perf['median']:.4f}s for {len(file_paths)} files (serial)")

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
