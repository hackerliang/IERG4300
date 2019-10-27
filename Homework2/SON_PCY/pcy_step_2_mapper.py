#!/usr/bin/python3
"""pcy_step_2_mapper.py
This is the mapper of the step 2 in SON MapReduce job.
This mapper loads the output from the previous job, aka. frequent item sets,
then count the appearances of those sets in the original dataset.
"""

import fileinput
import itertools

frequent_pairs = {}
pairs = {}

freq_buckets_count = {}

# Read the side-loaded input file.
with open('pcy_step_1_result.txt', 'r') as f:
    for line in f:
        bucket, count = line.split('\t')
        freq_buckets_count[int(bucket)] = int(count)

# Handle original dataset input from STDIN.
lines = fileinput.input()
baskets = []
# One line is a basket.
for line in lines:
    # Remove white spaces and line feed.
    words = line.strip().split()
    baskets += [words]

# Generate pairs from the basket.
for basket in baskets:
    basket_pair = itertools.combinations(basket, 2)
    for pair in basket_pair:
        if hash(pair) in freq_buckets_count:
            frequent_pairs[pair] += 1
        else:
            continue


# Output the counts to reducer.
for key, value in frequent_pairs.items():
    print('{}\t{}'.format(str(key), str(value)))
