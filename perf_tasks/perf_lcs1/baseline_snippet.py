"""
Baseline (correct) implementation of longest_common_subsequence from master branch.
This is the fast O(m*n) version using DP table.
"""

def longest_common_subsequence_baseline(str_a, str_b):
    """
    Compute longest common subsequence using dynamic programming.
    Complexity: O(m*n) where m, n are lengths of input strings.
    """
    if str_a == "" or str_b == "":
        return 0

    m = len(str_a)
    n = len(str_b)
    dp_table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str_a[i - 1] == str_b[j - 1]:
                dp_table[i][j] = dp_table[i - 1][j - 1] + 1
            else:
                dp_table[i][j] = max(dp_table[i][j - 1], dp_table[i - 1][j])

    return dp_table[m][n]
