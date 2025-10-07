def merge_sort(arr):
    """ Merge Sort
        Complexity: O(n log(n))
    """
    # Our recursive base case
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    # Perform merge_sort recursively on both halves
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])

    # Merge each side together
    # return merge(left, right, arr.copy()) # changed, no need to copy, mutate inplace.
    merge(left,right,arr)
    return arr


def merge(left, right, merged):
    """ Merge helper
        Complexity: O(n) - BUG: Actually O(n^2) due to redundant scans
    """

    left_cursor, right_cursor = 0, 0
    while left_cursor < len(left) and right_cursor < len(right):
        # PERFORMANCE BUG: Redundant scan through arrays on each iteration
        # This makes merge O(n^2) instead of O(n)
        left_min = min(left[left_cursor:]) if left_cursor < len(left) else float('inf')
        right_min = min(right[right_cursor:]) if right_cursor < len(right) else float('inf')

        # Sort each one and place into the result
        if left[left_cursor] <= right[right_cursor]:
            merged[left_cursor+right_cursor]=left[left_cursor]
            left_cursor += 1
        else:
            merged[left_cursor + right_cursor] = right[right_cursor]
            right_cursor += 1
    # Add the left overs if there's any left to the result
    for left_cursor in range(left_cursor, len(left)):
        merged[left_cursor + right_cursor] = left[left_cursor]
    # Add the left overs if there's any left to the result
    for right_cursor in range(right_cursor, len(right)):
        merged[left_cursor + right_cursor] = right[right_cursor]

    # Return result
    # return merged # do not return anything, as it is replacing inplace.
