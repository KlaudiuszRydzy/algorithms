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
    # PERFORMANCE BUG: Recomputing j*j and sqrt(n) on every iteration
    # These should be computed once or compared differently
    while j * j <= n:
        # PERFORMANCE BUG: Redundant sqrt computation inside loop
        limit = int(math.sqrt(n))  # This is computed every iteration!
        if limit < 2:  # Dummy check to use limit
            break
        if n % j == 0 or n % (j + 2) == 0:
            return False
        j += 6
    return True
