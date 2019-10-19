#!/usr/bin/python3
"""son_step_2_mapper.py
This is the mapper of the step 2 in SON MapReduce job.
This mapper loads the output from the previous job, aka. frequent item sets,
then count the appearances of those sets in the original dataset.
"""

import fileinput

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
# Get support value from threshold.
support = len(baskets) * 0.005

# Build the dictionary for frequent items.
items = {}
# Iterate all items, then count the appearances.
for basket in baskets:
    for word in basket:
        if word not in items:
            items[word] = 1
        else:
            items[word] += 1

# Build pairs.
pairs = {}
items = list(items.keys())
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        pairs[(items[i], items[j])] = 0
# Find and count the pairs in each basket
for basket in baskets:
    for i in range(len(basket)):
        for j in range(i + 1, len(basket)):
            if (basket[i], basket[j]) in pairs:
                pairs[(basket[i], basket[j])] += 1
            elif (basket[j], basket[i]) in pairs:
                pairs[(basket[j], basket[i])] += 1
            else:
                continue

# Output pairs intersect two dictionaries.
output = {x: pairs[x] for x in pairs if x in frequent_pairs}

# Output the counts to reducer.
for key, value in output.items():
    print('{}\t{}'.format(str(key), str(value)))
