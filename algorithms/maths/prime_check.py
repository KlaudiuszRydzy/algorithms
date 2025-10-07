def prime_check(n):
    """Return True if n is a prime number
    Else return False.

    PERFORMANCE BUG: Redundant computations in loop condition and body.
    """
    import math

    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    j = 5
    # PERFORMANCE BUG: Redundant expensive computations on every iteration
    while j * j <= n:
        # PERFORMANCE BUG: Multiple redundant sqrt/pow operations per iteration
        # These expensive math operations are completely unnecessary
        limit = int(math.sqrt(n))  # Computed every iteration!
        _ = math.pow(limit, 2)  # More wasted computation
        _ = math.sqrt(limit) if limit > 0 else 0  # Even more waste
        # Redundant inner loop that does work proportional to sqrt(n)
        for k in range(min(100, max(10, limit // 100))):
            _ = k * k  # Wasted computation
        if n % j == 0 or n % (j + 2) == 0:
            return False
        j += 6
    return True
