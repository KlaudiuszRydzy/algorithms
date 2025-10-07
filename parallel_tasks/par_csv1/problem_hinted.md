Parallelize process_csv_files in algorithms/parallel/csv_processor.py:29-36 - uses sequential for loop, should use multiprocessing.Pool to process files in parallel
