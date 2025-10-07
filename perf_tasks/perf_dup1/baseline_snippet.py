# Optimized version using set for O(1) membership checks
def remove_duplicates(array):
    """
    Remove duplicates from array efficiently.
    O(n) complexity using set for membership testing.
    """
    seen = set()
    new_array = []

    for item in array:
        if item not in seen:
            seen.add(item)
            new_array.append(item)

    return new_array
