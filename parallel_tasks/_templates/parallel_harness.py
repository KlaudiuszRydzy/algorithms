"""
Performance testing utilities for parallelization tasks.
"""
import time
import statistics
from typing import Callable, Tuple


def measure_performance(
    func: Callable,
    args: Tuple = (),
    kwargs: dict = None,
    n_runs: int = 5,
    warmup: int = 1
) -> dict:
    """
    Measure function performance over multiple runs.

    Args:
        func: Function to measure
        args: Positional arguments to pass to func
        kwargs: Keyword arguments to pass to func
        n_runs: Number of measurement runs
        warmup: Number of warmup runs (excluded from stats)

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
        'std': statistics.stdev(times) if len(times) > 1 else 0
    }


def assert_speedup(
    slow_func: Callable,
    fast_func: Callable,
    args: Tuple = (),
    kwargs: dict = None,
    min_speedup: float = 2.0,
    n_runs: int = 5
) -> dict:
    """
    Assert that fast_func is significantly faster than slow_func.

    Args:
        slow_func: Original (slower) function
        fast_func: Optimized (faster) function
        args: Arguments to pass to both functions
        kwargs: Keyword arguments to pass to both functions
        min_speedup: Minimum required speedup factor
        n_runs: Number of runs for measurement

    Returns:
        dict with speedup statistics
    """
    slow_perf = measure_performance(slow_func, args, kwargs, n_runs)
    fast_perf = measure_performance(fast_func, args, kwargs, n_runs)

    speedup = slow_perf['median'] / fast_perf['median']

    return {
        'slow_median': slow_perf['median'],
        'fast_median': fast_perf['median'],
        'speedup': speedup,
        'meets_target': speedup >= min_speedup
    }
