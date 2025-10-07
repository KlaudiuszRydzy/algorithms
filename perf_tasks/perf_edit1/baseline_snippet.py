# Optimized version using DP table for O(m*n) time
def edit_distance(word_a, word_b):
    """Finds edit distance using DP table - O(m*n) time"""
    length_a, length_b = len(word_a) + 1, len(word_b) + 1

    edit = [[0 for _ in range(length_b)] for _ in range(length_a)]

    for i in range(1, length_a):
        edit[i][0] = i

    for j in range(1, length_b):
        edit[0][j] = j

    for i in range(1, length_a):
        for j in range(1, length_b):
            cost = 0 if word_a[i - 1] == word_b[j - 1] else 1
            edit[i][j] = min(edit[i - 1][j] + 1, edit[i][j - 1] + 1, edit[i - 1][j - 1] + cost)

    return edit[-1][-1]
