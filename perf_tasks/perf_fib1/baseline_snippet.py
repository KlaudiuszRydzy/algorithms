"""
Baseline (correct) implementation of fib_list from master branch.
This is the fast O(n) version with proper DP.
"""

def fib_list_baseline(n):
    """
    Computes the n-th fibonacci number using dynamic programming.
    Complexity: O(n)
    """
    assert n >= 0, 'n must be a positive integer'

    list_results = [0, 1]
    for i in range(2, n+1):
        list_results.append(list_results[i-1] + list_results[i-2])
    return list_results[n]
