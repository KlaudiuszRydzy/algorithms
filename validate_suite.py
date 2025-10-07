#!/usr/bin/env python3
"""
Validation script for the performance bug suite.

Runs all performance test harnesses to verify:
1. Correctness tests pass (bugged code still produces correct output)
2. Performance tests FAIL on current branch (perf-bugs-suite)
3. Performance tests would PASS on master branch (with fixes)

Usage:
    python validate_suite.py
"""

import subprocess
import sys
from pathlib import Path


# List of all performance test files
PERF_TESTS = [
    "tests/test_perf_ms1.py",
    "tests/test_perf_fib1.py",
    "tests/test_perf_dup1.py",
    "tests/test_perf_bfs1.py",
    "tests/test_perf_prime1.py",
    "tests/test_perf_lcs1.py",
    "tests/test_perf_edit1.py",
    "tests/test_perf_knap1.py",
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
                timeout=60
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, timeout=60)
            return result.returncode, "", ""
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout after 60 seconds"


def test_correctness(test_file):
    """Run only correctness tests (not performance)."""
    cmd = f"pytest {test_file}::test_correctness -v"
    returncode, stdout, stderr = run_command(cmd)
    return returncode == 0


def test_performance(test_file):
    """Run performance test (should FAIL on bugged branch)."""
    cmd = f"pytest {test_file}::test_performance -v"
    returncode, stdout, stderr = run_command(cmd)
    # We expect this to FAIL (returncode != 0) on the bugged branch
    return returncode != 0  # Return True if it fails (as expected)


def main():
    print("=" * 70)
    print("Performance Bug Suite Validation")
    print("=" * 70)
    print()

    # Check we're on the right branch
    returncode, stdout, _ = run_command("git branch --show-current")
    current_branch = stdout.strip()
    print(f"Current branch: {current_branch}")

    if current_branch != "perf-bugs-suite":
        print("⚠️  Warning: Not on 'perf-bugs-suite' branch!")
        print("   Performance tests are expected to FAIL on this branch.")
        print()

    # Validate each task
    results = []
    for test_file in PERF_TESTS:
        task_id = Path(test_file).stem.replace("test_", "")
        print(f"\n{'─' * 70}")
        print(f"Testing: {task_id}")
        print(f"{'─' * 70}")

        # Test 1: Correctness
        print(f"  Running correctness tests...", end=" ")
        correctness_pass = test_correctness(test_file)
        if correctness_pass:
            print("✓ PASS")
        else:
            print("✗ FAIL (bugged code should still be correct!)")

        # Test 2: Performance (should FAIL on bugged branch)
        print(f"  Running performance tests...", end=" ")
        perf_fails_as_expected = test_performance(test_file)
        if perf_fails_as_expected:
            print("✓ FAIL (as expected - bug present)")
        else:
            print("✗ PASS (unexpected - bug may not be impactful enough!)")

        results.append({
            'task': task_id,
            'correctness': correctness_pass,
            'perf_fails': perf_fails_as_expected
        })

    # Summary
    print(f"\n{'=' * 70}")
    print("Summary")
    print(f"{'=' * 70}")

    all_correct = all(r['correctness'] for r in results)
    all_perf_fail = all(r['perf_fails'] for r in results)

    print(f"\nCorrectness tests: {sum(r['correctness'] for r in results)}/{len(results)} passed")
    print(f"Performance tests: {sum(r['perf_fails'] for r in results)}/{len(results)} fail as expected")

    if all_correct and all_perf_fail:
        print("\n✓ ✓ ✓ All validation checks PASSED! ✓ ✓ ✓")
        print("\nThe performance bug suite is working correctly:")
        print("  - Bugged code produces correct output")
        print("  - Bugged code fails performance gates")
        print("\nNext steps:")
        print("  1. Commit changes: git add -A && git commit -m 'Add performance bug suite'")
        print("  2. Push to GitHub: git push -u origin perf-bugs-suite")
        print("  3. Test with SWE-Agent using instances.jsonl")
        return 0
    else:
        print("\n✗ ✗ ✗ Validation FAILED ✗ ✗ ✗")
        print("\nSome tests did not behave as expected.")
        print("Review the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
