"""
Reusable performance testing utilities for the performance bug suite.

Provides statistical timing measurements with relative speedup gates.
"""

import time
import statistics
from typing import Callable, Any, List, Tuple


def measure_performance(
    func: Callable,
    args: Tuple = (),
    kwargs: dict = None,
    n_runs: int = 10,
    warmup: int = 2
) -> dict:
    """
    Measure function performance over multiple runs.

    Args:
        func: Function to benchmark
        args: Positional arguments for func
        kwargs: Keyword arguments for func
        n_runs: Number of measurement runs
        warmup: Number of warmup runs (not measured)

    Returns:
        dict with keys: times, median, mean, min, max, std
    """
    if kwargs is None:
        kwargs = {}

    # Warmup runs
    for _ in range(warmup):
        func(*args, **kwargs)

    # Measurement runs
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        'times': times,
        'median': statistics.median(times),
        'mean': statistics.mean(times),
        'min': min(times),
        'max': max(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0.0
    }


def assert_speedup(
    baseline_func: Callable,
    fixed_func: Callable,
    args: Tuple = (),
    kwargs: dict = None,
    min_speedup: float = 5.0,
    baseline_runs: int = 10,
    test_runs: int = 10,
    warmup: int = 2
) -> dict:
    """
    Assert that fixed_func is at least min_speedup times faster than baseline_func.

    Args:
        baseline_func: The slow/bugged function
        fixed_func: The optimized function
        args: Arguments to pass to both functions
        kwargs: Keyword arguments to pass to both functions
        min_speedup: Minimum required speedup factor
        baseline_runs: Number of runs for baseline measurement
        test_runs: Number of runs for fixed measurement
        warmup: Number of warmup runs

    Returns:
        dict with keys: baseline_median, fixed_median, speedup, passed

    Raises:
        AssertionError: If speedup < min_speedup
    """
    baseline_perf = measure_performance(
        baseline_func, args, kwargs, baseline_runs, warmup
    )
    fixed_perf = measure_performance(
        fixed_func, args, kwargs, test_runs, warmup
    )

    baseline_median = baseline_perf['median']
    fixed_median = fixed_perf['median']
    speedup = baseline_median / fixed_median if fixed_median > 0 else 0.0

    passed = speedup >= min_speedup

    result = {
        'baseline_median': baseline_median,
        'fixed_median': fixed_median,
        'speedup': speedup,
        'min_speedup': min_speedup,
        'passed': passed
    }

    assert passed, (
        f"Performance test failed: speedup {speedup:.2f}x < required {min_speedup:.2f}x "
        f"(baseline: {baseline_median:.4f}s, fixed: {fixed_median:.4f}s)"
    )

    return result


def compare_results(result1: Any, result2: Any, tolerance: float = 1e-9) -> bool:
    """
    Compare results from two functions for correctness.

    Handles lists, numbers, and nested structures.
    """
    if type(result1) != type(result2):
        return False

    if isinstance(result1, (list, tuple)):
        if len(result1) != len(result2):
            return False
        return all(compare_results(a, b, tolerance) for a, b in zip(result1, result2))

    if isinstance(result1, dict):
        if set(result1.keys()) != set(result2.keys()):
            return False
        return all(compare_results(result1[k], result2[k], tolerance) for k in result1)

    if isinstance(result1, (int, float)):
        return abs(result1 - result2) < tolerance

    return result1 == result2
