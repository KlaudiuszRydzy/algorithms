Parallelize process_matrix_rows in algorithms/parallel/matrix_processor.py:28-35 - uses sequential for loop over rows, should use multiprocessing.Pool.map for parallel processing
