"""
This algorithm removes any duplicates from an array and returns a new array with those duplicates
removed.

For example:

Input: [1, 1 ,1 ,2 ,2 ,3 ,4 ,4 ,"hey", "hey", "hello", True, True]
Output: [1, 2, 3, 4, 'hey', 'hello']

PERFORMANCE BUG: Uses list membership check (O(n)) in loop, making overall complexity O(n^2)
"""

def remove_duplicates(array):
    """
    Remove duplicates from array.

    BUG: O(n^2) complexity due to list membership check.
    Should use set for O(1) lookups, making overall O(n).
    """
    new_array = []

    for item in array:
        # PERFORMANCE BUG: 'item in new_array' is O(n) for lists
        # This makes the overall function O(n^2)
        # Should use a set for O(1) membership testing
        if item not in new_array:
            new_array.append(item)

    return new_array