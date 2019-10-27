#!/usr/bin/python3
"""pcy_step_1_mapper.py
This is the mapper of the step 1 in SON MapReduce job.
This mapper runs pass 1 of PCY algorithm on the chunk.
Hashes the pairs into buckets, then pass the pairs and their hash to next step.
"""

import fileinput

# Read the input from STDIN.
lines = fileinput.input()
baskets = []
# One line is a basket.
for line in lines:
    # Remove white spaces and line feed.
    words = line.strip().split()
    baskets += [words]
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
# Remove non-frequent items.
freq_items = {}
for item, count in items.items():
    if count >= support:
        freq_items[item] = count

# Build and hash the pairs.
pair_bucket = {}
items = list(freq_items.keys())
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        pair_bucket[(items[i], items[j])] = hash(items[i] + items[j])

# Output the result.
for key, value in pair_bucket.items():
    print('{}\t{}'.format(key, value))
