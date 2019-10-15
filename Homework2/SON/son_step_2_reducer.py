#!/usr/bin/python3
"""son_step_2_reducer.py
This is the reducer of the step 2 in SON MapReduce job.
Aggregate the outputs from the mappers, sum up the frequency that each pair appears,
then filter out the pairs do not satisfy the minimum support.
"""

import fileinput

pairs = {}
# TODO: where does the support come from?
support = 40000

for line in fileinput.input():
    # Remove white spaces and line feed.
    line = line.strip()
    # Splits key and value.
    pair, count = line.split('\t', 1)
    # Convert datatype
    item_1, item_2 = pair[1:-1].split(',')
    count = int(count)
    # Save the pairs into memory
    if (item_1, item_2) in pairs:
        pairs[(item_1, item_2)] += count
    elif (item_2, item_1) in pairs:
        pairs[(item_2, item_1)] += count
    else:
        pairs[(item_1, item_2)] = count

# Filter out frequent pairs.
for key, value in pairs.items():
    if value >= support:
        print('{}\t{}'.format(str(key), str(value)))
