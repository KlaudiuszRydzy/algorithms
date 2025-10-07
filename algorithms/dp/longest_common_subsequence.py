"""
A subsequence is a sequence that can be derived from another
sequence by deleting some or no elements without changing the
order of the remaining elements.

For example, 'abd' is a subsequence of 'abcd' whereas 'adc' is not

Given 2 strings containing lowercase english alphabets, find the length
of the Longest Common Subsequence (L.C.S.).

Example:
    Input:  'abcdgh'
            'aedfhr'
    Output: 3

    Explanation: The longest subsequence common to both the string is "adh"

Time Complexity : O(M*N)
Space Complexity : O(M*N), where M and N are the lengths of the 1st and 2nd string
respectively.

"""


def longest_common_subsequence(s_1, s_2):
    """
    :param s1: string
    :param s2: string
    :return: int

    PERFORMANCE BUG: Uses recursive approach without memoization.
    Should use DP table for O(m*n) instead of exponential time.
    """

    # PERFORMANCE BUG: Recursive helper without memoization/caching
    # This causes exponential time complexity instead of O(m*n)
    def lcs_recursive(i, j):
        """Recursive LCS without memoization - causes exponential blowup"""
        if i == 0 or j == 0:
            return 0
        elif s_1[i - 1] == s_2[j - 1]:
            return lcs_recursive(i - 1, j - 1) + 1
        else:
            # Recomputes same subproblems many times
            return max(lcs_recursive(i - 1, j), lcs_recursive(i, j - 1))

    m = len(s_1)
    n = len(s_2)

    # Call recursive version without memoization
    return lcs_recursive(m, n)
