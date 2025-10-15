"""
Baseline (correct) implementation of knapsack from master branch.
This is the fast O(n*W) version using DP array.
"""

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight


def get_maximum_value_baseline(items, capacity):
    """
    Knapsack using dynamic programming.
    Complexity: O(n*W) where n is number of items, W is capacity.
    """
    dp = [0] * (capacity + 1)
    for item in items:
        for cur_weight in reversed(range(item.weight, capacity+1)):
            dp[cur_weight] = max(dp[cur_weight], item.value + dp[cur_weight - item.weight])
    return dp[capacity]
