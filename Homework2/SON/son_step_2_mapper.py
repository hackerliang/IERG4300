#!/usr/bin/python3
"""son_step_2_mapper.py
This is the mapper of the step 2 in SON MapReduce job.
This mapper loads the output from the previous job, aka. frequent item sets,
then count the appearances of those sets in the original dataset.
"""

import fileinput
import itertools

frequent_pairs = {}
pairs = {}

# Read the side-loaded input file.
with open('step_1_result.txt', 'r') as f:
    for line in f:
        freq_pair, _ = line.split('\t')
        item_1, item_2 = freq_pair[1:-1].split(', ')
        item_1 = item_1[1:-1]
        item_2 = item_2[1:-1]
        frequent_pairs.setdefault((item_1, item_2), 0)

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
        if pair in frequent_pairs:
            frequent_pairs[pair] += 1
        else:
            continue


# Output the counts to reducer.
for key, value in frequent_pairs.items():
    print('{}\t{}'.format(str(key), str(value)))
