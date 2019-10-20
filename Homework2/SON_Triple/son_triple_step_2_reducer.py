#!/usr/bin/python3
"""son_triple_step_2_reducer.py
This is the reducer of the step 2 in SON MapReduce job.
Aggregate the outputs from the mappers, sum up the frequency that each triple appears,
then filter out the triples do not satisfy the minimum support.
"""

import fileinput

triples = {}
# Lines of the dataset * frequency
support = 4340062 * 0.0025

for line in fileinput.input():
    # Remove white spaces and line feed.
    line = line.strip()
    # Splits key and value.
    triple, count = line.split('\t', 1)
    # Convert datatype
    item_1, item_2, item_3 = triple[1:-1].split(', ')
    item_1 = item_1[1:-1]
    item_2 = item_2[1:-1]
    item_3 = item_3[1:-1]
    count = int(count)
    # Save the pairs into memory
    if (item_1, item_2, item_3) in triples:
        triples[(item_1, item_2, item_3)] += count
    elif (item_1, item_3, item_2) in triples:
        triples[(item_1, item_3, item_2)] += count
    elif (item_2, item_1, item_3) in triples:
        triples[(item_2, item_1, item_3)] += count
    elif (item_2, item_3, item_1) in triples:
        triples[(item_2, item_3, item_1)] += count
    elif (item_3, item_1, item_2) in triples:
        triples[(item_3, item_1, item_2)] += count
    elif (item_3, item_2, item_1) in triples:
        triples[(item_3, item_2, item_1)] += count
    else:
        triples[(item_1, item_2, item_3)] = count

# Filter out frequent pairs.
for key, value in triples.items():
    if value >= support:
        print('{}\t{}'.format(str(key), str(value)))
