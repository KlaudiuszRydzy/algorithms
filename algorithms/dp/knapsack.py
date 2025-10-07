"""
Given the capacity of the knapsack and items specified by weights and values,
return the maximum summarized value of the items that can be fit in the
knapsack.

Example:
capacity = 5, items(value, weight) = [(60, 5), (50, 3), (70, 4), (30, 2)]
result = 80 (items valued 50 and 30 can both be fit in the knapsack)

The time complexity is O(n * m) and the space complexity is O(m), where n is
the total number of items and m is the knapsack's capacity.
"""


class Item:

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight


def get_maximum_value(items, capacity):
    """
    PERFORMANCE BUG: Uses recursive approach without memoization.
    Should use DP array for O(n*W) instead of exponential time.
    """
    # PERFORMANCE BUG: Recursive helper without memoization - exponential!
    def knapsack_recursive(index, remaining_capacity):
        """Recursive knapsack without memoization - O(2^n)"""
        if index >= len(items) or remaining_capacity <= 0:
            return 0

        # Can't include this item
        if items[index].weight > remaining_capacity:
            return knapsack_recursive(index + 1, remaining_capacity)

        # Try both including and excluding current item
        include = items[index].value + knapsack_recursive(index + 1, remaining_capacity - items[index].weight)
        exclude = knapsack_recursive(index + 1, remaining_capacity)

        return max(include, exclude)

    return knapsack_recursive(0, capacity)

