#!/usr/bin/python3
"""receducer.py
The reducer go through the list of the users and the ratings, grab the users give the same rating.
Input: movie_id \t (user_id,rating)
Output: [user_id_1,user_id_2] \t 1
The user ids in the output always in ascending order.
Then pass through to another MR job to count the number.
"""

import fileinput

# Initialize user id / rating mapping
rating_uid = {}

for line in fileinput.input():
    # Remove white spaces and line feed.
    line = line.strip()
    # Splits key and value.
    line_data = line.split('\t')
    # Convert the datatypes.
    line_data_1_split = line_data[1][1:-1].split(',')
    user_id = int(line_data_1_split[0])
    rating = float(line_data_1_split[1])

    # Debug
    # print('{}\t{}\t{}'.format(line_data[0], user_id, rating))

    # Add the rating to the dictionary.
    if rating in rating_uid:
        if user_id not in rating_uid[rating]:
            rating_uid[rating] += [user_id]
        else:
            continue
    else:
        rating_uid[rating] = [user_id]

for _, value in rating_uid.items():
    # Build the record as two users a pair.
    # Sort the value.
    value = sorted(value)
    # Go through the user list, form the pairs.
    for i in range(0, len(value)):
        for j in range(i + 1, len(value)):
            print('({},{})\t1'.format(value[i], value[j]))