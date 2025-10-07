"""
Monte Carlo simulation for estimating pi using random sampling.

PERFORMANCE BUG: Trials are executed sequentially in a single thread.
Should use multiprocessing to run trials in parallel.

Example use case: Risk analysis, option pricing, physics simulations,
uncertainty quantification, any embarrassingly parallel simulation.
"""
import random
from typing import List


def estimate_pi(num_samples: int) -> float:
    """
    Estimate pi using Monte Carlo method with random sampling.

    PERFORMANCE BUG: Runs all samples sequentially instead of in parallel batches.
    Independent trials can be parallelized using multiprocessing.Pool to
    achieve ~N× speedup on N cores.

    Method: Generate random points in a unit square and count how many
    fall inside the quarter circle. The ratio approximates pi/4.

    Args:
        num_samples: Number of random samples to generate

    Returns:
        Estimated value of pi
    """
    # PERFORMANCE BUG: Sequential execution of all trials
    # Should split into batches and use:
    #   with multiprocessing.Pool() as pool:
    #       results = pool.map(_run_trial_batch, batch_configs)
    inside_circle = 0

    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            inside_circle += 1

    return 4.0 * inside_circle / num_samples


def _run_trial_batch(num_trials: int) -> int:
    """
    Run a batch of Monte Carlo trials.

    This function is designed to be called by multiprocessing.Pool.

    Args:
        num_trials: Number of trials in this batch

    Returns:
        Count of points inside the circle
    """
    inside = 0
    for _ in range(num_trials):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            inside += 1
    return inside


def monte_carlo_simulation(num_simulations: int, samples_per_sim: int) -> List[float]:
    """
    Run multiple independent Monte Carlo simulations.

    PERFORMANCE BUG: Simulations run sequentially instead of in parallel.
    Each simulation is independent and could run concurrently.

    Args:
        num_simulations: Number of independent simulations to run
        samples_per_sim: Number of samples per simulation

    Returns:
        List of results from each simulation
    """
    results = []

    # PERFORMANCE BUG: Sequential for loop
    # Should use: with multiprocessing.Pool() as pool:
    #                results = pool.map(estimate_pi, [samples_per_sim] * num_simulations)
    for _ in range(num_simulations):
        result = estimate_pi(samples_per_sim)
        results.append(result)

    return results
