# Optimized BFS using collections.deque for O(1) queue operations
import collections

def bfs(grid, matrix, i, j, count):
    """
    BFS helper function using deque for efficient queue operations.
    """
    q = collections.deque([(i, j, 0)])  # Use deque for O(1) popleft
    while q:
        # O(1) operation with deque.popleft()
        i, j, step = q.popleft()
        for k, l in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            if 0<=k<len(grid) and 0<=l<len(grid[0]) and \
                    matrix[k][l][1]==count and grid[k][l]==0:
                matrix[k][l][0] += step+1
                matrix[k][l][1] = count+1
                q.append((k, l, step+1))
