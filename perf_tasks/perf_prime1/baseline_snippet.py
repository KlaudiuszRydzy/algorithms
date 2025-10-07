# Optimized version without redundant computations
def prime_check(n):
    """Return True if n is a prime number, else False."""
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    j = 5
    # Efficient: j*j computed in condition, no extra sqrt calls
    while j * j <= n:
        if n % j == 0 or n % (j + 2) == 0:
            return False
        j += 6
    return True
