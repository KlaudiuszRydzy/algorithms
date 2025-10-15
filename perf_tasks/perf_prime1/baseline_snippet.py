"""
Baseline (correct) implementation of prime_check from master branch.
This is the optimized version with sqrt computed once.
"""

def prime_check_baseline(n):
    """
    Check if n is prime efficiently.
    Complexity: O(sqrt(n))
    """
    if n == 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    j = 5
    while j * j <= n:
        if n % j == 0 or n % (j + 2) == 0:
            return False
        j += 6
    return True
