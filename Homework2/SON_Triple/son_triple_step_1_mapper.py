#!/usr/bin/python3
"""son_triple_step_1_mapper.py
This is the mapper of the step 1 in SON MapReduce job.
This mapper runs A-Priori algorithm on the chunk using support threshold 𝑝𝑠,
output the frequent itemsets for that chunk (F, c), where F is the key (itemset) and c is count (or proportion)
"""

import fileinput
import itertools

# Read the input from STDIN.
lines = fileinput.input()
baskets = []
# One line is a basket.
for line in lines:
    # Remove white spaces and line feed.
    words = line.strip().split()
    baskets += [words]
# Get support value from threshold.
support = len(baskets) * 0.0025
# DEBUG
# support = 1

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
candidate_pairs = {}
items = list(freq_items.keys())
for x in itertools.combinations(items, 2):
    candidate_pairs.setdefault(x, 0)
# Find and count the pairs in each basket
for basket in baskets:
    basket_pairs = itertools.combinations(basket, 2)
    for basket_pair in basket_pairs:
        if basket_pair in candidate_pairs:
            candidate_pairs[basket_pair] += 1
        else:
            continue
# Remove non-frequent pairs.
freq_pairs = {}
for pair, count in candidate_pairs.items():
    if count >= support:
        freq_pairs[pair] = count

# Build frequent triples
# Discard the counts of the frequent pairs.
freq_pairs_list = freq_pairs.keys()
# Extract the items of the pairs.
freq_pairs_member_list = []
for pair in freq_pairs_list:
    freq_pairs_member_list += [pair[0]]
    freq_pairs_member_list += [pair[1]]
# Construct candidate triples.
candidate_triples = {}
for x in itertools.combinations(freq_pairs_member_list, 3):
    candidate_triples.setdefault(x, 0)
# Count triples from baskets.
for basket in baskets:
    basket_triples = itertools.combinations(basket, 3)
    for basket_triple in basket_triples:
        if basket_triple in candidate_triples:
            candidate_triples[basket_triple] += 1
        else:
            continue
# Remove non-frequent triples.
freq_triples = {}
for triple, count in candidate_triples.items():
    if count >= support:
        freq_triples[triple] = count

# Output the result as key-value pair.
for pair, count in freq_triples.items():
    print('{}\t{}'.format(str(pair), str(count)))
