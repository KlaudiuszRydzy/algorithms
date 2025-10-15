"""
Baseline (correct) implementation of shortest_distance BFS from master branch.
This version uses deque for efficient O(1) queue operations.
"""

from collections import deque

def shortest_distance_baseline(grid):
    """
    Find shortest distance from all buildings using BFS with deque.
    Complexity: O(m*n*k) where k is number of buildings
    """
    if not grid or not grid[0]:
        return -1

    matrix = [[[0,0] for i in range(len(grid[0]))] for j in range(len(grid))]

    count = 0    # count how many building we have visited
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                bfs_baseline(grid, matrix, i, j, count)
                count += 1

    res = float('inf')
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j][1]==count:
                res = min(res, matrix[i][j][0])

    return res if res!=float('inf') else -1


def bfs_baseline(grid, matrix, i, j, count):
    """BFS using deque for O(1) queue operations"""
    q = deque([(i, j, 0)])
    while q:
        i, j, step = q.popleft()  # Efficient O(1) with deque
        for k, l in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            if 0<=k<len(grid) and 0<=l<len(grid[0]) and \
                    matrix[k][l][1]==count and grid[k][l]==0:
                matrix[k][l][0] += step+1
                matrix[k][l][1] = count+1
                q.append((k, l, step+1))
