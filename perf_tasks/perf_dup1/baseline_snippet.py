"""
Baseline (correct) implementation of remove_duplicates from master branch.
This is the fast O(n) version using set for O(1) membership testing.
"""

def remove_duplicates_baseline(array):
    """
    Remove duplicates from array using set for O(1) lookups.
    Complexity: O(n)
    """
    new_array = []
    seen = set()

    for item in array:
        if item not in seen:
            new_array.append(item)
            seen.add(item)

    return new_array
