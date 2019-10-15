#!/usr/bin/python3
"""son_step_2_mapper.py
This is the mapper of the step 2 in SON MapReduce job.
This mapper takes the output from the previous step,
then count the frequency of the itemsets in local chunk.
"""

import fileinput

pairs = {}

for line in fileinput.input():
    # Remove white spaces and line feed.
    line = line.strip()
    # Splits key and value.
    line_data = line.split('\t')
    # Convert datatype.
    item_1, item_2 = line_data[0][1:-1].split(',')
    # Save the pairs into memory
    if (item_1, item_2) in pairs:
        pairs[(item_1, item_2)] += 1
    elif (item_2, item_1) in pairs:
        pairs[(item_2, item_1)] += 1
    else:
        pairs[(item_1, item_2)] = 1

# Output the counts to reducer.
for key, value in pairs.items():
    print('{}\t{}'.format(str(key), str(value)))
