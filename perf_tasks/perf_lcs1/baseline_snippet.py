# Optimized version using DP table for O(m*n) time
def longest_common_subsequence(s_1, s_2):
    """
    LCS using dynamic programming with memoization table.
    Time: O(m*n), Space: O(m*n)
    """
    m = len(s_1)
    n = len(s_2)

    mat = [[0] * (n + 1) for i in range(m + 1)]
    # mat[i][j] : contains length of LCS of s_1[0..i-1] and s_2[0..j-1]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                mat[i][j] = 0
            elif s_1[i - 1] == s_2[j - 1]:
                mat[i][j] = mat[i - 1][j - 1] + 1
            else:
                mat[i][j] = max(mat[i - 1][j], mat[i][j - 1])

    return mat[m][n]
