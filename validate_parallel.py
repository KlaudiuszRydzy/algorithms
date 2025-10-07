#!/usr/bin/env python3
"""
Validation script for the parallelization task suite.

Runs all parallel test harnesses to verify:
1. Correctness tests pass (serial code produces correct output)
2. Performance tests PASS (code is slow without parallelization)
"""

import subprocess
import sys
from pathlib import Path


# List of all parallel test files
PARALLEL_TESTS = [
    "tests/test_par_csv1.py",
    "tests/test_par_matrix1.py",
    "tests/test_par_monte1.py",
]


def run_command(cmd, capture=True):
    """Run a shell command and return result."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, timeout=120)
            return result.returncode, "", ""
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout after 120 seconds"


def main():
    print("=" * 70)
    print("Parallelization Task Suite Validation")
    print("=" * 70)
    print()

    # Check we're on the right branch
    returncode, stdout, _ = run_command("git branch --show-current")
    current_branch = stdout.strip()
    print(f"Current branch: {current_branch}")
    print()

    # Validate each task
    results = []
    for test_file in PARALLEL_TESTS:
        task_id = Path(test_file).stem.replace("test_", "")
        print(f"\n{'─' * 70}")
        print(f"Testing: {task_id}")
        print(f"{'─' * 70}")

        # Run the test
        print(f"  Running tests...", end=" ")
        returncode, stdout, stderr = run_command(f"python3 {test_file}")

        if returncode == 0:
            print("✓ PASS")
            passed = True
        else:
            print("✗ FAIL")
            print(f"\nError output:\n{stderr}")
            passed = False

        results.append({
            'task': task_id,
            'passed': passed
        })

    # Summary
    print(f"\n{'=' * 70}")
    print("Summary")
    print(f"{'=' * 70}")

    passed_count = sum(r['passed'] for r in results)
    print(f"\nTests passed: {passed_count}/{len(results)}")

    if passed_count == len(results):
        print("\n✓ ✓ ✓ All validation checks PASSED! ✓ ✓ ✓")
        print("\nThe parallelization task suite is working correctly.")
        print("Tasks demonstrate serial execution that would benefit from multiprocessing.")
        return 0
    else:
        print("\n✗ ✗ ✗ Validation FAILED ✗ ✗ ✗")
        print("\nSome tests did not pass.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
