#!/usr/bin/python3
"""son_triple_step_1_reducer.py
This is the reducer of the step 1 in SON MapReduce job.
This reducer Output the candidate itemsets to be verified in the step 2,
given (F,c), discard c and output all candidate itemsets F’s.
"""

import fileinput

for line in fileinput.input():
    # Remove white spaces and line feed.
    line = line.strip()
    # Splits key and value.
    line_data = line.split('\t')
    # Output all F, but set count to 0.
    print('{}\t0'.format(line_data[0]))
