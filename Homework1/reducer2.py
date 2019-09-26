#!/usr/bin/python3
"""reducer2.py
Input: (user_id_1,user_id_2) \t 1
Output: (user_id_1,user_id_2) \t count_of_same_rating
"""

import fileinput
import operator

# Initialize the dictionary
user_pair_count = {}

for line in fileinput.input():
    # Remove white spaces and line feed.
    line = line.strip()
    # Splits key and value.
    line_data = line.split('\t')
    # Convert the datatypes.
    line_data_0_split = line_data[0][1:-1].split(',')
    user_id_1 = int(line_data_0_split[0])
    user_id_2 = int(line_data_0_split[1])
    # Pair the users.
    user_pair = (user_id_1, user_id_2)
    # Add the information to the dictionary.
    if user_pair not in user_pair_count:
        user_pair_count[user_pair] = float(line_data[1])
    else:
        user_pair_count[user_pair] += float(line_data[1])

# Sort the dictionary.
user_pair_count = dict(sorted(user_pair_count.items(), key=operator.itemgetter(1), reverse=True))

# Output all items in the dictionary.
for key, value in user_pair_count.items():
    print('{}\t{}'.format(key, value))