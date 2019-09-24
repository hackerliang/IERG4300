#!/usr/bin/python3
"""receducer.py
The reduce work combines the list of the users that gave same rating for a movie.
Input: (movie_id, rating)   user_id
"""

import fileinput

# Initialize user list variable.
user_list = []

for line in fileinput.input():
    # Splits key and value.
    line_data = line.split('\t')
    # Append the user ids to the list.
    user_list.append(line_data[1])

# Output the list for further process.
print('{}\t{}'.format(line_data[0], user_list))
