#!/usr/bin/python3
"""son_step_1_mapper.py
This is the mapper of the step 1 in SON MapReduce job.
This mapper runs A-Priori algorithm on the chunk using support threshold 𝑝𝑠,
output the frequent itemsets for that chunk (F, c), where F is the key (itemset) and c is count (or proportion)
"""

import fileinput
from operator import itemgetter

# Read the input from STDIN.
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
# Remove non-frequent items.
freq_items = {}
for item, count in items.items():
    if count >= support:
        freq_items[item] = count

# Build frequent item pairs.
pairs = {}
items = list(freq_items.keys())
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
# Remove non-frequent pairs.
freq_pairs = {}
for pair, count in pairs.items():
    if count >= support:
        freq_pairs[pair] = count
# Sort the dictionary.
freq_pairs = dict(sorted(freq_pairs.items(), key=itemgetter(1)))

# Output the result as key-value pair.
for pair, count in freq_pairs.items():
    print('{}\t{}'.format(str(pair), str(count)))
