#!/usr/bin/python3
"""pcy_step_1_reducer.py
This is the reducer of the step 1 in SON MapReduce job.
This reducer aggregate the hash values from mappers, count the appearances, then remove infrequent buckets.
"""

import fileinput

# Lines of the dataset * frequency
support = 4340062 * 0.005

bucket_count = {}
for line in fileinput.input():
    line = line.strip()
    # Aggregate the baskets
    _, bucket = line.split('\t')
    if bucket in bucket_count:
        bucket_count[bucket] += 1
    else:
        bucket_count[bucket] = 1

# Output values above the threshold.
for key, value in bucket_count.items():
    if value >= support:
        print('{}\t{}'.format(key, value))
