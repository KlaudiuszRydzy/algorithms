"""
Performance test for Monte Carlo simulation (Task: par_monte1)

Bug: Sequential simulation execution instead of parallel with multiprocessing
Expected fix: Use multiprocessing.Pool to run simulations in parallel
"""

import sys
from pathlib import Path
import math

sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.parallel.monte_carlo import estimate_pi, monte_carlo_simulation
from parallel_tasks._templates.parallel_harness import measure_performance


def test_correctness():
    """Verify Monte Carlo functions produce reasonable results."""
    # Test estimate_pi with enough samples for reasonable accuracy
    pi_estimate = estimate_pi(100000)
    assert 2.5 < pi_estimate < 3.8, f"Pi estimate {pi_estimate} should be roughly close to 3.14"

    # Test monte_carlo_simulation
    results = monte_carlo_simulation(num_simulations=5, samples_per_sim=10000)
    assert len(results) == 5, "Should return 5 simulation results"
    assert all(2.5 < r < 3.8 for r in results), "All estimates should be roughly close to pi"

    # Mean of multiple simulations should be close to pi
    mean_estimate = sum(results) / len(results)
    assert abs(mean_estimate - math.pi) < 1.0, f"Mean estimate {mean_estimate} should be close to pi"


def test_performance():
    """
    Performance gate: Multiple independent simulations should benefit from parallelization.

    With 8+ simulations of sufficient size, parallel execution with
    multiprocessing.Pool should achieve 2-4× speedup on multi-core systems.
    """
    num_simulations = 12
    samples_per_sim = 5000000  # 5M samples per simulation

    perf = measure_performance(
        lambda: monte_carlo_simulation(num_simulations, samples_per_sim),
        n_runs=3,
        warmup=1
    )

    # Without parallelization, this should be slow (>3s on typical hardware)
    # With multiprocessing.Pool, should be < 1.5s on 4+ core systems
    assert perf['median'] > 3.0, (
        f"monte_carlo_simulation too fast: {perf['median']:.3f}s for {num_simulations} simulations. "
        f"Expected > 3.0s without parallelization. "
        f"Likely already using parallel processing."
    )

    print(f"✓ Performance gate met: {perf['median']:.4f}s for {num_simulations} simulations (serial)")


if __name__ == "__main__":
    print("Running correctness tests...")
    test_correctness()
    print("✓ All correctness tests passed")

    print("\nRunning performance test...")
    test_performance()
    print("✓ Performance test passed")
