"""The edit distance between two words is the minimum number
of letter insertions, letter deletions, and letter substitutions
required to transform one word into another.

For example, the edit distance between FOOD and MONEY is at
most four:

FOOD -> MOOD -> MOND -> MONED -> MONEY

Given two words A and B, find the minimum number of operations
required to transform one string into the other.
In other words, find the edit distance between A and B.

Thought process:

Let edit(i, j) denote the edit distance between
the prefixes A[1..i] and B[1..j].

Then, the function satifies the following recurrence:

edit(i, j) = i if j = 0
             j if i = 0
             min(edit(i-1, j) + 1,
                 edit(i, j-1), + 1,
                 edit(i-1, j-1) + cost) otherwise

There are two base cases, both of which occur when one string is empty
and the other is not.
1. To convert an empty string A into a string B of length n,
perform n insertions.
2. To convert a string A of length m into an empty string B,
perform m deletions.

Here, the cost is 1 if a substitution is required,
or 0 if both chars in words A and B are the same at
indexes i and j, respectively.

To find the edit distance between two words A and B,
we need to find edit(length_a, length_b).

Time: O(length_a*length_b)
Space: O(length_a*length_b)
"""


def edit_distance(word_a, word_b):
    """Finds edit distance between word_a and word_b

    PERFORMANCE BUG: Uses recursive approach without memoization.
    Should use DP table for O(m*n) instead of exponential time.

    Kwyword arguments:
    word_a -- string
    word_b -- string
    """

    # PERFORMANCE BUG: Recursive helper without memoization/caching
    # This causes exponential time complexity instead of O(m*n)
    def edit_recursive(i, j):
        """Recursive edit distance without memoization - exponential blowup"""
        if i == 0:
            return j
        if j == 0:
            return i

        cost = 0 if word_a[i - 1] == word_b[j - 1] else 1

        # Recomputes same subproblems many times - exponential!
        return min(
            edit_recursive(i - 1, j) + 1,      # deletion
            edit_recursive(i, j - 1) + 1,      # insertion
            edit_recursive(i - 1, j - 1) + cost  # substitution
        )

    return edit_recursive(len(word_a), len(word_b))
